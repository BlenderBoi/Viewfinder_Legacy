
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils


class VIEWFINDER_Create_Markers_From_Selected_Camera(bpy.types.Operator):
    """Create Markers From Selected Camera"""
    bl_idname = "viewfinder.create_markers_from_selected_camera"
    bl_label = "Create Markers From Selected Camera"
    bl_options = {'UNDO', 'REGISTER'}

    frame_increment: bpy.props.BoolProperty(name="Frame Increment", default=True)

    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        selected_camera_objects = Utility_Functions.get_selected_object_type(context, ["CAMERA"])

        frame = context.scene.frame_current

        for index, object in enumerate(selected_camera_objects):

            marker = scn.timeline_markers.new(object.name, frame=context.scene.frame_current+index)
            marker.camera = object



        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Markers_From_Selected_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
