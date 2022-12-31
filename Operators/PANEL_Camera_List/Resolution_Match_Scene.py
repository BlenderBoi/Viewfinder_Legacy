




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Resolution_Match_Scene(bpy.types.Operator):
    """Resolution Match Scene"""
    bl_idname = "viewfinder.resolution_match_scene"
    bl_label = "Resolution Match Scene"
    bl_options = {'UNDO', 'REGISTER'}


    object: bpy.props.StringProperty()

    def execute(self, context):

        scn = context.scene
        object = context.view_layer.objects.get(self.object)

        if object:
            Object_Properties = object.Viewfinder_Object_Properties

            if Object_Properties:

                Object_Properties.Resolution_X = context.scene.render.resolution_x
                Object_Properties.Resolution_Y = context.scene.render.resolution_y



        return {'FINISHED'}



classes = [VIEWFINDER_Resolution_Match_Scene]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
