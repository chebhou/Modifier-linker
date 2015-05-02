# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "Modifiers Linker",
    "author": "Chebhou",
    "version": (1, 0),
    "blender": (2, 74, 0),
    "location": "Tools Shelf > M-L",
    "description": "Link modifiers between objects",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty, IntProperty, EnumProperty, StringProperty, CollectionProperty
from bpy.types import Operator, Panel


"""   **********************************   Costum properties section  **************************************** """

# update functions for the link properties
def check_link(self, value):
      
      obj = self.id_data
      name = self.name
      source = self.source
      scene = bpy.context.scene
      # there should be a modifier with this name
      if name == "" or not obj.modifiers[name]:
          print(" no modifier found : "+name)
          self.linked = False
      elif source == "" or not scene.objects[source]:
          print(" no object found : "+source)
          self.linked = False

def check_name(self, value):
      
      obj = self.id_data
      # there should be a modifier with this name
      if value == "" or not obj.modifiers[value]:
          self.linked = False

def check_source(self, value):
      
      scene = bpy.context.scene
      # there should be an object with this name
      if value == "" or not scene.objects[value]:
          self.linked = False


# Class that holds one modifier link 
class modifier_link(bpy.types.PropertyGroup):
    # modifiers name should be a dynamic list of all available modifiers
    # if the source is empty set the link to false
    name  = StringProperty(name="name", default="")#, set = check_name # it's handled by the UI
    # the index of the link according to the object
    index = IntProperty(name="index", default=0 )
    # the source of this modifier settings
    source = StringProperty(name="source", default="") #, set = check_source # it's handled by the UI
    # link state, if the link has been anabled the source and name shouldn't be empty
    linked = BoolProperty(name="linked", default=False, update = check_link)
    


#holds all modifiers' links and the update event property for this object

def update_obj_list(self,context):
      print(self.update_event, self.linked)
      obj = self.id_data
      in_list = context.scene.linked_objects.count(context.object.name)
      if (self.update_event == 'None' or  not self.linked ) and in_list :
          context.scene.linked_objects.remove(obj.name)
      elif self.update_event != 'None' and self.linked and not in_list :
          context.scene.linked_objects.append(obj.name)


class modifiers_link(bpy.types.PropertyGroup):
      links = CollectionProperty(type=modifier_link)
      linked = BoolProperty(name="linked", default=False, update = update_obj_list)
      update_event    = EnumProperty(
                        name="update_event",
                        description="Choose update event",
                        items=(('frame_post', "after frame change", "update modifiers after frame change"),
                               ('frame_pre', "Before frame change", "update modifiers Before frame change"),
                               ('scene_post', "After scene update", "update modifiers After scene update"),
                               ('scene_pre', "Before scene update", "update modifiers Before scene update"),
                               ('None', "No update", "update is canceled")),
                        default='None',
                        update = update_obj_list
                        )
 

# some function to setup the links
def clear_links(self):
      self.modifiers_link.links.clear()

def clear_update(self):
      self.modifiers_link.update_event = 'None'

      


"""   *****************************************  Operators Section  ****************************************** """

class AddLink(bpy.types.Operator):
    """add a modifier link to the active object"""
    bl_idname = "links.add_link"
    bl_label = "Add Modifier Link"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        new_link = context.active_object.modifiers_link.links.add()
        new_link.index = len(context.active_object.modifiers_link.links)-1
        return {'FINISHED'}


class RemoveLink(bpy.types.Operator):
    """remove a modifier link from the active object"""
    bl_idname = "links.remove_link"
    bl_label = "Remove Modifier Link"

    link_index = IntProperty()
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        links = context.active_object.modifiers_link.links
        for i in range(0,len(links)) :
            print(links[i].index,self.link_index)
            if links[i].index == self.link_index :
                links.remove(i)
                break
        return {'FINISHED'}


class ClearLinks(bpy.types.Operator):
    """remove all modifier links from the active object"""
    bl_idname = "links.clear_links"
    bl_label = "clear all Modifier Link"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        context.active_object.clear_links()
        return {'FINISHED'}


class ClearLinkUpdate(bpy.types.Operator):
    """set modifier links update to None"""
    bl_idname = "links.clear_update"
    bl_label = "clear all objects update event"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        list = context.scene.linked_objects.copy()
        for name in list :
            print(name)
            obj = context.scene.objects.get(name, None)
            if obj :
                print(obj)
                obj.clear_update()
                
        context.scene.linked_objects.clear()
        return {'FINISHED'}

class UnlinkAll(bpy.types.Operator):
    """set modifier links to Unlinked"""
    bl_idname = "links.unlink_all"
    bl_label = "clear all objects linked flag"
    
    unlink = BoolProperty(default = False)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for obj in context.scene.objects :
            obj.modifiers_link.linked = self.unlink
        return {'FINISHED'}
    
class CopyToSelcted(bpy.types.Operator):
    """copy modifier links to selected objects"""
    bl_idname = "links.copy_to_selected"
    bl_label = "Copy Modifier Links to selected"
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        source = context.active_object

        for obj in context.selected_objects :
          if obj != source :
             obj.clear_links()
             for link in source.modifiers_link.links :
                new_link = obj.modifiers_link.links.add()
                new_link.name = link.name
                new_link.source = link.source
                new_link.index = link.index
                new_link.linked = link.linked
          obj.modifiers_link.update_event = source.modifiers_link.update_event

          return {'FINISHED'}


class RefreshlinkedList(bpy.types.Operator):
    """refresh the linked objects list"""
    bl_idname = "links.refresh_linked_list"
    bl_label = "refresh the linked objects list"
    
    @classmethod
    def poll(cls, context):
        return context.scene is not None

    def execute(self, context):

        for obj in context.scene.objects :
            in_list = context.scene.linked_objects.count(obj.name)
            links = obj.modifiers_link
            if (links.update_event == 'None' or  not links.linked ) and in_list :
                context.scene.linked_objects.remove(obj.name)
            elif links.update_event != 'None' and links.linked and not in_list :
                context.scene.linked_objects.append(obj.name)

        return {'FINISHED'}



"""   *****************************************  Handlers section   ****************************************** """

# copy
def copy_modifier(obj, source, name):
        """ Copy one modifier from the source to obj """

        mDst = obj.modifiers.get(name, None)
        mSrc = source.modifiers.get(name, None)

        if mSrc :
          if not mDst:
              mDst = obj.modifiers.new(name, mSrc.type)
                
          # collect names of writeable properties
          properties = [p.identifier for p in mSrc.bl_rna.properties
                        if not p.is_readonly]

          # copy those properties
          for prop in properties:
              if getattr(mDst, prop) != getattr(mSrc, prop) :
                  setattr(mDst, prop, getattr(mSrc, prop))
          return True
        return False



# handlers functions

# Main update function called by all handlers
def update_func(scene, handler):
    """ Update the linked modifiers for all objects """

    #scene = bpy.data.scenes[0]
    objects = scene.objects
    lobjects = [o for o in objects if scene.linked_objects.count(o.name) and o.modifiers_link.update_event == handler ]
     
    for obj in lobjects :
        for link in obj.modifiers_link.links :
            source = objects.get(link.source, None)
            name   = link.name

            if source and link.linked :
                copy_modifier(obj, source, name)

# handler functions seperated to know the running handler
def update_on_f_pr(scene):

    handler = 'frame_pre'
    update_func(scene, handler)

def update_on_f_po(scene):

    handler = 'frame_post'
    update_func(scene, handler)

def update_on_s_pr(scene):

    handler = 'scene_pre'
    update_func(scene, handler)

def update_on_s_po(scene):

    handler = 'scene_post'
    update_func(scene, handler)
              


"""   ********************************************  UI Section   ********************************************** """

class Ml3DPanel(bpy.types.Panel):
    ''' Panel to manipuplate parameters of modifiers links '''

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "modifiers\' links " 
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = 'M-L'

    def draw(self, context):

        obj = context.object

        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.label(text="Active object \"" + obj.name + "\" options :")
        row = box.row()
        row.prop(obj.modifiers_link, 'update_event', text ='Update event')
        row = box.row()
        row.prop(obj.modifiers_link, 'linked', text='linked', toggle=True, icon='LINKED')
        row = box.row()
        row.operator("links.clear_links", text="Delete all links", icon='X', emboss=True)
        
        box = layout.box()
        row = box.row(align=True)
        row.label(text ="All objects options :")
        row = box.row(align=True)
        row.operator("links.unlink_all", text="Unlink all objects", icon='UNLINKED', emboss=True).unlink = False
        row.operator("links.unlink_all", text="link all objects", icon='LINKED', emboss=True).unlink = True
        row = box.row(align=True)
        row.operator("links.clear_update", text="Clear all apdates", icon='X', emboss=True)
        row.operator("links.refresh_linked_list", text="Refresh All links", icon='FILE_TICK', emboss=True)
        row = box.row(align=True)
        row.operator("links.copy_to_selected", text="Copy to selected", icon='PASTEDOWN', emboss=True)
        # To do   #maybe make it a property
        #row.operator("links.skip_common", text="Skip hide/show options")


        # labels creating some kind of a table header
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        row.label(text="", icon='GRIP')
        row.scale_y = 0.5


        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="linked modifiers list")

        row = layout.row(align=True)
        row.label(text="Modifier", icon='MODIFIER')
        row.label(text="Object", icon='OBJECT_DATAMODE')
        row.label(text="Link", icon='LINKED')
        row.label(text="Delete", icon='X')

        
        for link in obj.modifiers_link.links:
              #box = layout.box()
              row = layout.row(align=True)
              #row.prop(link, 'name', text='modifier')
              row.prop_search(link, 'name', obj, "modifiers",text = '',icon='MODIFIER')

              #row.prop(link, 'source', text=' settings source')
              row.prop_search(link, 'source', context.scene, "objects",text = '')

              row.prop(link, 'linked', text='linked', toggle=True, icon='LINKED')

              op = row.operator("links.remove_link", text="Remove", icon='X')
              op.link_index = link.index

        row = layout.row()
        row.operator("links.add_link", text="Add new Link", icon='PLUS', emboss=True)
        
        

"""************************************** Registration ************************************"""

def register():
    # register classes
    bpy.utils.register_module(__name__)
    # add the modifiers_link prop to Object type
    bpy.types.Object.modifiers_link  = bpy.props.PointerProperty(type=modifiers_link)
    bpy.types.Object.clear_links  = clear_links
    bpy.types.Object.clear_update  = clear_update
    bpy.types.Scene.linked_objects = []
    #append the update func to the handlers
    bpy.app.handlers.frame_change_pre.append(update_on_f_pr)
    bpy.app.handlers.frame_change_post.append(update_on_f_po)
    bpy.app.handlers.scene_update_pre.append(update_on_s_pr)
    bpy.app.handlers.scene_update_post.append(update_on_s_po)


def unregister():
    # add the modifiers_link prop to Object type
    del  bpy.types.Object.modifiers_link  
    del  bpy.types.Object.clear_links  
    del  bpy.types.Object.clear_update  
    del  bpy.types.Scene.linked_objects 
    # unregister classes
    bpy.utils.unregister_module(__name__)
    # append the update func to the handlers
    bpy.app.handlers.frame_change_pre.remove(update_on_f_pr)
    bpy.app.handlers.frame_change_post.remove(update_on_f_po)
    bpy.app.handlers.scene_update_pre.remove(update_on_s_pr)
    bpy.app.handlers.scene_update_post.remove(update_on_s_po)


if __name__ == "__main__":
    register()

