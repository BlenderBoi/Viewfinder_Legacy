
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math


class VIEWFINDER_Selected_Camera_To_View(bpy.types.Operator):
    """Selected Camera To View"""
    bl_idname = "viewfinder.selected_camera_to_view"
    bl_label = "Selected Camera to View"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):


        if context.space_data.region_3d.view_perspective == 'PERSP':
            cameras = [object for object in context.selected_objects if object.type == "CAMERA"]
            previous_cam = context.scene.camera

            for camera in cameras:

                context.scene.camera = camera
                bpy.ops.view3d.camera_to_view()
                context.space_data.region_3d.view_perspective = 'PERSP'
            
            context.scene.camera = previous_cam

        # col.operator("view3d.camera_to_view_selected", text="Frame Selected Objects", icon="MESH_PLANE")
        # col.operator("view3d.camera_to_view", text="Camera To View", icon="CAMERA_DATA")

        # scn = context.scene
        # object = context.view_layer.objects.get(self.object)
        # scn_properties = scn.Viewfinder_Scene_Properties

        # if object:
        #     Object_Properties = object.Viewfinder_Object_Properties

        #     if scn_properties.Set_Resolution:
        #         if Object_Properties:
        #             if Object_Properties.Use_Resolution:
        #                 context.scene.render.resolution_x = Object_Properties.Resolution_X
        #                 context.scene.render.resolution_y = Object_Properties.Resolution_Y

        #     context.scene.camera = object
        #     context.space_data.region_3d.view_perspective = 'CAMERA'
        




        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Selected_Camera_To_View]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()



