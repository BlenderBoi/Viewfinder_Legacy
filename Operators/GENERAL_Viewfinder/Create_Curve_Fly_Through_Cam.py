

import bpy
import os
from Viewfinder import Utility_Functions
import mathutils

import math


ENUM_Constraint = [("FOLLOW_PATH","Follow Path", "FOLLOW_PATH"),("CLAMP_TO","Clamped","Clamped")]
ENUM_Curve_Type = [("BEZIER","Bezier", "Bezier"),("NURBS","Nurbs","Nurbs")]





class VIEWFINDER_Create_Curve_Fly_Through_Cam(bpy.types.Operator):
    """Create Curve Fly Through Cam"""
    bl_idname = "viewfinder.create_curve_fly_through_cam"
    bl_label = "Create Curve Fly Through Cam"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="FlyThroughCamera")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name", expand=True)

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

        constraint.use_curve_follow = True
        camera_object.rotation_euler.x = math.radians(90)
        camera_object.rotation_euler.y = 0
        camera_object.rotation_euler.z = 0






        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Curve_Fly_Through_Cam]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
