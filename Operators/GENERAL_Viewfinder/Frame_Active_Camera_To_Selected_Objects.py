
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math



class VIEWFINDER_Frame_Active_Camera_To_Selected_Objects(bpy.types.Operator):
    """Selected Camera To Selected Objects"""
    bl_idname = "viewfinder.frame_active_camera_to_selected_objects"
    bl_label = "Frame Active Camera To Selected Objects"
    bl_options = {'UNDO', 'REGISTER'}




    def execute(self, context):


        cameras = [cam for cam in context.selected_objects if cam.type == "CAMERA"]

        for cam in cameras:
            cam.select_set(False)


        previous_cam = context.scene.camera

        for cam in cameras:
            
            context.scene.camera = cam
            bpy.ops.view3d.camera_to_view_selected()
            cam.select_set(True)
        

        context.scene.camera = previous_cam



        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Frame_Active_Camera_To_Selected_Objects]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()



