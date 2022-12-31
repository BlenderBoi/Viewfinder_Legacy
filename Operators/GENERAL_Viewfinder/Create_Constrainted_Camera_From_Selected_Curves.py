
import bpy
import os
from Viewfinder import Utility_Functions
import mathutils



ENUM_Constraint = [("FOLLOW_PATH","Follow Path", "FOLLOW_PATH"),("CLAMP_TO","Clamped","Clamped")]







class VIEWFINDER_Create_Constrainted_Camera_From_Selected_Curves(bpy.types.Operator):
    """Create Constrainted Camera From Selected Curves"""
    bl_idname = "viewfinder.create_constrainted_camera_from_selected_curves"
    bl_label = "Create Constrainted Camera From Selected Curves"
    bl_options = {'UNDO', 'REGISTER'}

    constraint: bpy.props.EnumProperty(items=ENUM_Constraint)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "constraint", text="Constraint", expand=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        scn = context.scene
        render = scn.render

        selected_curve_objects = Utility_Functions.get_selected_object_type(context, ["CURVE"])

        for object in selected_curve_objects:
            camera = bpy.data.cameras.new("Camera_" + object.name)
            camera_object = bpy.data.objects.new(self.name, camera)
            context.collection.objects.link(camera_object)

            # camera_object.parent = object
            constraint = camera_object.constraints.new(self.constraint)
            constraint.target = object


            curve_data = bpy.data.curves.new(object.name + "_curve", type='CURVE')
            curve_data.dimensions = "3D"
            curve = bpy.data.objects.new(object.name + "_curve", curve_data)




        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Create_Constrainted_Camera_From_Selected_Curves]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
