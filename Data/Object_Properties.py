import bpy
from Viewfinder import Utility_Functions




class Viewfinder_OBJECT_Properties(bpy.types.PropertyGroup):

    SHOW_Camera_Data_Options: bpy.props.BoolProperty(default=False)
    SHOW_Display_Options: bpy.props.BoolProperty(default=False)
    SHOW_Sensor_Options: bpy.props.BoolProperty(default=False)
    SHOW_DOF_Options: bpy.props.BoolProperty(default=False)

    Use_Resolution: bpy.props.BoolProperty(default=False)
    Resolution_X: bpy.props.IntProperty(default=1920)
    Resolution_Y: bpy.props.IntProperty(default=1080)

classes = [Viewfinder_OBJECT_Properties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Object.Viewfinder_Object_Properties = bpy.props.PointerProperty(type=Viewfinder_OBJECT_Properties)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.Viewfinder_Object_Properties
