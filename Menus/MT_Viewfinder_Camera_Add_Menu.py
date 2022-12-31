import bpy
from Viewfinder import Utility_Functions


def draw_viewfinder_camera(self, context):


    preferences = Utility_Functions.get_addon_preferences()

    if preferences.Add_Menu:
        layout = self.layout






        if preferences.OP_Camera_From_View:
            layout.separator()
            operator = layout.operator("viewfinder.create_camera_from_view", text="Camera From View", icon="RESTRICT_VIEW_ON")


        
        if preferences.OP_Camera_And_Empty_Target:
            operator = layout.operator("viewfinder.add_camera_and_empty_target", text="Camera And Empty Target", icon="CON_CAMERASOLVER")



        if preferences.OP_Front_Camera:
            layout.separator()
            operator = layout.operator("viewfinder.add_aligned_camera", text="Front Camera", icon="VIEW_CAMERA")
            operator.side = "FRONT"
            operator.Angle = 0
            operator.Distance = 5
            operator.Use_Orthographic = False


        if preferences.OP_Top_Camera:
            operator = layout.operator("viewfinder.add_aligned_camera", text="Top Camera", icon="VIEW_CAMERA")
            operator.side = "TOP"
            operator.Angle = 0
            operator.Distance = 5
            operator.Use_Orthographic = False

        if preferences.OP_Camera_Booth:
            layout.separator()
            operator = layout.operator("viewfinder.add_camera_booth", text="Camera Booth", icon="SPHERE")
            operator.Use_Orthographic = False


        if preferences.OP_Camera_Preset:
            layout.separator()
            layout.operator("viewfinder.create_curve_fly_through_cam", text="Curve Fly Through Cam", icon="CON_CLAMPTO")
            layout.operator("viewfinder.create_curve_cam_with_aim", text="Curve Cam With Aim", icon="CON_CLAMPTO")



        if preferences.OP_Target_Empty_From_Selected:
            layout.separator()
            layout.operator("viewfinder.create_camera_target_empties", text="Target Empties From Selected Cameras", icon="EMPTY_AXIS")
        if preferences.OP_Marker_From_Selected_Camera:
            layout.operator("viewfinder.create_markers_from_selected_camera", text="Markers From Selected Cameras", icon="PMARKER_ACT")
        if preferences.OP_Clamped_Camera_From_Selected_Curve:
            layout.separator()
            # layout.operator("viewfinder.create_clamped_camera_from_selected_curves", text="Clamped Camera From Selected Curves", icon="CON_CLAMPTO")

            # layout.operator("viewfinder.constraint_camera_to_curve", text="Constraint Camera To Curve", icon="EMPTY_AXIS")
            layout.operator("viewfinder.create_constrainted_camera_from_selected_curves", text="Camera From Curves", icon="CON_CLAMPTO")
            layout.operator("viewfinder.create_and_constraint_curve_from_selected_camera", text="Curve From Camera", icon="CON_CLAMPTO")


classes = []

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_camera_add.append(draw_viewfinder_camera)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_camera_add.remove(draw_viewfinder_camera)

if __name__ == "__main__":
    register()
