<span style="color: #ff0000;"><strong>Instructions </span></strong>

So you've written a skill and want to translate it ? Good job, lets get into it then.

On this skill's settings..

##**skillLanguage field**

 Enter the language abbreviation that the skill was initially coded in. 
 
 - EG: de = German, it for Italian etc 

##**skillName** 

Enter the name of the directory of the skill you want to translate

 - EG: HomeAssistant or Reminder etc 
    
    NOTE: to test translation on this skillTranslator skill.... delete all or some of the dialog and talk language files that ARN'T "en.json"
     then leave the skillName field blank and ask alice to "translate my skill" she will translate 
     this SkillTranslator skill 
 
 ##**skillPath** (optional)
 
 Add the path to the directory of the skill manually. Exclude the skill name in this path but include
   it in- skillName 
 
 - EG: SkillPath field = C:/Documents/ProjectFiles/Skills
    and skillName field = Reminder  
    
NOTE: If this path is not set then it defaults to the Alice skills directory 

NOTE #2, Currently a manual path only looks at path's on the pi, not via a SSH directory on your desktop PC

Click Save

Then ask Alice "translate my skill"

and that's it :)
