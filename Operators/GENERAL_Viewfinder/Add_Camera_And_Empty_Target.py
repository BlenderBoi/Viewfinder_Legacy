
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math

ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Constraint = [("TRACK_TO","Track To","Track To"),("DAMPED_TRACK","Damped Track","Damped Track")]
ENUM_Empty_Shapes = [('PLAIN_AXES', 'Plain Axes', 'Plain Axes', "EMPTY_AXIS", 1), ('ARROWS', 'Arrows', 'Arrows', "EMPTY_ARROWS", 2), ('SINGLE_ARROW', 'Single Arrow', 'Single Arrow', "EMPTY_SINGLE_ARROW", 3), ('CIRCLE', "Circle", "Circle", "MESH_CIRCLE", 4), ('CUBE', "Cube", "Cube", "CUBE", 5), ('SPHERE', "Sphere", "Sphere", "SPHERE", 6), ('CONE', "Cone", "Cone", "CONE", 7), ('IMAGE',  "Image", "Image", "IMAGE_DATA", 8)]

class VIEWFINDER_Add_Camera_And_Empty_Target(bpy.types.Operator):
    """Add Camera And Empty Target"""
    bl_idname = "viewfinder.add_camera_and_empty_target"
    bl_label = "Add Camera And Empty Target"
    bl_options = {'UNDO', 'REGISTER'}


    name: bpy.props.StringProperty(default="Camera")
    position: bpy.props.EnumProperty(items=ENUM_Position)

    Constraint: bpy.props.EnumProperty(items=ENUM_Constraint)

    Distance: bpy.props.FloatProperty(default=5.0)
    Height: bpy.props.FloatProperty(default=0.0, subtype="ANGLE")
    Angle: bpy.props.FloatProperty(default=0.0, subtype="ANGLE")

    Empty_Shape: bpy.props.EnumProperty(items=ENUM_Empty_Shapes)
    Empty_Display_Size: bpy.props.FloatProperty(default=1)

    Use_Orthographic: bpy.props.BoolProperty(default=False)

    # Empty Size
    # Empty Shape
    # Constraint

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "name", text="Name")
        # row = layout.row(align=True)
        # row.prop(self, "side", text="Side")
        row = layout.row(align=True)
        row.prop(self, "position", expand=True)

        col = layout.column(align=True)

        col.prop(self, "Distance", text="Distance")
        row = col.row(align=True)
        row.prop(self, "Height", text="Height")
        row.prop(self, "Angle", text="Angle")

        row = layout.row(align=True)
        row.prop(self, "Constraint", expand=True)

        layout.prop(self, "Empty_Shape", text="Shape")
        layout.prop(self, "Empty_Display_Size", text="Display Size")

    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        bpy.ops.object.select_all(action='DESELECT')

        camera = bpy.data.cameras.new(self.name)
        object = bpy.data.objects.new(self.name, camera)
        context.collection.objects.link(object)

        if self.Use_Orthographic:
            camera.type = 'ORTHO'


        object.select_set(True)
        bpy.context.view_layer.objects.active = object

        target = bpy.data.objects.new("TGT_" + self.name, None)
        context.collection.objects.link(target)

        target.select_set(True)

        target.empty_display_type = self.Empty_Shape
        target.empty_display_size = self.Empty_Display_Size


        object.location = (0, 0, 0)
        target.location = (0, 0, 0)

        if self.position == "CURSOR":
            object.location = context.scene.cursor.location
            target.location = context.scene.cursor.location



        object.rotation_euler.rotate(mathutils.Euler((math.radians(90), 0, 0)))
        object.rotation_euler.rotate(mathutils.Euler((-self.Height, 0, 0)))
        object.rotation_euler.rotate(mathutils.Euler((0, 0, self.Angle)))




        context.view_layer.update()



        object.location = object.matrix_world @ mathutils.Vector((0, 0, self.Distance))


        constraint = object.constraints.new(self.Constraint)
        constraint.target = target
        constraint.track_axis = "TRACK_NEGATIVE_Z"



        context.view_layer.update()





        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Add_Camera_And_Empty_Target]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
