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
	There is a time.sleep() function in the code set for 70 seconds
	to reduce chances of google IP blocking
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
		super().__init__()


	@IntentHandler('TranslateSkill')
	def translateSkill(self, session: DialogSession, **_kwargs):
		if not self.getConfig('skillLanguage') or not self.getConfig('skillLanguage') in self._supportedLanguages:
			self.logWarning(self.randomTalk(text='invalidLang'))
			return
		self._languageNames = {
			'en': 'English',
			'de': 'German',
			'fr': 'French',
			'it': 'Italian'
		}
		if self._languageNames:
			self.logInfo(self.randomTalk(text='translateDialog', replace=[self._languageNames['en']]))
			return
		# get the default language of the skill from config
		self._skillLanguage = self.getConfig('skillLanguage')
		# list of supported languages
		self._supportedLanguages.remove(self._skillLanguage)

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
			self.translateTalksfile(activeLanguage)
			self.translateSynonyms(activeLanguage)
			self.translateDialogFile(activeLanguage)


	def translateTalksfile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateTalks', replace=[self._languageNames[activeLanguage]]), )
		# Path to the active language talks file
		file = Path(f'{self._translationPath}/talks/{self._skillLanguage}.json')

		# load the contents of the active language file
		talksData = json.loads(file.read_text())
		# create instance of translator
		translator = Translator()
		# Check if we have all the language files. If not make them
		if not os.path.isfile(Path(f'{self._translationPath}/talks/{activeLanguage}.json')):
			with open(Path(f'{self._translationPath}/talks/{activeLanguage}.json'), 'x'):
				self.logInfo(self.randomTalk(text='talkNotExist', replace=[activeLanguage]))

		# choose the file to be translated
		translatedFile = Path(f'{self._translationPath}/talks/{activeLanguage}.json')
		for key, value in talksData.items():
			defaultList = list()
			shortList = list()

			for i, defaultTalk in enumerate(value['default']):
				self.characterCountor(text=defaultTalk)
				self.requestLimitChecker()
				translated = translator.translate(defaultTalk, dest=activeLanguage)
				self._requestLimiter += 1
				defaultList.append(translated.text)

			for i, shortTalk in enumerate(value['short']):
				self.characterCountor(text=shortTalk)
				self.requestLimitChecker()
				translated = translator.translate(shortTalk, dest=activeLanguage)
				self._requestLimiter += 1
				shortList.append(translated.text)

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
		translator = Translator()

		for i, item in enumerate(dialogData['intents']):

			dialogList = list()
			for utterance in item['utterances']:
				self.characterCountor(text=utterance)
				self.requestLimitChecker()
				translated = translator.translate(utterance, dest=activeLanguage)
				self._requestLimiter += 1
				dialogList.append(translated.text)

			item['utterances'] = dialogList
		# print(f' dialog utterances are now ->> {item["utterances"]}')
		translatedFile.write_text(json.dumps(dialogData, ensure_ascii=False, indent=4))

		self.writeInstallConditions()


	def translateSynonyms(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateSyn', replace=[self._languageNames[activeLanguage]]))
		# The Language file the skill was written in
		file = Path(f'{self._translationPath}/dialogTemplate/{self._skillLanguage}.json')
		# The language dile we are going to translate into
		translatedFile = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')

		synonymData = json.loads(file.read_text())
		translator = Translator()

		for i, item in enumerate(synonymData['slotTypes']):

			synList = list()
			for slotValue in item['values']:
				# Using try in case user has empty Synonym lists (index out of range errors)
				try:
					for synonym in slotValue['synonyms']:
						self.characterCountor(text=synonym)
						self.requestLimitChecker()
						translated = translator.translate(synonym, dest=activeLanguage)
						self._requestLimiter += 1
						synList.append(translated.text)
						synList.append(synonym)

					item['values'][0]['synonyms'] = synList
				except:
					continue
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
				file.write_text(json.dumps(installData, ensure_ascii=False, indent=4))

		self.logInfo(self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter]))
		self.say(
			text=self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter])
		)


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
