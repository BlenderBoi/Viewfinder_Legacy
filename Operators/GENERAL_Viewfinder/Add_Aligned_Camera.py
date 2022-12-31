
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils
import math

ENUM_Position = [("CURSOR","Cursor","Cursor"), ("CENTER","Center","Center")]
ENUM_Side = [("FRONT","Front","Front"), ("TOP","Top","Top")]

class VIEWFINDER_Add_Aligned_Camera(bpy.types.Operator):
    """Add Aligned Camera"""
    bl_idname = "viewfinder.add_aligned_camera"
    bl_label = "Add Aligned Camera"
    bl_options = {'UNDO', 'REGISTER'}

    side: bpy.props.EnumProperty(items=ENUM_Side)
    name: bpy.props.StringProperty(default="Camera")
    position: bpy.props.EnumProperty(items=ENUM_Position)
    Distance: bpy.props.FloatProperty(default=10.0)
    Angle: bpy.props.FloatProperty(default=0.0, subtype="ANGLE")
    View_Camera: bpy.props.BoolProperty(default=True)
    Use_Orthographic: bpy.props.BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "name", text="Name")
        row = layout.row(align=True)
        row.prop(self, "side", text="Side")
        row = layout.row(align=True)
        row.prop(self, "position", expand=True)
        layout.prop(self, "Distance", text="Distance")
        # layout.prop(self, "Angle", text="Angle")
        layout.prop(self, "View_Camera", text="View Camera")

    def execute(self, context):

        scn = context.scene
        render = scn.render
        object = None

        Viewfinder_Scene_Properties = scn.Viewfinder_Scene_Properties 
        # distance = Viewfinder_Scene_Properties.Default_Distance


        # self.Distance = distance

        bpy.ops.object.select_all(action='DESELECT')
        
        camera = bpy.data.cameras.new(self.name)
        object = bpy.data.objects.new(self.name, camera)
        context.collection.objects.link(object)

        if self.Use_Orthographic:
            camera.type = 'ORTHO'

        object.select_set(True)
        bpy.context.view_layer.objects.active = object

        if self.side == "FRONT":
            object.rotation_euler.x = math.radians(90)
            object.rotation_euler.y = math.radians(0)
            object.rotation_euler.z = self.Angle

        if self.side == "TOP":
            object.rotation_euler.x = self.Angle
            object.rotation_euler.y = math.radians(0)
            object.rotation_euler.z = math.radians(0)



        object.location = (0, 0, 0)

        if self.position == "CURSOR":
            object.location = context.scene.cursor.location


        context.view_layer.update()
        object.location = object.matrix_world @ mathutils.Vector((0, 0, self.Distance))

        if self.View_Camera:
            context.scene.camera = object
            context.space_data.region_3d.view_perspective = 'CAMERA'

        context.view_layer.update()





        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Add_Aligned_Camera]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
