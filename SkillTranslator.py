import json
import time
import re

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
	 to help reduce the chances of google IP blocking.
	 self._developerUse is only triggered manually by the skill dev (by setting to True). and used
	 for doing dummy runs on certain code in english without annoying google.

	"""


	def __init__(self):

		self._translatedData = dict()
		self._supportedLanguages = ['en', 'de', 'it', 'fr', 'pl']
		self._translatedLanguages = ['en', 'de', 'it', 'fr', 'pl']
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
		self._sampleCount = 0
		self._precheckTrigger = 0
		self._requestTotal = 0
		self._instructionCount = 0
		self._developerUse = False
		self._translateThis = ""

		super().__init__()


	@IntentHandler('TranslateSkill')
	def translateSkill(self, session: DialogSession, **_kwargs):

		# internal (developer) use only
		if self._developerUse and not self.getConfig('preCheck'):
			self.logError(f'Nope, i ain\'t gonna do anything until you turn on preCheck')
			return

		# give user feedback that shes doing it
		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text='startTranslate'),
			siteId=session.siteId
		)

		# Wait 5 seconds or the above endDialog wont speak until the end of translating on some larger files
		self.ThreadManager.doLater(
			interval=5,
			func=self.runTranslateProcess
		)


	def runTranslateProcess(self):

		# convert language abbreviations
		self._languageNames = {
			'en': 'English',
			'de': 'German',
			'fr': 'French',
			'it': 'Italian',
			'pl': 'Polish'
		}

		# do prechecks if this is enabled
		if self.getConfig('preCheck'):
			self.logWarning(self.randomTalk(text='precheckHeading'))
		if self._developerUse:
			self.logWarning(f'Your in internal developer mode. Things will get written')

		# get the default language of the skill from config

		self._skillLanguage = self.getConfig('skillLanguage')

		# Remove the sillLanguage from the translatedLanguage list
		index = self._supportedLanguages.index(self._skillLanguage)
		numberOfSupportedLanguages = len(self._supportedLanguages)

		if len(self._translatedLanguages) == numberOfSupportedLanguages:
			self._translatedLanguages.pop(index)

		# remove languages user chooses to ignore
		if self.getConfig("ignoreLanguages"):
			for lang in self.getConfig("ignoreLanguages").split(","):
				index = self._translatedLanguages.index(lang)
				if lang in self._translatedLanguages:
					self._translatedLanguages.pop(index)

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


	def translateOnlySelectedfolder(self, activeLanguage) -> bool:
		if self._translateThis.lower() == 'talks':
			self.translateTalksfile(activeLanguage)
			self.logInfo(self.randomTalk(text='translatingOnlyThis', replace=[self._translateThis]), )
			return True
		elif self._translateThis.lower() == 'dialog':
			self.translateDialogFile(activeLanguage)
			self.logInfo(self.randomTalk(text='translatingOnlyThis', replace=[self._translateThis]), )
			return True
		elif self._translateThis.lower() == 'instructions':
			self.translateInstructions(activeLanguage)
			self.logInfo(self.randomTalk(text='translatingOnlyThis', replace=[self._translateThis]), )
			return True
		elif self._translateThis.lower() == 'samples':
			self.translateSamples(activeLanguage)
			self.logInfo(self.randomTalk(text='translatingOnlyThis', replace=[self._translateThis]), )
			return True
		else:
			self.logError(self.randomTalk(text='notValidFolder', replace=[self._translateThis]), )
			return False


	def iterateActiveLanguage(self):
		self.logInfo(self.randomTalk(text='translatingSkill', replace=[self._skillName]))

		self._translateThis = self.getConfig('translateOnlyThis')

		for activeLanguage in self._translatedLanguages:
			# precheck Trigger used so counter later on only triggers for first file
			self._precheckTrigger += 1
			if self._translateThis and not self.getConfig('precheck'):
				valid = self.translateOnlySelectedfolder(activeLanguage=activeLanguage)
				if not valid:
					self.say(
						text=self.randomTalk(text='notValidFolder', replace=[self._translateThis]),
					)
					return
			else:
				self.translateTalksfile(activeLanguage)
				self.translateDialogFile(activeLanguage)
				self.translateInstructions(activeLanguage)
				self.translateSamples(activeLanguage)
		if not self._translateThis:
			self.writeInstallConditions()
		else:
			self.endOfprocessing()


	def checkFileExists(self, activeLanguage, path, talkFile, fileType):
		# If language file doesnt exists and preCheck is not enabled then create it
		if not Path(f'{self._translationPath}/{path}/{activeLanguage}{fileType}').exists() and not self.getConfig('preCheck'):
			with open(Path(f'{self._translationPath}/{path}/{activeLanguage}{fileType}'), 'x'):
				self.logInfo(self.randomTalk(text=talkFile, replace=[activeLanguage]))

		# if language file doesn't exist and preCheck is on, then just tell the user it will be created but don't create it (prevents later error)
		elif not Path(f'{self._translationPath}/{path}/{activeLanguage}{fileType}').exists() and self.getConfig('preCheck'):
			self.logInfo(self.randomTalk(text=talkFile, replace=[activeLanguage]))


	# There are three options to account for in the talks file.
	# User codes with default keys and short keys , or just default keys or no keys (as a list)
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
		self.checkFileExists(activeLanguage=activeLanguage, path='talks', talkFile='talkNotExist', fileType=".json")

		# choose the file to be translated
		translatedFile = Path(f'{self._translationPath}/talks/{activeLanguage}.json')

		# Get the value from the talks file
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


	def processTalksFileDictionary(self, talkValue, translator, activeLanguage: str, defaultList: list):
		"""
		enumerate each line of the talk file and process as required

		:param talkValue: The string from talks file currently being processed
		:param translator: The Translator instance
		:param activeLanguage: The active language thats being process
		:param defaultList: stores the translated data in a list
		:return: either stores dict to self._translatedData or moves on to process short dictionary values
		"""
		# The value of the dictionary - the key
		talkDictionary = dict(talkValue[1])

		for i, message in enumerate(talkDictionary['default']):
			defaultList = self.doCommonTasks(text=message, activeLanguage=activeLanguage, transInstance=translator, translatedList=defaultList, triggeredFrom='talk')

		if not 'short' in dict(talkDictionary).keys():
			self._translatedData = {
				'default': defaultList
			}

		else:
			self.processTalksFileShortKey(value=talkDictionary, translator=translator, activeLanguage=activeLanguage, defaultList=defaultList)


	def doCommonTasks(self, text: str, activeLanguage: str, transInstance, translatedList: list, triggeredFrom):
		"""
		Do the common tasks between several of the methods

		:param text: The active line of code to translate
		:param activeLanguage: the current language that's being processed
		:param transInstance: A instance of the translator
		:param translatedList: The list for storing the translated values
		:param triggeredFrom: What triggered this code, options= talk, dialog, synnoyms
		:return: Translated values (or non translated values if in preCheck mode)
		"""
		translated = transInstance.__class__  # i'm guessing this is correct, just want to declare it ?

		# do safe guard checks
		self.characterCountor(text=text)
		self.requestLimitChecker()

		# If not doing a preCheck then request the translation
		if not self.getConfig('preCheck'):
			translated = transInstance.translate(text, dest=activeLanguage)

		# Start counting file characters
		if self._precheckTrigger == 1:
			if triggeredFrom == 'talk':
				self._talkDefaultCount += len(text)
			elif triggeredFrom == 'dialog':
				self._dialogCount += len(text)
			elif triggeredFrom == 'synonym':
				self._synonymCount += len(text)
			elif triggeredFrom == 'talkShort':
				self._talkShortCount += len(text)

		# Start counting requests
		self._requestLimiter += 1
		self._requestTotal += 1

		# If not preChecks then add translations to a list
		if not self.getConfig('preCheck'):
			translatedList.append(translated.text)
		else:
			translatedList.append(text)

		return translatedList


	def processTalksFileShortKey(self, value, translator, activeLanguage, defaultList):
		shortList = list()

		for message in value['short']:
			shortList = self.doCommonTasks(text=message, activeLanguage=activeLanguage, transInstance=translator, translatedList=shortList, triggeredFrom='talkShort')

		self._translatedData = {
			'default': defaultList,
			'short'  : shortList
		}


	# if the talks file item is a list not a dictionary
	def processTalksFileLists(self, talk, translator, activeLanguage):
		talkList = list()

		for message in talk[1]:
			talkList = self.doCommonTasks(text=message, activeLanguage=activeLanguage, transInstance=translator, translatedList=talkList, triggeredFrom='talkShort')

		return talkList


	def translateDialogFile(self, activeLanguage):
		self.logDebug(self.randomTalk(text='translateDialog', replace=[self._languageNames[activeLanguage]]), )
		# Check if we have all the language files. If not make them
		self.checkFileExists(activeLanguage=activeLanguage, path='dialogTemplate', talkFile='dialogNotExist', fileType='.json')

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
				# check safe guards
				self.characterCountor(text=utterance)
				self.requestLimitChecker()

				utterance, translatedUtterance = self.removeDialogCodeSnippet(utterance=utterance, translated=translated, activeLanguage=activeLanguage, translatorUtterance=translatorUtterance)

				if self._precheckTrigger == 1:
					self._dialogCount += len(utterance)
				self._requestLimiter += 1
				self._requestTotal += 1

				if not self.getConfig('preCheck'):
					dialogList.append(translatedUtterance)
				else:
					# Internal debugging aid
					if self._developerUse:
						utterance = f'DUMMY RUN - {utterance}'
					dialogList.append(utterance)

			item['utterances'] = dialogList
			# Internal debugging aid
			if self._developerUse:
				self.logWarning(f'Request counter = {self._requestLimiter}')

		self.translateSynonyms(activeLanguage=activeLanguage, dialogData=dialogData)


	def removeDialogCodeSnippet(self, utterance, translated, activeLanguage, translatorUtterance):
		### Extract dialog code ":=>keyValue}" so it doesnt get translated
		storeCodeSnippet = list()
		# Remove the code string and store in a list
		for word in utterance.split(" "):
			removedCode = re.search(':=>(.*)}', word)
			if removedCode:
				storeCodeSnippet.append(removedCode.group())

		# replace the code in the utterance with {0}
		for code in storeCodeSnippet:
			utterance = str(utterance).replace(code, '{0}')

		if self._developerUse:
			self.logWarning(f'DevMode - stripped utterance is "{utterance}" ')
		if not self.getConfig('preCheck'):
			translated = translatorUtterance.translate(utterance, dest=activeLanguage)

		# put the codedSnippet back in the string
		translatedUtterance = ""
		if not self.getConfig('preCheck'):
			translatedUtterance = str(translated.text)
		while storeCodeSnippet:
			if self.getConfig('preCheck'):
				utterance = str(utterance).replace("{0}", storeCodeSnippet[0], 1)
			else:
				translatedUtterance = str(translatedUtterance).replace(" {0}", storeCodeSnippet[0], 1)
			# Internal debugging aid
			if self._developerUse:
				self.logWarning(f'Rebuilding translated Utterance "{utterance}" ')

			storeCodeSnippet.pop(0)

		return utterance, translatedUtterance


	def translateSynonyms(self, activeLanguage, dialogData):
		self.logDebug(self.randomTalk(text='translateSyn', replace=[self._languageNames[activeLanguage]]))

		# The language file we are going to translate into
		translatedFile = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.json')

		# create a new instance
		translatorSyn = Translator()

		for i, item in enumerate(dialogData['slotTypes']):

			synList = list()
			for slotValue in item['values']:
				# Using try in case user has empty Synonym lists (index out of range errors)
				try:
					for synonym in slotValue['synonyms']:
						synList = self.doCommonTasks(text=synonym, activeLanguage=activeLanguage, transInstance=translatorSyn, translatedList=synList, triggeredFrom='synonym')

					item['values'][0]['synonyms'] = synList

				except:
					continue

		if not self.getConfig('preCheck'):
			translatedFile.write_text(json.dumps(dialogData, ensure_ascii=False, indent=4))
		if self._developerUse:
			translatedFile.write_text(json.dumps(dialogData, ensure_ascii=False, indent=4))


	def translateSamples(self, activeLanguage):

		self.logDebug(self.randomTalk(text='translateSamples', replace=[self._languageNames[activeLanguage]]), )

		# Check if we have all the language files. If not make them
		self.checkFileExists(activeLanguage=activeLanguage, path='dialogTemplate', talkFile='sampleNotExist', fileType='.sample')

		# The Language file that the skill was written in
		file = Path(f'{self._translationPath}/dialogTemplate/{self._skillLanguage}.sample')
		# The file we are going to translate into
		translatedPath = Path(f'{self._translationPath}/dialogTemplate/{activeLanguage}.sample')
		sampleData = file.read_text()

		# create a new instance
		translatorSample = Translator()

		# do safe guard checks
		self.characterCountor(text=sampleData)
		self.requestLimitChecker()
		sampleCharacterCount = len(sampleData)
		if self._precheckTrigger == 1:
			self._sampleCount += sampleCharacterCount
		self._requestLimiter += 1
		self._requestTotal += 1

		# if ready to translate do this
		if not self.getConfig('preCheck'):
			# dont translate if charactor count is too large
			if sampleCharacterCount >= 14900:
				self.logWarning(self.randomTalk(text='doManually', replace=[sampleCharacterCount]))

			else:
				translated = translatorSample.translate(sampleData, dest=activeLanguage)
				fixedTranslationSyntax = translated.text.replace('«', '"').replace('„', '"')
				# write to file
				translatedPath.write_text(data=fixedTranslationSyntax)
		else:
			if self._developerUse:
				translatedPath.write_text(data=sampleData)

	def writeInstallConditions(self):
		self.logDebug(self.randomTalk(text='updateInstall'))
		# Lets update the install file language conditions
		file = Path(f'{self._translationPath}/{self._skillName}.install')
		installData = json.loads(file.read_text())

		for i, item in enumerate(installData['conditions']):
			if 'lang' in item:
				installData['conditions']['lang'] = self._supportedLanguages

				if not self.getConfig('preCheck'):
					file.write_text(json.dumps(installData, ensure_ascii=False, indent=4))
		self.endOfprocessing()


	def endOfprocessing(self):
		if not self.getConfig('preCheck'):
			self.logInfo(self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter]))
			self.say(
				text=self.randomTalk(text='sayCompleted', replace=[self._skillName, self._characterCounter])
			)

		if self.getConfig('preCheck'):
			# say to check syslog results
			self.say(
				text=self.randomTalk(text='preCheckResults'),
			)
			# the combined talk file character count
			totalTalk = self._talkDefaultCount + self._talkShortCount

			# delay warnings if quota will be exceeded
			if self._requestTotal > 550:
				self.logWarning(self.randomTalk(text='expectDelays'))
			if totalTalk >= 14900 or self._dialogCount >= 14900 or self._synonymCount >= 14900:
				self.logWarning(self.randomTalk(text='expectMajorDelays'))
			# results
			self.logInfo(self.randomTalk(text='resultsHeading', replace=[self._skillName]))
			self.logInfo(f'')
			self.logInfo(self.randomTalk(text='results1', replace=[totalTalk]))
			self.logInfo(self.randomTalk(text='results2', replace=[self._dialogCount]))
			self.logInfo(self.randomTalk(text='results3', replace=[self._synonymCount]))
			self.logInfo(self.randomTalk(text='results8', replace=[self._instructionCount]), )
			self.logInfo(self.randomTalk(text='results9', replace=[self._sampleCount]), )
			self.logInfo('')
			self.logInfo(self.randomTalk(text='results4', replace=[self._characterCounter]))
			self.logInfo(self.randomTalk(text='results5', replace=[self._requestTotal]))
			self.logInfo(self.randomTalk(text='results6'))
			self.logInfo('')
			self.logInfo(self.randomTalk(text='results7'))


	def translateInstructions(self, activeLanguage):
		if not Path(f'{self._translationPath}/instructions').exists():
			self.logInfo(self.randomTalk(text='skipInstructions'))
			return

		self.logDebug(self.randomTalk(text='translateInstructions', replace=[self._languageNames[activeLanguage]]), )

		# Check if we have all the language files. If not make them
		self.checkFileExists(activeLanguage=activeLanguage, path='instructions', talkFile='instructionsNotExist', fileType='.md')

		# The Language file that the skill was written in
		file = Path(f'{self._translationPath}/instructions/{self._skillLanguage}.md')
		# The file we are going to translate into
		translatedPath = Path(f'{self._translationPath}/instructions/{activeLanguage}.md')
		instructionData = file.read_text()

		# create a new instance
		translatorInstructions = Translator()

		# do safe guard checks
		self.characterCountor(text=instructionData)
		self.requestLimitChecker()
		instructionCharacterCount = len(instructionData)
		if self._precheckTrigger == 1:
			self._instructionCount += instructionCharacterCount
		self._requestLimiter += 1
		self._requestTotal += 1

		# if ready to translate do this
		if not self.getConfig('preCheck'):
			# dont translate if charactor count is too large
			if instructionCharacterCount >= 14900:
				self.logWarning(self.randomTalk(text='doManually', replace=[instructionCharacterCount]))

			else:
				translated = translatorInstructions.translate(text=instructionData, dest=activeLanguage)
				# remove known translated differences like white space in tags
				translatedInstructions: str = self.tidyUpInstructionTranslations(text=str(translated.text))
				# write to file
				translatedPath.write_text(data=translatedInstructions)
		else:
			dummyInstructions: str = self.tidyUpInstructionTranslations(text=str(instructionData))
			if self._developerUse:
				translatedPath.write_text(data=dummyInstructions)


	# Used to repair known issues with google translations. EG when they add unwanted whitespace
	@staticmethod
	def tidyUpInstructionTranslations(text: str):

		# todo i feel there's a smarter way to do this to make it more future friendly but yet to work it out
		newText = ""
		for position, line in enumerate(text.split("\n")):
			if '</ ' in line or 'color: # ' in line:
				modifiedLine = line.replace('</ ', '</').replace('color: # ', 'color: #')
				newText = f'{newText}\n{modifiedLine}'
			else:
				newText = f'{newText}\n{line}'

		return newText


	def requestLimitChecker(self):
		"""
		Used to prevent google blocking your Ip from exceeding 600
		 requests per minute
		"""
		seconds: float = 70
		# 600 is apparently the limit but was blocked at below 550
		# so have set the limit to 480 before triggering the 70 second timer
		if self._requestLimiter == 480:

			self.logWarning(self.randomTalk(text='breather', replace=[seconds]))
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
