




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Find_Camera(bpy.types.Operator):
    """Find Camera"""
    bl_idname = "viewfinder.find_camera"
    bl_label = "Find Camera"
    bl_options = {'UNDO', 'REGISTER'}

    object: bpy.props.StringProperty()


    @classmethod
    def poll(cls, context):

        return context.mode in ["OBJECT"]


    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        if object:
            bpy.ops.object.select_all(action='DESELECT')
            object.select_set(True)
            context.view_layer.objects.active = object
            bpy.ops.view3d.view_selected(use_all_regions=False)

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Find_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
