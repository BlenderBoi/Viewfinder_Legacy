import bpy
from Viewfinder import Utility_Functions
import os

class VIEWFINDER_Add_Camera_To_Still_List(bpy.types.Operator):
    """Add Camera to Still List"""
    bl_idname = "viewfinder.add_camera_to_still_list"
    bl_label = "Add Camera To Still List"
    bl_options = {'UNDO', 'REGISTER'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        scn = context.scene

        Scene_Properties = scn.Viewfinder_Scene_Properties
        item_list = Scene_Properties.Still_Render_List

        object = context.view_layer.objects.get(self.object)


        if object:

            item = item_list.add()
            item.name = object.name


            item.frame = context.scene.frame_current

            item.render_at_frame = False

            item.resolution_custom_x = context.scene.render.resolution_x
            item.resolution_custom_y = context.scene.render.resolution_y
            item.camera = object

            item.film_transparent = context.scene.render.film_transparent

            item.use_compositing = context.scene.render.use_compositing
            item.use_sequencer = context.scene.render.use_sequencer

            item.output_path = os.path.join(context.scene.render.filepath, object.name)


            if context.scene.render.engine == "BLENDER_EEVEE":
                item.engine = "EEVEE"
            if context.scene.render.engine == "CYCLES":
                item.engine = "CYCLES"
            if context.scene.render.engine == "BLENDER_WORKBENCH":
                item.engine = "WORKBENCH"

        Scene_Properties.Still_Render_List_Index = len(item_list) - 1

        Utility_Functions.update_UI()
        return {'FINISHED'}



classes = [VIEWFINDER_Add_Camera_To_Still_List]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
