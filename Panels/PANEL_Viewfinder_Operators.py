import bpy
import os
from Viewfinder import Utility_Functions

class VIEWFINDER_PT_Viewfinder_Operators_Panel(bpy.types.Panel):
    """Viewfinder Operators"""
    bl_label = "Viewfinder Operators"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Viewfinder"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        return preferences.PANEL_Viewfinder_Operators_Panel

    def draw(self, context):



        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT";

        layout.label(text="Scene Camera")
        layout.prop(context.scene, "camera", text="")


        layout.separator()

        Utility_Functions.draw_operators(context, layout)



classes = [VIEWFINDER_PT_Viewfinder_Operators_Panel]


def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
