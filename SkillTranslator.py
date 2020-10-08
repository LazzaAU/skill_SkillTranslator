import json
import time

from pathlib import Path
from googletrans import Translator
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class SkillTranslator(AliceSkill):
	"""
	Author: Lazza
	Description: Translates your skill into other languages

	There is 2 time.sleep() function in the code. They may not trigger in alot of cases but are there
	 to help reduce the chances of google IP blocking
	"""


	def __init__(self):

		self._translatedData = dict()
		self._supportedLanguages = ['en', 'de', 'it', 'fr']
		self._skillLanguage = ""
		self._skillName = ""
		self._translationPath = Path
		self._manualPath = Path
		self._languageNames = dict()
		self._requestLimiter = 0
		self._characterCounter = 0
		self._talkDefaultCount = 0
		self._talkShortCount = 0
		self._dialogCount = 0
		self._synonymCount = 0
		self._precheckTrigger = 0

		super().__init__()


	@IntentHandler('TranslateSkill')
	def translateSkill(self, session: DialogSession, **_kwargs):
		if not self.getConfig('skillLanguage') or not self.getConfig('skillLanguage') in self._supportedLanguages:
			self.logWarning(self.randomTalk(text='invalidLang'))
			return

		# convert language abbreviations
		self._languageNames = {
			'en': 'English',
			'de': 'German',
			'fr': 'French',
			'it': 'Italian'
		}

		# do prechecks if this is enabled
		if self.getConfig('preCheck'):
			self.logWarning(self.randomTalk(text='precheckHeading'))

		# get the default language of the skill from config
		self._skillLanguage = self.getConfig('skillLanguage')
		# list of supported languages
		self._supportedLanguages.remove(self._skillLanguage)

		# set the skill to process as this skill if nothing configured in settings
		if not self.getConfig('skillTitle'):
			self._skillName = self.name
		else:
			self._skillName = self.getConfig('skillTitle')

		# Set the path of the skill folder to translate
		if self.getConfig('skillPath'):
			self._translationPath = Path(f'{self.getConfig("skillPath")}/{self._skillName}')
		else:
			self._translationPath = Path(self.Commons.rootDir(), f'skills/{self._skillName}')

		self.logDebug(self.randomTalk(text='path', replace=[self._translationPath]))

		if self.getConfig('skillTitle') and not self._translationPath.exists():
			self.logWarning(self.randomTalk(text='missingSkill', replace=[self._skillName]))
			return

		# triggers the main code process
		self._requestLimiter = 0
		self.iterateActiveLanguage()

		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text='startTranslate'),
			siteId=session.siteId
		)


	def iterateActiveLanguage(self):
		self.logInfo(self.randomTalk(text='translatingSkill', replace=[self._skillName]))

		for activeLanguage in self._supportedLanguages:
			# precheck Trigger used so counter later on only triggers for first file
			self._precheckTrigger += 1

			self.translateTalksfile(activeLanguage)
			self.translateDialogFile(activeLanguage)
		self.writeInstallConditions()


	def checkFileExists(self, activeLanguage, path, talkFile):
		# If language file doesnt exists and preCheck is not enabled then create it
		if not Path(f'{self._translationPath}/talks/{activeLanguage}.json').exists() and not self.getConfig('preChecks'):
			with open(Path(f'{self._translationPath}/{path}/{activeLanguage}.json'), 'x'):
				self.logInfo(self.randomTalk(text=talkFile, replace=[activeLanguage]))

		# if language file doesn't exist and preCheck is on, then just tell the user it will be created but don't create it (prevents later error)
		elif not Path(f'{self._translationPath}/talks/{activeLanguage}.json').exists() and self.getConfig('preChecks'):
			self.logInfo(self.randomTalk(text='talkNotExist', replace=[activeLanguage]))


	def processTalksFileDictionary(self, talkValue, translator, activeLanguage, defaultList):
		translated = translator.__class__  # i'm guessing this is correct, just want to decalre it
		talkDictionary = dict(talkValue[1])

		for i, message in enumerate(talkDictionary['default']):
			# do safe guard checks
			self.characterCountor(text=message)
			self.requestLimitChecker()
			# If not doing a preCheck then request the translation
			if not self.getConfig('preCheck'):
				translated = translator.translate(message, dest=activeLanguage)

			# Start counting talks file characters
			if self._precheckTrigger == 1:
				self._talkDefaultCount += len(message)
			# Start counting requests
			self._requestLimiter += 1

			# If not preChecks then add translations to a list
			if not self.getConfig('preCheck'):
				defaultList.append(translated.text)
			else:
				defaultList.append(message)

		if not 'short' in dict(talkDictionary).keys():
			self._translatedData = {
				'default': defaultList
			}

		else:
			self.processTalksFileShortKey(value=talkDictionary, translator=translator, activeLanguage=activeLanguage, defaultList=defaultList)


	def processTalksFileShortKey(self, value, translator, activeLanguage, defaultList):
		translated = translator.__class__  # i'm guessing this is correct, just want to decalre it
		shortList = list()

		for message in value['short']:

			self.characterCountor(text=message)
			self.requestLimitChecker()

			if not self.getConfig('preCheck'):
				translated = translator.translate(message, dest=activeLanguage)

			if self._precheckTrigger == 1:
				self._talkShortCount += len(message)
			self._requestLimiter += 1

			if not self.getConfig('preCheck'):
				shortList.append(translated.text)
			else:
				shortList.append(message)

		self._translatedData = {
			'default': defaultList,
			'short'  : shortList
		}


	def processTalksFileLists(self, talk, translator, activeLanguage):
		translated = translator.__class__  # i'm guessing this is correct, just want to decalre it
		talkList = list()

		for message in talk[1]:
			self.characterCountor(text=message)
			self.requestLimitChecker()

			if not self.getConfig('preCheck'):
				translated = translator.translate(message, dest=activeLanguage)
			if self._precheckTrigger == 1:
				self._talkShortCount += len(message)
			self._requestLimiter += 1

			if not self.getConfig('preCheck'):
				talkList.append(translated.text)
			else:
				talkList.append(message)

		return talkList


	# There are three options to account for in the talks file.
	# User codes with default keys and short , or just default keys or no keys (as a list)
	# This below method gets broken up into three sections for sonar readabilty acceptance
	def translateTalksfile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateTalks', replace=[self._languageNames[activeLanguage]]), )
		# Path to the active language talks file
		file = Path(f'{self._translationPath}/talks/{self._skillLanguage}.json')

		# load the contents of the active language file
		talksData = json.loads(file.read_text())

		# create instance of translator
		translator = Translator()

		# Check if we have all the language files. If not make them
		self.checkFileExists(activeLanguage=activeLanguage, path='talks', talkFile='talkNotExist')

		# choose the file to be translated
		translatedFile = Path(f'{self._translationPath}/talks/{activeLanguage}.json')

		for talkValue in talksData.items():
			defaultList = list()

			if isinstance(talkValue[1], dict):
				self.processTalksFileDictionary(talkValue=talkValue, translator=translator, activeLanguage=activeLanguage, defaultList=defaultList)
				talksData[talkValue[0]] = self._translatedData

			elif isinstance(talkValue[1], list):
				result = self.processTalksFileLists(talk=talkValue, translator=translator, activeLanguage=activeLanguage)
				talksData[talkValue[0]] = result

		# write to file
		if not self.getConfig('preCheck'):
			translatedFile.write_text(json.dumps(talksData, ensure_ascii=False, indent=4))


	def translateDialogFile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateDialog', replace=[self._languageNames[activeLanguage]]), )
		# Check for the language file. if not then create them
		if not Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json'):
			with open(Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json'), 'x'):
				self.logInfo(self.randomTalk(text='dialogNotExist', replace=[activeLanguage]))

		# The Language file that the skill was written in
		file = Path(f'{self._translationPath}/dialogTemplate/{self._skillLanguage}.json')
		# The file we are going to translate into

		dialogData = json.loads(file.read_text())
		# create a new instance
		translatorUtterance = Translator()
		translated = translatorUtterance.__class__

		for i, item in enumerate(dialogData['intents']):

			dialogList = list()
			for utterance in item['utterances']:
				self.characterCountor(text=utterance)
				self.requestLimitChecker()

				if not self.getConfig('preCheck'):
					translated = translatorUtterance.translate(utterance, dest=activeLanguage)

				if self._precheckTrigger == 1:
					self._dialogCount += len(utterance)
				self._requestLimiter += 1

				if not self.getConfig('preCheck'):
					dialogList.append(translated.text)
				else:
					dialogList.append(utterance)
			item['utterances'] = dialogList

		self.translateSynonyms(activeLanguage=activeLanguage, dialogData=dialogData)


	def translateSynonyms(self, activeLanguage, dialogData):
		self.logDebug(self.randomTalk(text='translateSyn', replace=[self._languageNames[activeLanguage]]))

		# The language file we are going to translate into
		translatedFile = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')

		# create a new instance
		translatorSyn = Translator()
		translated = translatorSyn.__class__

		for i, item in enumerate(dialogData['slotTypes']):

			synList = list()
			for slotValue in item['values']:
				# Using try in case user has empty Synonym lists (index out of range errors)
				try:
					for synonym in slotValue['synonyms']:
						self.characterCountor(text=synonym)
						self.requestLimitChecker()

						if not self.getConfig('preCheck'):
							translated = translatorSyn.translate(synonym, dest=activeLanguage)

						if self._precheckTrigger == 1:
							self._synonymCount += len(synonym)
						self._requestLimiter += 1

						if not self.getConfig('preCheck'):
							synList.append(translated.text)
						else:
							synList.append(synonym)

					item['values'][0]['synonyms'] = synList

				except:
					continue

				if not self.getConfig('preCheck'):
					translatedFile.write_text(json.dumps(dialogData, ensure_ascii=False, indent=4))


	def writeInstallConditions(self):
		self.logDebug(self.randomTalk(text='updateInstall'))
		# Lets update the install file language conditions
		file = Path(f'{self._translationPath}/{self._skillName}.install')
		installData = json.loads(file.read_text())
		supportedLanguages = ['en', 'de', 'it', 'fr']

		for i, item in enumerate(installData['conditions']):
			if 'lang' in item:
				installData['conditions']['lang'] = supportedLanguages

				if not self.getConfig('preCheck'):
					file.write_text(json.dumps(installData, ensure_ascii=False, indent=4))

		if not self.getConfig('preCheck'):
			self.logInfo(self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter]))
			self.say(
				text=self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter])
			)

		if self.getConfig('preCheck'):
			self.say(
				text='Please check your system log for pre check results'
			)
			totalTalk = self._talkDefaultCount + self._talkShortCount
			self.logInfo(self.randomTalk(text='resultsHeading'))
			self.logInfo(f'')
			self.logInfo(self.randomTalk(text='results1', replace=[totalTalk]))
			self.logInfo(self.randomTalk(text='results2', replace=[self._dialogCount]))
			self.logInfo(self.randomTalk(text='results3', replace=[self._synonymCount]))
			self.logInfo('')
			self.logInfo(self.randomTalk(text='results4', replace=[self._characterCounter]))
			self.logInfo(self.randomTalk(text='results5', replace=[self._requestLimiter]))
			self.logInfo(self.randomTalk(text='results6'))
			self.logInfo('')
			self.logInfo(self.randomTalk(text='results7'))


	def requestLimitChecker(self):
		"""
		Used to prevent google blocking your Ip from exceeding 600
		 requests per minute
		"""
		seconds: float = 70
		if self._requestLimiter == 550:
			self.logDebug(self.randomTalk(text='breather', replace=[seconds]))
			time.sleep(seconds)
			self._requestLimiter = 0


	def characterCountor(self, text):
		"""
		Used as a last resort if the character count is about to hit the Google quota
		"""
		seconds: float = 3660
		self._characterCounter += len(text)

		if self._characterCounter == 14900:
			self.logDebug(self.randomTalk(text='majorLimit', replace=[seconds, self._characterCounter]))
			time.sleep(seconds)
