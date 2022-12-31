




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_View_Camera(bpy.types.Operator):
    """View Camera"""
    bl_idname = "viewfinder.view_camera"
    bl_label = "Select Camera"
    bl_options = {'UNDO', 'REGISTER'}


    object: bpy.props.StringProperty()



    def execute(self, context):

        scn = context.scene
        object = context.view_layer.objects.get(self.object)
        scn_properties = scn.Viewfinder_Scene_Properties

        if object:
            Object_Properties = object.Viewfinder_Object_Properties

            if scn_properties.Set_Resolution:
                if Object_Properties:
                    if Object_Properties.Use_Resolution:
                        context.scene.render.resolution_x = Object_Properties.Resolution_X
                        context.scene.render.resolution_y = Object_Properties.Resolution_Y

            context.scene.camera = object
            context.space_data.region_3d.view_perspective = 'CAMERA'

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_View_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
