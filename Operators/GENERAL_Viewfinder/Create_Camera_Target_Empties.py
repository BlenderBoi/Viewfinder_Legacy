import bpy
from Viewfinder import Utility_Functions
import mathutils

ENUM_Empty_Shapes = [('PLAIN_AXES', 'Plain Axes', 'Plain Axes', "EMPTY_AXIS", 1), ('ARROWS', 'Arrows', 'Arrows', "EMPTY_ARROWS", 2), ('SINGLE_ARROW', 'Single Arrow', 'Single Arrow', "EMPTY_SINGLE_ARROW", 3), ('CIRCLE', "Circle", "Circle", "MESH_CIRCLE", 4), ('CUBE', "Cube", "Cube", "CUBE", 5), ('SPHERE', "Sphere", "Sphere", "SPHERE", 6), ('CONE', "Cone", "Cone", "CONE", 7), ('IMAGE',  "Image", "Image", "IMAGE_DATA", 8)]
ENUM_Constraint = [("TRACK_TO","Track To","Track To"),("DAMPED_TRACK","Damped Track","Damped Track")]

class VIEWFINDER_Create_Camera_Target_Empties(bpy.types.Operator):
    """Create Empties from Light and Track the Light to the created Empties"""
    bl_idname = "viewfinder.create_camera_target_empties"
    bl_label = "Create Camera Target Empties"
    bl_options = {'UNDO', 'REGISTER'}


    Empty_Shape: bpy.props.EnumProperty(items=ENUM_Empty_Shapes)
    Empty_Display_Size: bpy.props.FloatProperty(default=1)
    distance: bpy.props.FloatProperty(default=5.0)
    in_front: bpy.props.BoolProperty(default=True)
    Constraint: bpy.props.EnumProperty(items=ENUM_Constraint)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Constraint", text="Constraint", expand=True)
        layout.prop(self, "distance", text="Distance")
        layout.prop(self, "Empty_Display_Size", text="Size")
        layout.prop(self, "Empty_Shape", text="Shape")
        layout.prop(self, "in_front", text="In Front")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        selected_objects = [object for object in context.selected_objects if object.type == "CAMERA"]

        

        for object in selected_objects:

            empty = Utility_Functions.Create_Empty("TGT_EMPTIES_" + object.name)
            local_offset = mathutils.Vector((0, 0, -self.distance))
            empty.location = object.matrix_world @ local_offset
            empty.empty_display_type = self.Empty_Shape
            empty.empty_display_size = self.Empty_Display_Size
            empty.show_in_front = self.in_front
            object.select_set(False)
            empty.select_set(True)
            constraint = object.constraints.new(self.Constraint)
            constraint.target = empty
            constraint.track_axis = "TRACK_NEGATIVE_Z"
            context.view_layer.objects.active = empty

        return {'FINISHED'}


classes = [VIEWFINDER_Create_Camera_Target_Empties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
