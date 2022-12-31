




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Select_Camera(bpy.types.Operator):
    """Select Camera"""
    bl_idname = "viewfinder.select_camera"
    bl_label = "Select Camera"
    bl_options = {'UNDO', 'REGISTER'}


    object: bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):

        return context.mode in ["OBJECT"]



    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        bpy.ops.object.select_all(action='DESELECT')

        if object:
            object.select_set(True)
            context.view_layer.objects.active = object

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Select_Camera]

def register():
  for cls in classes:

    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
