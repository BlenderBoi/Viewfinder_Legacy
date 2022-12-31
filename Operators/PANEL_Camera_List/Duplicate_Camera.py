




import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Duplicate_Camera(bpy.types.Operator):
    """Duplicate Camera"""
    bl_idname = "viewfinder.duplicate_camera"
    bl_label = "Duplicate Camera"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty()
    object: bpy.props.StringProperty()


    def invoke(self, context, event):
        self.name = self.object + "_Copy"
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")

    def execute(self, context):

        object = context.view_layer.objects.get(self.object)
        if object:
            duplicate_object = object.copy()
            duplicate_camera = object.data.copy()
            duplicate_object.data = duplicate_camera
            duplicate_camera.name = self.name
            duplicate_object.name = self.name
            collections = object.users_collection
            for collection in collections:
                collection.objects.link(duplicate_object)

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Duplicate_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
