
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math

ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Side = [("FRONT","Front","Front"), ("TOP","Top","Top")]

class VIEWFINDER_Add_Camera_Booth(bpy.types.Operator):
    """Add Aligned Camera"""
    bl_idname = "viewfinder.add_camera_booth"
    bl_label = "Add Camera Booth"
    bl_options = {'UNDO', 'REGISTER'}

    Top: bpy.props.BoolProperty(default=True)
    Quarter: bpy.props.BoolProperty(default=True)
    Bottom: bpy.props.BoolProperty(default=False)
    Size: bpy.props.FloatProperty(default=10)
    link_camera: bpy.props.BoolProperty(default=True)
    Use_Orthographic: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Size", text="Size")
        layout.prop(self, "Top", text="Top")
        layout.prop(self, "Quarter", text="Quarter")
        layout.prop(self, "Bottom", text="Bottom")
        layout.prop(self, "link_camera", text="Link Camera")

    def create_booth_camera(self, context, name, rotation, data=None):

        if data:
            camera = data
        else:
            camera = bpy.data.cameras.new(name)

        object = bpy.data.objects.new(name, camera)
        context.collection.objects.link(object)

        object.rotation_euler = rotation

        object.lock_location[0] = True
        object.lock_location[1] = True
        object.lock_location[2] = True

        object.lock_rotation[0] = True
        object.lock_rotation[1] = True
        object.lock_rotation[2] = True

        object.lock_scale[0] = True
        object.lock_scale[1] = True
        object.lock_scale[2] = True


        return object


    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        bpy.ops.object.select_all(action='DESELECT')

        link_camera = None

        if self.link_camera:
            link_camera = bpy.data.cameras.new("Cameras")

        Camera_Booth_Empty = bpy.data.objects.new("Camera_Booth", None)
        Camera_Booth_Empty.empty_display_type = "SPHERE"
        context.collection.objects.link(Camera_Booth_Empty)
        Camera_Booth_Empty.select_set(True)
        bpy.context.view_layer.objects.active = Camera_Booth_Empty

        Direction_Angle = {}

        Direction_Angle["Front"] = (90, 0, 0)
        Direction_Angle["Right"] = (90, 0, 90)
        Direction_Angle["Back"] = (90, 0, 180)
        Direction_Angle["Left"] = (90, 0, 270)

        if self.Quarter:
            Direction_Angle["Quarter_Front_Right"] = (90, 0, 45)
            Direction_Angle["Quarter_Back_Right"] = (90, 0, 135)
            Direction_Angle["Quarter_Back_Left"] = (90, 0, 225)
            Direction_Angle["Quarter_Front_Left"] = (90, 0, 315)

        if self.Top:
            Direction_Angle["Top"] = (0, 0, 0)
            Direction_Angle["Top_Front"] = (45, 0, 0)
            Direction_Angle["Top_Right"] = (45, 0, 90)
            Direction_Angle["Top_Back"] = (45, 0, 180)
            Direction_Angle["Top_Left"] = (45, 0, 270)

            if self.Quarter:
                Direction_Angle["Top_Quarter_Front_Left"] = (45, 0, 315)
                Direction_Angle["Top_Quarter_Front_Right"] = (45, 0, 45)
                Direction_Angle["Top_Quarter_Back_Right"] = (45, 0, 135)
                Direction_Angle["Top_Quarter_Back_Left"] = (45, 0, 225)

        if self.Bottom:
            Direction_Angle["Bottom"] = (180, 0, 0)
            Direction_Angle["Bottom_Front"] = (135, 0, 0)
            Direction_Angle["Bottom_Right"] = (135, 0, 90)
            Direction_Angle["Bottom_Back"] = (135, 0, 180)
            Direction_Angle["Bottom_Left"] = (135, 0, 270)


            if self.Quarter:
                Direction_Angle["Bottom_Quarter_Front_Right"] = (135, 0, 45)
                Direction_Angle["Bottom_Quarter_Back_Right"] = (135, 0, 135)
                Direction_Angle["Bottom_Quarter_Back_Left"] = (135, 0, 225)
                Direction_Angle["Bottom_Quarter_Front_Left"] = (135, 0, 315)

        Cameras = []

        for name, rotation_degree in Direction_Angle.items():

            rotation_radians = (math.radians(rotation_degree[0]), math.radians(rotation_degree[1]), math.radians(rotation_degree[2]))
            Camera = self.create_booth_camera(context, name, rotation_radians, data=link_camera)
            Cameras.append(Camera)

        context.view_layer.update()

        for Camera in Cameras:
            Distance = 1
            Camera.location = Camera.matrix_world @ mathutils.Vector((0, 0, Distance))
            Camera.select_set(True)




            context.view_layer.update()
            mw = Camera.matrix_world.copy()
            Camera.parent = Camera_Booth_Empty
            Camera.matrix_world = mw

            if self.Use_Orthographic:
                Camera.data.type = 'ORTHO'


            Constraint = Camera.constraints.new("LIMIT_SCALE")

            Constraint.use_min_x = True
            Constraint.use_min_y = True
            Constraint.use_min_z = True

            Constraint.min_x = 1
            Constraint.min_y = 1
            Constraint.min_z = 1

            Constraint.use_max_x = True
            Constraint.use_max_y = True
            Constraint.use_max_z = True

            Constraint.max_x = 1
            Constraint.max_y = 1
            Constraint.max_z = 1


        Camera_Booth_Empty.scale = (self.Size, self.Size, self.Size)
        Camera_Booth_Empty.location = context.scene.cursor.location
        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Add_Camera_Booth]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
