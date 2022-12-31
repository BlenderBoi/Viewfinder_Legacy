




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Remove_Camera(bpy.types.Operator):
    """Remove Camera"""
    bl_idname = "viewfinder.remove_camera"
    bl_label = "Select Camera"
    bl_options = {'UNDO', 'REGISTER'}


    object: bpy.props.StringProperty()



    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        if object:
            bpy.data.objects.remove(object)


        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Remove_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
