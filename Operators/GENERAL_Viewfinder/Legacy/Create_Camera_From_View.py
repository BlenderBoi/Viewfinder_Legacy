
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils

ENUM_Constraint = [("TRACK_TO","Track To","Track To"),("DAMPED_TRACK","Damped Track","Damped Track")]

class VIEWFINDER_Create_Camera_From_View(bpy.types.Operator):
    """Create Camera From View"""
    bl_idname = "viewfinder.create_camera_from_view"
    bl_label = "Create Camera From View"
    bl_options = {'UNDO', 'REGISTER'}
    # bl_options = {'UNDO'}

    name: bpy.props.StringProperty(default="Camera")
    create_target: bpy.props.BoolProperty(default=False)
    Empty_Distance: bpy.props.FloatProperty(default=5.0)
    Constraint: bpy.props.EnumProperty(items=ENUM_Constraint)

    View_Camera: bpy.props.BoolProperty(default=True)
    Lock_Camera_To_View: bpy.props.BoolProperty(default=False)
    zoom_camera_1_to_1: bpy.props.BoolProperty(default=False)

    Dolly: bpy.props.FloatProperty(default=0.0)


    def invoke(self, context, event):

        if context.space_data.region_3d.view_perspective == "ORTHO":

            context.space_data.region_3d.view_perspective = "PERSP"
            context.space_data.region_3d.update()
            self.view_matrix = context.space_data.region_3d.view_matrix.copy()
            context.space_data.region_3d.view_perspective = "ORTHO"
            context.space_data.region_3d.update()
            self.view_perspective = context.space_data.region_3d.view_perspective
        else:

            self.view_matrix = context.space_data.region_3d.view_matrix.copy()
            self.view_perspective = context.space_data.region_3d.view_perspective


        self.Dolly = 0



        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "create_target", text="Create Target")
        layout.prop(self, "View_Camera", text="View Camera")
        layout.prop(self, "Dolly", text="Dolly Camera")


        if self.View_Camera:
            layout.prop(self, "Lock_Camera_To_View", text="Lock Camera to View")
            # layout.prop(self, "zoom_camera_1_to_1", text="Zoom Camera to 1 to 1")
        if self.create_target:
            layout.prop(self, "Constraint", text="Constraint", expand=True)
            layout.prop(self, "Empty_Distance", text="Empty Distance")


    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None


        # if self.view_perspective == "CAMERA":
        #     if scn.camera:
        #         object = scn.camera.copy()
        #         object.name = self.name
        #         context.collection.objects.link(object)
        #     else:
        #         camera = bpy.data.cameras.new(self.name)
        #         object = bpy.data.objects.new(self.name, camera)
        #         context.collection.objects.link(object)
        # else:
        #     camera = bpy.data.cameras.new(self.name)
        #     object = bpy.data.objects.new(self.name, camera)
        #     context.collection.objects.link(object)

        if context.space_data.type == "VIEW_3D":

            camera = bpy.data.cameras.new(self.name)
            object = bpy.data.objects.new(self.name, camera)
            context.collection.objects.link(object)

            if object:
                scn.camera = object
                object.select_set(True)
                context.view_layer.objects.active = object

                if self.view_perspective == "PERSP":
                    object.data.type = "PERSP"
                if self.view_perspective == "ORTHO":
                    object.data.type = "ORTHO"



                object.data.lens = context.space_data.lens
                object.matrix_world = self.view_matrix
                object.matrix_world.invert()
                object.data.clip_start = context.space_data.clip_start
                object.data.clip_end = context.space_data.clip_end

                rotationMAT = mathutils.Euler(object.rotation_euler).to_matrix()
                rotationMAT.invert()
                zVector = mathutils.Vector((0, 0, self.Dolly)) @ rotationMAT
                object.location = object.location + zVector



                # if self.view_perspective == "ORTHO":
                #
                #     object.data.type = "ORTHO"
                #     object.data.lens = context.space_data.lens
                #     object.matrix_world = self.view_matrix
                #     object.matrix_world.invert()
                #
                #     rotationMAT = mathutils.Euler(object.rotation_euler).to_matrix()
                #     rotationMAT.invert()
                #     zVector = mathutils.Vector((0, 0, self.Dolly)) @ rotationMAT
                #     object.location = object.location + zVector
                #
                #
                #     object.data.clip_start = context.space_data.clip_start
                #     object.data.clip_end = context.space_data.clip_end



                # if scn.camera:
                #     context.space_data.region_3d.view_perspective = 'CAMERA'

                if self.create_target:
                    empty = Utility_Functions.Create_Empty("TGT_" + self.name)

                    empty.select_set(True)
                    object.select_set(True)

                    empty.matrix_world = object.matrix_world
                    empty.location = object.matrix_world @ mathutils.Vector((0, 0, -self.Empty_Distance))


                    context.view_layer.objects.active = empty

                    constraint = object.constraints.new(self.Constraint)
                    constraint.target = empty
                    constraint.track_axis = "TRACK_NEGATIVE_Z"

        context.view_layer.update()

        # if self.View_Camera:
        #
        #     context.space_data.region_3d.view_perspective = 'CAMERA'
        #     # bpy.ops.view3d.view_camera()
        #     if self.zoom_camera_1_to_1:
        #         bpy.ops.view3d.zoom_camera_1_to_1()
        #
        #     if self.Lock_Camera_To_View:
        #         context.space_data.lock_camera = True




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
