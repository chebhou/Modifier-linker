# Modifier-linker
Blender Addon for linking modifiers

The addon creates a link between modifiers from defferent objects, allowing to share the same modifier across multiple objects and having  the control from one master object.
Each object can have multiple links ( one per modifier ) to different objects.
The Modifiers can be appdated on diffeerent events ( using bpy.app.handlers ) to adapte to the current usage.<br>
The user can :
 - Create new links 
 - Remove a link or all at once
 - Disable/enable induvidual links
 - Set the update event for each object
 - Disable all objects links at once
 - Change all objects update event to a certain event
 - Copy links from active to selected objects

 

Known Issues :
 - the continues update will cause the render in viewport never stop, a work around is to unlink all objects or change the update event to frame_change

TODO :
 - still working on it
