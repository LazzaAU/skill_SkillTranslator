## Instructions

So you've written a skill and want to translate it ? Good job, lets get into it then.

## Quick operational steps

**To use this skill**

1. Go to the skill settings

2. Enter the name of the skill you want to translate in **skillTitle** field

3. Click Save

Ask alice to " translate my skill"

## Skill Overview

- Precheck mode
 
This will run through the translation process without actually sending translation data to Google.
It's a dummy run that won't modify any files but give statistic feedback at the end of the process.

This mode uses the language file the skill was written in (set via...skill settings >> skillLanguage) to determine statistics on the translation process
prior to sending that data to Google. That way you can make an informed decision if 

1. There are errors in the files that will stop the translation process

2. The files are within Goggle's quota limits or over its limits and therefore will trigger in built safeguards

Once run, and it shows no errors, turn this mode off to run the skill in Translation mode


## **When run in translation mode :**

The skill will translate the talks directory first. If the requests being made to Google exceed the quota it will 
pause the code for 70 seconds (Pause the skill not Alice) then resume.

The skill will then translate the dialog file and do the same quota safeguards. (Note: If character count 
for one instance will likely exceed 1500 the code will pause for 1 hour)

During Dialog Template translation the code extracts the :=>Keyvalue} portion of the utterances
so that the keyValue doesn't get translated and stop the skill from working. It then puts that code back in
before writing it to file.

Once translated it will then add all translated languages to the install-file.

## **skillPath** field (optional)

- This is handy if you want to translate your skill files that are out-side of the skills folder

  - **IE:**
 
    - If you're a skill dev and have a master copy you want to translate, rather than translate an active skill
that may have custom utterances etc. in it. 

Type the path **TO** the skill, but **NOT** the skillname. (Use the skillTitle field for that)

EG: 

- skillPath = /home/pi/DevelopmentSkills
- skillTitle = HomeAssistant
.

## **SkillTitle** field (required)

This field denotes the skill you want to translate

- With this field filled and **NOT** the *skillPath* field as well, then the path defaults to the ProjectAlice/skills folder
- With this field and skillPath field **NOT** filled in then you will translate this skill by default.
_
## **translateOnlyThis**

For this field...

- Empty = Will translate all required files (default)

- Enter one of the following to translate ONLY that folder (optional)
 - talks
 - dialog
 - instructions
 - Sample files

## **ignoreLanguages**

Let's say you know that german and French translation has been done manually by a @translator in discord.
so you want to translate your skill but exclude the german and French translation. Well you can do that with the

**ignoreLanguages** field. In the above senario you would just enter into that field
```de, fr```

Please note: seperate languages with a comma
 _______________________

## Tips

Currently, if you run the skill in one language and then run the skill in another language you may strike an error.
Restart Alice if you are switching the default languages between attempts.

- Side note:

 if you do happen to get this error consistently ..
 
 ```json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)```
 
 Then potentially, Goggle has just blocked your IP from translating files, and you'll have to wait until the following 
 midnight pacific time for it to be unblocked  

------------------

Google Translate tends to love adding whitespace where whitespace wasn't before. Although this skill trys to capture
some of these occasions you may find that when translating the instructions folder that if you have tags in the markdown
that you may have to manually take out some white spaces to have it display properly.
Alice currently doesn't like tags in the instruction file, so refrain from using them if you can.


NOTE: The accuracy of the translations is not guaranteed to be correct. We rely on Google being able to also understand 
the context of the speech. After translation via this skill it will require manual verification from a @translator in
the discord channel
 
Enjoy translating 

 
