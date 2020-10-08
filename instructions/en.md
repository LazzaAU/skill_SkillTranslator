<span style="color: #ff0000;"><strong>Instructions </span></strong>

So you've written a skill and want to translate it ? Good job, lets get into it then.

On this skill's settings..

##**skillLanguage field**

 Enter the language abbreviation that the skill was initially coded in. 
 
 - EG: de = German, it for Italian etc 

Note: there is a current bug that appears if you run translator skill more than once without restarting Alice.
For some reason yet known you will recieve a language error in this case. Please restart alice to fix the issue

##**skillTitle** 

Enter the name of the directory of the skill you want to translate.

 - EG: HomeAssistant or Reminder etc 
    
    NOTE: to test translation on this skillTranslator skill.... delete all or some of the dialog and talk language files that ARN'T "en.json"
     then leave the skillTitle field blank and ask alice to "translate my skill" she will translate 
     this SkillTranslator skill 
 
 ##**skillPath** (optional)
 
 Add the path to the directory of the skill manually. Exclude the skill name in this path but include
   it in- skillTitle 
 
 - EG: SkillPath field = C:/Documents/ProjectFiles/Skills
    and skillTitle field = Reminder  
    
NOTE: If this path is not set then it defaults to the Alice skills directory 

NOTE #2, Currently a manual path only looks at path's on the pi, not via a SSH directory on your desktop PC

**Click Save**

Then ask Alice to "translate my skill"

and that's it :)


##**preChecks**

The preeChecks button in the skill settings will allow you to analyze the files in the skill you want to translate.

It'll give feedback translation request count, character count etc so that you can make a informed decision
before trying to actually translate the file. It will also allow you to see if the process will be error free prior to sending requests to Google

If preCheck is enabled it will NOT overwrite or translate anything so it is Google friendly and won't change any files
Once happy turn it off and translate the skill.
