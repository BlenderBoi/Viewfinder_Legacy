
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils


#Fit Selected


ENUM_Mode = [("CURSOR", "Cursor", "Cursor"), ("VIEW", "Current View", "Current View")]

class VIEWFINDER_Create_Camera_And_Target(bpy.types.Operator):
    """Create Camera And Target"""
    bl_idname = "viewfinder.create_camera_and_target"
    bl_label = "Create Camera From And Target"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="Camera")
    offset: bpy.props.FloatVectorProperty(default=(0, -5, 0))
    view_camera: bpy.props.BoolProperty(default=False)

    mode: bpy.props.EnumProperty(items=ENUM_Mode)

    affect_x: bpy.props.BoolProperty(default=True)
    affect_y: bpy.props.BoolProperty(default=True)
    affect_z: bpy.props.BoolProperty(default=True)

    create_fit_boundary_box: bpy.props.BoolProperty(default=False)
    create_empty_parent: bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        # layout.prop(self, "mode", expand=True)


        if self.mode == "CURSOR":
            layout.prop(self, "offset", text="Offset")

        layout.prop(self, "view_camera", text="View Camera")

        layout.prop(self, "create_empty_parent", text="Create Empty Parent")


        layout.prop(self, "create_fit_boundary_box", text="Create Camera Fit Boundary Box")
        if self.create_fit_boundary_box:
            row = layout.row(align=True)
            row.prop(self, "affect_x", text="Affect X")
            row.prop(self, "affect_y", text="Affect Y")
            row.prop(self, "affect_z", text="Affect Z")


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
        empty.show_in_front = True
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

            # camera["Offset_Boundary"] = 2
            camera["Affect_X"] = self.affect_x
            camera["Affect_Y"] = self.affect_y
            camera["Affect_Z"] = self.affect_z

            camera["_RNA_UI"] = {}
            camera["_RNA_UI"]["Affect_X"] = {"default": 1, "min":0, "max":1, "soft_mix":0, "soft_max":1}
            camera["_RNA_UI"]["Affect_Y"] = {"default": 1, "min":0, "max":1, "soft_mix":0, "soft_max":1}
            camera["_RNA_UI"]["Affect_Z"] = {"default": 1, "min":0, "max":1, "soft_mix":0, "soft_max":1}




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

            v_lens = driver.variables.new()
            v_lens.name = "Angle"
            v_lens.targets[0].id = camera
            v_lens.targets[0].data_path = "data.angle"

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

            # v_offset_boundary = driver.variables.new()
            # v_offset_boundary.name = "Offset_Boundary"
            # v_offset_boundary.targets[0].id = camera
            # v_offset_boundary.targets[0].data_path = '["Offset_Boundary"]'


            v_offset_boundary = driver.variables.new()
            v_offset_boundary.name = "Affect_X"
            v_offset_boundary.targets[0].id = camera
            v_offset_boundary.targets[0].data_path = '["Affect_X"]'

            v_offset_boundary = driver.variables.new()
            v_offset_boundary.name = "Affect_Y"
            v_offset_boundary.targets[0].id = camera
            v_offset_boundary.targets[0].data_path = '["Affect_Y"]'
            v_offset_boundary = driver.variables.new()

            v_offset_boundary.name = "Affect_Z"
            v_offset_boundary.targets[0].id = camera
            v_offset_boundary.targets[0].data_path = '["Affect_Z"]'


            #depth = -scale_y/(tan(CamAngle/2)* Res_Y/(Res_X))

            # driver.expression = "max(Dim_X, Dim_Y, Dim_Z)*Lens/10*(max(Res_X, Res_Y)/min(Res_X, Res_Y))/(1 if Offset_Boundary == 0 else Offset_Boundary)"
            driver.expression = "max(Dim_X*Affect_X, Dim_Y*Affect_Y, Dim_Z*Affect_Z)/tan(Angle/2)*(max(Res_X, Res_Y)/min(Res_X, Res_Y))"

        if self.create_empty_parent:
            context.view_layer.update()
            parent_empty = Utility_Functions.Create_Empty("ROOT_" + name)
            parent_empty.matrix_world = empty.matrix_world
            parent_empty.empty_display_type = "CIRCLE"

            mw = empty.matrix_world.copy()
            empty.parent = parent_empty
            empty.matrix_world = mw

            mw = camera.matrix_world.copy()
            camera.parent = parent_empty
            camera.matrix_world = mw
            parent_empty.show_in_front = True

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
