
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils


class VIEWFINDER_Create_Camera_And_Target(bpy.types.Operator):
    """Create Camera And Target"""
    bl_idname = "viewfinder.create_camera_and_target"
    bl_label = "Create Camera From And Target"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="Camera")
    offset: bpy.props.FloatVectorProperty(default=(0, -5, 0))
    view_camera: bpy.props.BoolProperty(default=False)

    create_fit_boundary_box: bpy.props.BoolProperty(default=False)
    create_empty_parent: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "view_camera", text="View Camera")
        layout.prop(self, "offset", text="Offset")
        layout.prop(self, "create_fit_boundary_box", text="Create Camera Fit Boundary Box")
        layout.prop(self, "create_empty_parent", text="Create Empty Parent")

    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        name = self.name
        location = context.scene.cursor.location

        bpy.ops.object.select_all(action='DESELECT')


        if self.create_fit_boundary_box:
            fit_boundary_box = Utility_Functions.create_cube(name="TGT_" + name + "Fit_Boundary_Box")
            fit_boundary_box.display_type = "WIRE"
            fit_boundary_box.hide_render = True

            empty = fit_boundary_box
            empty.location = location
        else:
            empty = Utility_Functions.Create_Empty("TGT_" + name)
            empty.location = location

        camera = Utility_Functions.Create_Camera(name, collection=None)
        camera.location = location + mathutils.Vector(self.offset)

        empty.select_set(True)
        camera.select_set(True)
        context.view_layer.objects.active = camera

        constraint = camera.constraints.new("TRACK_TO")
        constraint.target = empty
        constraint.track_axis = "TRACK_NEGATIVE_Z"



        if self.view_camera:
            context.scene.camera = camera
            context.space_data.region_3d.view_perspective = 'CAMERA'

        if self.create_fit_boundary_box:
            constraint = camera.constraints.new("LIMIT_DISTANCE")
            constraint.target = empty
            constraint.limit_mode = "LIMITDIST_OUTSIDE"
            constraint.use_transform_limit = True

            camera["Offset_Boundary"] = 2
            empty.show_in_front = True
            driver = constraint.driver_add('distance').driver
            v_dimension_x = driver.variables.new()
            v_dimension_x.name = "Dim_X"
            v_dimension_x.targets[0].id = empty
            v_dimension_x.targets[0].data_path = "dimensions[0]"

            v_dimension_y = driver.variables.new()
            v_dimension_y.name = "Dim_Y"
            v_dimension_y.targets[0].id = empty
            v_dimension_y.targets[0].data_path = "dimensions[1]"

            v_dimension_z = driver.variables.new()
            v_dimension_z.name = "Dim_Z"
            v_dimension_z.targets[0].id = empty
            v_dimension_z.targets[0].data_path = "dimensions[2]"

            v_lens = driver.variables.new()
            v_lens.name = "Lens"
            v_lens.targets[0].id = camera
            v_lens.targets[0].data_path = "data.lens"

            v_resolution_x = driver.variables.new()
            v_resolution_x.name = "Res_X"
            v_resolution_x.targets[0].id_type = "SCENE"
            v_resolution_x.targets[0].id = context.scene
            v_resolution_x.targets[0].data_path = "render.resolution_x"

            v_resolution_y = driver.variables.new()
            v_resolution_y.name = "Res_Y"
            v_resolution_y.targets[0].id_type = "SCENE"
            v_resolution_y.targets[0].id = context.scene
            v_resolution_y.targets[0].data_path = "render.resolution_y"

            v_offset_boundary = driver.variables.new()
            v_offset_boundary.name = "Offset_Boundary"
            v_offset_boundary.targets[0].id = camera
            v_offset_boundary.targets[0].data_path = '["Offset_Boundary"]'


            driver.expression = "max(Dim_X, Dim_Y, Dim_Z)*Lens/10*(max(Res_X, Res_Y)/min(Res_X, Res_Y))/(1 if Offset_Boundary == 0 else Offset_Boundary)"

        if self.create_empty_parent:
            context.view_layer.update()
            parent_empty = Utility_Functions.Create_Empty("ROOT_" + name)
            parent_empty.matrix_world = empty.matrix_world
            parent_empty.empty_display_type = "SPHERE"

            mw = empty.matrix_world.copy()
            empty.parent = parent_empty
            empty.matrix_world = mw

            mw = camera.matrix_world.copy()
            camera.parent = parent_empty
            camera.matrix_world = mw


        context.view_layer.update()
        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Camera_And_Target]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
