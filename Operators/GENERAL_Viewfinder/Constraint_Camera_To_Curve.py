

import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math



ENUM_Constraint = [("FOLLOW_PATH","Follow Path", "FOLLOW_PATH"),("CLAMP_TO","Clamped","Clamped")]




class VIEWFINDER_Constraint_Camera_To_Curve(bpy.types.Operator):
    """Constraint Camera To Curve"""
    bl_idname = "viewfinder.constraint_camera_to_curve"
    bl_label = "Constraint Camera To Curve"
    bl_options = {'UNDO', 'REGISTER'}


    constraint: bpy.props.EnumProperty(items=ENUM_Constraint)
    turn_off_influence_after_first: bpy.props.BoolProperty(default=True)
    clear_location: bpy.props.BoolProperty(default=True)
    follow_curve_angle: bpy.props.BoolProperty(default=False)
    face_forward: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "constraint", text="Constraint", expand=True)
        layout.prop(self, "turn_off_influence_after_first", text="Turn Off Influence After First Curve", expand=True)
        layout.prop(self, "clear_location", text="Clear Location", expand=True)
        if self.constraint == "FOLLOW_PATH":
            layout.prop(self, "follow_curve_angle", text="Follow Curve Angle")
            layout.prop(self, "face_forward", text="Face Forward")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        render = scn.render

        curves = [obj for obj in context.selected_objects if obj.type == "CURVE"]
        cameras = [obj for obj in context.selected_objects if obj.type == "CAMERA"]


        for camera in cameras:


            for index, curve in enumerate(curves):

                if self.clear_location:
                    camera.location = (0, 0, 0)


                constraint = camera.constraints.new(self.constraint)
                constraint.target = curve
                if self.constraint == "FOLLOW_PATH":
                    constraint.use_curve_follow = self.follow_curve_angle
                if self.face_forward:
                    camera.rotation_euler.x = math.radians(90)
                    camera.rotation_euler.y = 0
                    camera.rotation_euler.z = 0


                if index > 0:
                    if self.turn_off_influence_after_first:
                        constraint.influence = 0


        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Constraint_Camera_To_Curve]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
