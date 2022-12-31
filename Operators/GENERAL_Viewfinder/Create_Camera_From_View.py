
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils



class VIEWFINDER_Create_Camera_From_View(bpy.types.Operator):
    """Create Camera From View"""
    bl_idname = "viewfinder.create_camera_from_view"
    bl_label = "Create Camera From View"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="Camera")
    Dolly: bpy.props.FloatProperty(default=0.0)
    Create_Camera_Marker: bpy.props.BoolProperty(default=False)
    Frame_Selected: bpy.props.BoolProperty(default=False)####

    Add_To_Still_List: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        if context.space_data.region_3d.view_perspective == "ORTHO":

            context.space_data.region_3d.view_perspective = "PERSP"
            context.space_data.region_3d.update()
            self.view_matrix = context.space_data.region_3d.view_matrix.copy()
            context.space_data.region_3d.view_perspective = "ORTHO"
            context.space_data.region_3d.update()
            self.view_perspective = context.space_data.region_3d.view_perspective

            context.space_data.region_3d.view_camera_zoom = 0
            context.space_data.region_3d.view_camera_offset = (0,0)


        else:

            self.view_matrix = context.space_data.region_3d.view_matrix.copy()
            self.view_perspective = context.space_data.region_3d.view_perspective

            context.space_data.region_3d.view_camera_zoom = 0
            context.space_data.region_3d.view_camera_offset = (0,0)



        self.Dolly = 0

        return context.window_manager.invoke_props_dialog(self)

        # return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "Dolly", text="Dolly Camera")
        layout.prop(self, "Create_Camera_Marker", text="Camera Markers at Current Frame")
        # layout.prop(self, "Add_To_Still_List", text="Add to Render Still List")



    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        if context.space_data.type == "VIEW_3D":


            camera = bpy.data.cameras.new(self.name)
            object = bpy.data.objects.new(self.name, camera)
            context.collection.objects.link(object)

            if self.view_perspective == "PERSP":
                object.data.type = "PERSP"
            if self.view_perspective == "ORTHO":
                object.data.type = "ORTHO"

            if object:
                scn.camera = object
                object.select_set(True)
                context.view_layer.objects.active = object

                object.data.lens = context.space_data.lens
                object.matrix_world = self.view_matrix
                object.matrix_world.invert()
                object.data.clip_start = context.space_data.clip_start
                object.data.clip_end = context.space_data.clip_end

                rotationMAT = mathutils.Euler(object.rotation_euler).to_matrix()
                rotationMAT.invert()
                zVector = mathutils.Vector((0, 0, self.Dolly)) @ rotationMAT
                object.location = object.location + zVector

                context.space_data.region_3d.view_perspective = 'CAMERA'

                if self.Add_To_Still_List:

                    Scene_Properties = context.scene.Viewfinder_Scene_Properties
                    item_list = Scene_Properties.Still_Render_List


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










                if self.Create_Camera_Marker:
                    marker = context.scene.timeline_markers.new(object.name)
                    marker.camera = object
                    marker.frame = context.scene.frame_current

        context.view_layer.update()





        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Camera_From_View]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
