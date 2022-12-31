
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils

import math


ENUM_Constraint = [("FOLLOW_PATH","Follow Path", "FOLLOW_PATH"),("CLAMP_TO","Clamped","Clamped")]
ENUM_Curve_Type = [("BEZIER","Bezier", "Bezier"),("NURBS","Nurbs","Nurbs")]





class VIEWFINDER_Create_And_Constraint_Curve_From_Selected_Camera(bpy.types.Operator):
    """Create and Constraint Curve From Selected Camera"""
    bl_idname = "viewfinder.create_and_constraint_curve_from_selected_camera"
    bl_label = "Create and Constraint Curve From Selected Camera"
    bl_options = {'UNDO', 'REGISTER'}

    constraint: bpy.props.EnumProperty(items=ENUM_Constraint)
    curve_type: bpy.props.EnumProperty(items=ENUM_Curve_Type)
    follow_curve_angle: bpy.props.BoolProperty(default=False)
    face_forward: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "constraint", text="Constraint", expand=True)
        # layout.prop(self, "curve_type", text="Curve Type", expand=True)

        if self.constraint == "FOLLOW_PATH":
            layout.prop(self, "follow_curve_angle", text="Follow Curve Angle")
            layout.prop(self, "face_forward", text="Face Forward")


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)




    def execute(self, context):


        scn = context.scene
        render = scn.render
        object = None

        selected_camera_objects = Utility_Functions.get_selected_object_type(context, ["CAMERA"])

        for object in selected_camera_objects:

            curve_data = bpy.data.curves.new(object.name + "_curve", type='CURVE')
            curve_data.dimensions = "3D"
            curve = bpy.data.objects.new(object.name + "_curve", curve_data)
            curve.location = object.matrix_world.translation
            context.collection.objects.link(curve)
            object.location = (0, 0, 0)

            spline = curve.data.splines.new(self.curve_type)

            if self.curve_type == "BEZIER":
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


            constraint = object.constraints.new(self.constraint)
            constraint.target = curve

            if self.constraint == "FOLLOW_PATH":
                constraint.use_curve_follow = self.follow_curve_angle
            if self.face_forward:
                object.rotation_euler.x = math.radians(90)
                object.rotation_euler.y = 0
                object.rotation_euler.z = 0






        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_And_Constraint_Curve_From_Selected_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
