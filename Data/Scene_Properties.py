import bpy
from Viewfinder import Utility_Functions

import os
import pathlib



def POLL_Camera(self, object):
    if object.type == "CAMERA":
        if bpy.context.view_layer.objects.get(object.name):
            return True


ENUM_Filter_Camera_List = [("SCENE","Scene Camera","Scene Camera"), ("ACTIVE","Active Camera","Active Camera"), None, ("SELECTED","Selected Camera","Selected Camera"),("ALL","All Camera","All Camera")]


ENUM_Camera_Preview_Target = [("ACTIVE","Active","Active"),("SCENE","Scene","Scene"), ("PICK", "Pick", "Pick")]




class Viewfinder_SCENE_Properties(bpy.types.PropertyGroup):

    Camera_Picker: bpy.props.PointerProperty(type=bpy.types.Object, poll=POLL_Camera)
    FILTER_Camera_List: bpy.props.EnumProperty(items=ENUM_Filter_Camera_List, default="ALL")

    Set_Resolution: bpy.props.BoolProperty(default=False)


    Align_Cam_Use_Orthographic: bpy.props.BoolProperty(default=False)

    FILTER_Name: bpy.props.StringProperty(default="",options={'TEXTEDIT_UPDATE'})






classes = [Viewfinder_SCENE_Properties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.Viewfinder_Scene_Properties = bpy.props.PointerProperty(type=Viewfinder_SCENE_Properties)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.Viewfinder_Scene_Properties
