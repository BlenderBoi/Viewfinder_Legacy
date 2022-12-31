

from math import tan
import bpy
from Viewfinder import Utility_Functions


ENUM_Constraint = [("TRACK_TO","Track To","Track To"),("DAMPED_TRACK","Damped Track","Damped Track")]






class VIEWFINDER_Track_Constraint_Selected_Camera_To_Active(bpy.types.Operator):
    """Track Constraint Selected Camera To Active"""
    bl_idname = "viewfinder.track_constraint_selected_camera_to_active"
    bl_label = "Track Constraint Selected Cameras To Active"
    bl_options = {'UNDO', 'REGISTER'}

    Constraint: bpy.props.EnumProperty(items=ENUM_Constraint)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Constraint", text="Constraint")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        
        target = context.object
        selected = [object for object in context.selected_objects if object.type=="CAMERA" and object != target]

        for object in selected:
            constraint = object.constraints.new(self.Constraint)
            constraint.target = target

            if self.Constraint == "DAMPED_TRACK":
                constraint.track_axis = "TRACK_NEGATIVE_Z"



        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [VIEWFINDER_Track_Constraint_Selected_Camera_To_Active]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()



