




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Add_Camera_Marker(bpy.types.Operator):
    """Add Camera Marker"""
    bl_idname = "viewfinder.add_camera_marker"
    bl_label = "Add Marker"
    bl_options = {'UNDO', 'REGISTER'}

    object: bpy.props.StringProperty()
    frame: bpy.props.IntProperty()


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "frame", text="Frame")

    def invoke(self, context, event):

        self.frame = context.scene.frame_current

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        if object:
            marker = context.scene.timeline_markers.new(object.name, frame=self.frame)
            marker.camera = object

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Add_Camera_Marker]

def register():
  for cls in classes:

    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
