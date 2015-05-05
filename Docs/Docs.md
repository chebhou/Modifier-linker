#Modifier Linker

###Table of Contents
 * [Install](#install)
 * [How to use](#how-to-use)
 
##Install

1. Begin by downloading the file form this repo
2. Open blender and use <kbd>Ctrl</kbd>-<kbd>Alt</kbd>-<kbd>U</kbd> to open the user preferences.
3. Navigate to the addons tab
4. Hit install from file:<br>
![Image](http://i.stack.imgur.com/Ob676m.jpg)

##How to use 

![Image](http://i.stack.imgur.com/pBTkr.png)



###The update event :
 - for an interactive linking ( the link updates when you work in the 3D view ) you can choose either "Before scene update" or "After scene update" 
 - while if you want the linking to happen during animation you can choose between "Before frame update" or "After frame update" 
 - the "No update" option will simply disable updating all object's links 

###Linked :
this will enable or disable all links of this object meaning the object modifiers' links will not be updated ( this is used to swich on and off al links at the same time )

###Delete all links :
this will remove all modifiers' links on this object 

###Unlink all objects :
disable "linked" option of all objects meaning all object will not be updated 

###link all objects :
enable the "Link" option of all objects , this doesn't mean all objects will be updated [(see why)](###when-the-object-gets-updated-:)

###Clear all updates :
set all update events of all objects to "no update" so no object link get updated

###Refresh all links :
in case some links are malfunctioning clcick this to refresh all links ( it's not a reset button ) 

###Copy to selected :
copy links from the active object to all selected objects 

###Modifer links list :
a modifier link has three properties :

 * ###Modifier :
   the name of the modifier to copy fromm the settings ( the name of the modifiers should be the same on this object and the source object for the link to work )

 * ###Object :
   the source from which we copy from the modifier parameters 

 * ###Linked :
   activate and disactivate this link ( this gets overridden by the "Linked" property of the object ), you can't turn this ON unless you have entered a valid Object name and Modifier name 


###Remove :
remove this link

###Add a link :
add new link

----

###when the object gets updated :

 - the object "Linked" property should be ON
 - the object "update event"  should not be "No update"
 - the link  "Linked" propety should be ON
 - the link  "Object" should be on the same scene
