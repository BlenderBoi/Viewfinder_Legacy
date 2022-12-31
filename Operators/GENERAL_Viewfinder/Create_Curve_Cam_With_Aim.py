

import bpy
import os
from Viewfinder import Utility_Functions
import mathutils

import math


ENUM_Constraint = [("FOLLOW_PATH","Follow Path", "FOLLOW_PATH"),("CLAMP_TO","Clamped","Clamped")]
ENUM_Curve_Type = [("BEZIER","Bezier", "Bezier"),("NURBS","Nurbs","Nurbs")]
ENUM_Empty_Shapes = [('PLAIN_AXES', 'Plain Axes', 'Plain Axes', "EMPTY_AXIS", 1), ('ARROWS', 'Arrows', 'Arrows', "EMPTY_ARROWS", 2), ('SINGLE_ARROW', 'Single Arrow', 'Single Arrow', "EMPTY_SINGLE_ARROW", 3), ('CIRCLE', "Circle", "Circle", "MESH_CIRCLE", 4), ('CUBE', "Cube", "Cube", "CUBE", 5), ('SPHERE', "Sphere", "Sphere", "SPHERE", 6), ('CONE', "Cone", "Cone", "CONE", 7), ('IMAGE',  "Image", "Image", "IMAGE_DATA", 8)]

ENUM_Constraint = [("TRACK_TO","Track To","Track To"),("DAMPED_TRACK","Damped Track","Damped Track")]




class VIEWFINDER_Create_Curve_Cam_With_Aim(bpy.types.Operator):
    """Create Curve Fly Through Cam"""
    bl_idname = "viewfinder.create_curve_cam_with_aim"
    bl_label = "Create Curve Cam With Aim"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="CurveCamera")
    Empty_Shape: bpy.props.EnumProperty(items=ENUM_Empty_Shapes)
    Empty_Display_Size: bpy.props.FloatProperty(default=1)
    Constraint: bpy.props.EnumProperty(items=ENUM_Constraint)
    in_front: bpy.props.BoolProperty(default=True)
    distance: bpy.props.FloatProperty(default=5.0)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name", expand=True)
        layout.prop(self, "Empty_Display_Size", text="Target Size")
        layout.prop(self, "distance", text="Target Distance")
        layout.prop(self, "Empty_Shape", text="Target Shape")
        layout.prop(self, "in_front", text="Target In Front")
        layout.prop(self, "Constraint", text="Target Tracking Constraint", expand=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):


        scn = context.scene
        render = scn.render
        object = None

        camera = bpy.data.cameras.new(self.name)
        camera_object = bpy.data.objects.new(self.name, camera)
        context.collection.objects.link(camera_object)

        curve_data = bpy.data.curves.new(camera_object.name + "_curve", type='CURVE')
        curve_data.dimensions = "3D"
        curve = bpy.data.objects.new(camera_object.name + "_curve", curve_data)
        context.collection.objects.link(curve)
        curve.location = context.scene.cursor.location

        spline = curve.data.splines.new("BEZIER")

        spline.bezier_points.add(1)
        length = 3
        spline.bezier_points[1].co.y = -length
        spline.bezier_points[1].handle_left = spline.bezier_points[1].co
        spline.bezier_points[1].handle_right= spline.bezier_points[1].co
        spline.bezier_points[1].handle_left.y += 0.5
        spline.bezier_points[1].handle_right.y += -0.5

        spline.bezier_points[0].co.y = 0
        spline.bezier_points[0].handle_left = spline.bezier_points[0].co
        spline.bezier_points[0].handle_right= spline.bezier_points[0].co
        spline.bezier_points[0].handle_left.y += 0.5
        spline.bezier_points[0].handle_right.y += -0.5


        constraint = camera_object.constraints.new("FOLLOW_PATH")
        constraint.target = curve


        empty = Utility_Functions.Create_Empty("TGT_EMPTIES_" + camera_object.name)
        local_offset = mathutils.Vector((0, 0, -self.distance))
        empty.location = curve.location + local_offset
        empty.empty_display_type = self.Empty_Shape
        empty.empty_display_size = self.Empty_Display_Size
        empty.show_in_front = self.in_front
        camera_object.select_set(False)
        empty.select_set(True)
        constraint = camera_object.constraints.new(self.Constraint)
        constraint.target = empty
        constraint.track_axis = "TRACK_NEGATIVE_Z"
        context.view_layer.objects.active = empty


        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Curve_Cam_With_Aim]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
