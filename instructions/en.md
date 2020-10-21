#<span style="color: #ff0000;"><strong>Instructions </span></strong>

So you've written a skill and want to translate it ? Good job, lets get into it then.

#<span style="color: #0000FF;"><strong>Quick operational steps</span></strong>

**To use this skill**

1. Go to the skill settings

2. Enter the name of the skill you want to translate in **skillTitle** field

3. Click Save

Ask alice to " translate my skill"

#<span style="color: #0000FF;"><strong>Skill Overview </span></strong>

- Precheck mode
 
This will run through the translation process without actually sending translation data to Google.
It's a dummy run that won't modify any files but give statistic feedback at the end of the process.

This mode uses the language file the skill was written in (set via...skill settings >> skillLanguage) to determine statistics on the translation process
prior to sending that data to Google. That way you can make a informed decision if 

1. there are errors in the files that will stop the translation process

2. The files are within Goggle's quota limits or over it's limits and therefore will trigger in built safe guards

Once run and it shows no errors, turn this mode off to run the skill in Translation mode


##**When run in translation mode :**

The skill will translate the talks directory first. If the requests being made to Google exceed the quota it will 
pause the code for 70 seconds (Pause the skill not Alice) then resume.

The skill will then translate the dialog file and do the same quota safe guards. (Note: If character count 
for one instance will likely exceed 1500 the code will pause for 1 hour)

During Dialog Template translation the code extracts the :=>Keyvalue} portion of the utterances
so that the keyValue doesnt get translated and stop the skill from working. It then put's that code backin
before writing it to file.

Once translated it will then add all 4 languages to the install file.

##**skillPath** field (optional)

- This is handy of you want to translate your skill files that are outside of the skills folder

  - **IE:**
 
    - If you're a skill dev and have a master copy you want to translate, rather than translate a active skill
that may have custom utterances etc in. 

Type the path **TO** the skill but **NOT** the skillname. (Use the skillTitle field for that)

EG: 

- skillPath = /home/pi/DevelopmentSkills
- skillTitle = HomeAssistant
.

##**SkillTitle** field (required)

This field denotes the skill you want to translate

- With this field filled and **NOT** the *skillPath* field as well then the path defaults to the ProjectAlice/skills folder
- With this field and skillPath field **NOT** filled in then you will translate this skill by default..
_
##**translateOnlyThis**

For this field...

- Empty = Will translate all required files (default)

- Enter one of the following to translate ONLY that folder (optional)
 - talks
 - dialog
 - instructions
 - Sample files
 
 _______________________

#Tips

Currently.. if you run the skill in one language and then run the skill in another language you may strike a error.
Restart Alice if you are switching the default languages between attempts.

- Side note:

 if you do happen to get this error consistently ..
 
 ```json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)```
 
 Then potentially, Goggle has just blocked your IP from translating files and you'll have to wait until the following midnight pacific time for it t to be unblocked  

------------------

Google translate tends to love adding whitespace where whitespace wasn't before. Although this skill trys to capture
some of these occasions you may find that when translating the instructions folder that if you have tags in the markdown
that you may have to manually take out some white spaces to have it display properly.

**What the skill won't do**

Currently the skill will not translate markdown files such as these instructions. That's a future feature to be added

NOTE: the accuracy of the translations is not guaranteed to be correct. We rely on google being able to also understand 
the context of the speech. After translation via this skill it will require manual verification from a @translator in
the discord channel
 
Enjoy translating 

 
