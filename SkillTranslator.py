import json
import os.path
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

	There is 3 time.sleep() function in the code. 2 of them are to help
	reduce the chances of google IP blocking
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
		self._error = 0

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
			self.logWarning(f'PreChecks are enabled. NOTE: No file writing will occur.')

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
			self.translateSynonyms(activeLanguage)
			# Wait 15 seconds so dialogTemplate file has been written and closed before opening it again
			if not self.getConfig('preCheck'):
				self.logInfo(f'Waiting 15 seconds for write access to dialogTemplate file....')
				time.sleep(15)

			self.translateDialogFile(activeLanguage)
		self.writeInstallConditions()


	def translateTalksfile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateTalks', replace=[self._languageNames[activeLanguage]]), )
		# Path to the active language talks file
		file = Path(f'{self._translationPath}/talks/{self._skillLanguage}.json')

		# load the contents of the active language file
		talksData = json.loads(file.read_text())

		# create instance of translator
		translator = Translator()
		translated = translator.__class__  # i'm guessing this is correct

		# Check if we have all the language files. If not make them
		if not os.path.isfile(Path(f'{self._translationPath}/talks/{activeLanguage}.json')):
			with open(Path(f'{self._translationPath}/talks/{activeLanguage}.json'), 'x'):
				self.logInfo(self.randomTalk(text='talkNotExist', replace=[activeLanguage]))

		# choose the file to be translated
		translatedFile = Path(f'{self._translationPath}/talks/{activeLanguage}.json')

		for key, value in talksData.items():
			defaultList = list()
			shortList = list()
			try:
				for i, defaultTalk in enumerate(value['default']):
					# do safe guards
					self.characterCountor(text=defaultTalk)
					self.requestLimitChecker()
					# If not doing a preCheck then request the translation
					if not self.getConfig('preCheck'):
						translated = translator.translate(defaultTalk, dest=activeLanguage)
					# Start counting talks file characters
					if self._precheckTrigger == 1:
						self._talkDefaultCount += len(defaultTalk)
					# Start counting requests
					self._requestLimiter += 1

					# If not preChecks then add translations to a list
					if not self.getConfig('preCheck'):
						defaultList.append(translated.text)
					else:
						defaultList.append(defaultTalk)

				for i, shortTalk in enumerate(value['short']):
					self.characterCountor(text=shortTalk)
					self.requestLimitChecker()

					if not self.getConfig('preCheck'):
						translated = translator.translate(shortTalk, dest=activeLanguage)

					if self._precheckTrigger == 1:
						self._talkShortCount += len(shortTalk)
					self._requestLimiter += 1

					if not self.getConfig('preCheck'):
						shortList.append(translated.text)
					else:
						shortList.append(shortTalk)

				if defaultList[0] and shortList[0]:

					temp = {
						'default': defaultList,
						'short'  : shortList
					}
				else:
					temp = {
						'default': defaultList
					}

				self._translatedData[f'{key}'] = temp
			except:
				self.logError(f' If you see this, chances are the talk file is missing "default" or "short" keys. Ammend and re run translation ')
				self._error = 1
				break
		if not self.getConfig('preCheck'):
			translatedFile.write_text(json.dumps(self._translatedData, ensure_ascii=False, indent=4))


	def translateDialogFile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateDialog', replace=[self._languageNames[activeLanguage]]), )
		# Check for the language file. if not then create them
		if not os.path.isfile(Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')):
			with open(Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json'), 'x'):
				self.logInfo(self.randomTalk(text='dialogNotExist', replace=[activeLanguage]))

		# The Language file that the skill was written in
		file = Path(f'{self._translationPath}/dialogTemplate/{self._skillLanguage}.json')
		# The file we are going to translate into
		translatedFile = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')

		dialogData = json.loads(file.read_text())
		# create a new instance
		translator = Translator()
		translated = translator.__class__

		for i, item in enumerate(dialogData['intents']):

			dialogList = list()
			for utterance in item['utterances']:
				self.characterCountor(text=utterance)
				self.requestLimitChecker()

				if not self.getConfig('preCheck'):
					translated = translator.translate(utterance, dest=activeLanguage)

				if self._precheckTrigger == 1:
					self._dialogCount += len(utterance)
				self._requestLimiter += 1

				if not self.getConfig('preCheck'):
					dialogList.append(translated.text)
				else:
					dialogList.append(utterance)
			item['utterances'] = dialogList

		if not self.getConfig('preCheck'):
			translatedFile.write_text(json.dumps(dialogData, ensure_ascii=False, indent=4))


	def translateSynonyms(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateSyn', replace=[self._languageNames[activeLanguage]]))
		# The Language file the skill was written in
		file = Path(f'{self._translationPath}/dialogTemplate/{self._skillLanguage}.json')

		# The language dile we are going to translate into
		translatedFile = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')

		synonymData = json.loads(file.read_text())
		# create a new instance
		translator = Translator()
		translated = translator.__class__

		for i, item in enumerate(synonymData['slotTypes']):

			synList = list()
			for slotValue in item['values']:
				# Using try in case user has empty Synonym lists (index out of range errors)
				try:
					for synonym in slotValue['synonyms']:
						self.characterCountor(text=synonym)
						self.requestLimitChecker()

						if not self.getConfig('preCheck'):
							translated = translator.translate(synonym, dest=activeLanguage)

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
					translatedFile.write_text(json.dumps(synonymData, ensure_ascii=False, indent=4))


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
			totalTalk = self._talkDefaultCount + self._talkShortCount
			self.logInfo(f' Pre check\'s completed.... Satistics are as follows')
			if self._error == 1:
				self.logWarning(f'There are errors in the talk file. Please ammend them before translating (refer syslog)')
				self._error = 0
			self.logInfo("")
			self.logInfo(f'Talks file is {totalTalk} characters long on one instance')
			self.logInfo(f'Utterances  are {self._dialogCount} characters long on another instance')
			self.logInfo(f'Synonyms are {self._synonymCount} characters long on another instance')
			self.logInfo('')
			self.logInfo(f'there\'s a character count total of {self._characterCounter}')
			self.logInfo(f' and there would be {self._requestLimiter} requests made')
			self.logInfo(f'Limits are 15k for characters (per instance ?) and maximum of 600 requests per minute')
			self.logInfo('')
			self.logInfo(f'Please turn off preChecks in skill Settings to start Translating')


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
