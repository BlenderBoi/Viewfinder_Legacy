import bpy

from Viewfinder import Utility_Functions
#Camera to View

class VIEWFINDER_MT_Viewfinder_Menu(bpy.types.Menu):
    bl_label = "Viewfinder Menu"
    bl_idname = "VIEWFINDER_MT_viewfinder_menu"

    def draw(self, context):


        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT";





        scn = context.scene
        Viewfinder_Scene_Properties = scn.Viewfinder_Scene_Properties 


        col = layout.column(align=True)

        operator = col.operator("viewfinder.create_camera_from_view", text="Camera From View", icon="RESTRICT_VIEW_ON")


        col = layout.column(align=True)



        operator = col.operator("viewfinder.add_camera_and_empty_target", text="With Empty Target", icon="CON_CAMERASOLVER")
        operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

        operator = col.operator("viewfinder.add_aligned_camera", text="Front", icon="VIEW_CAMERA")
        operator.side = "FRONT"
        operator.Angle = 0
        operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

        operator = col.operator("viewfinder.add_aligned_camera", text="Top", icon="VIEW_CAMERA")
        operator.side = "TOP"
        operator.Angle = 0
        operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

        col.separator()

        operator = col.operator("viewfinder.add_camera_booth", text="Camera Booth Setup", icon="SPHERE")
        operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic


        col = layout.column(align=True)

        col.prop(Viewfinder_Scene_Properties, "Align_Cam_Use_Orthographic", text="Use Orthographic", expand=False)


        col.separator()

        col.label(text="Create Camera Setup", icon="PRESET")
        col.operator("viewfinder.create_curve_fly_through_cam", text="Curve Cam Fly Through", icon="CON_CLAMPTO")
        col.operator("viewfinder.create_curve_cam_with_aim", text="Curve Cam With Aim", icon="CON_CLAMPTO")


        layout.separator()



        col.separator()




        col.label(text="Constraint Selected Cameras", icon="CONSTRAINT")

        col.operator("viewfinder.constraint_camera_to_curve", text="To Selected Curve", icon="CONSTRAINT")
        col.operator("viewfinder.track_constraint_selected_camera_to_active", text="Track To Active Object", icon="CON_TRACKTO")

        col.separator()

        col.label(text="Selected Camera Utility", icon="RESTRICT_SELECT_OFF")

        col.operator("viewfinder.selected_camera_to_view", text="Selected Camera To View", icon="CAMERA_DATA")
        col.operator("viewfinder.frame_active_camera_to_selected_objects", text="Frame Active Camera To Selected Objects", icon="CAMERA_DATA")
        col.separator()

        col.label(text="From Selected", icon="ADD")

        col.operator("viewfinder.create_camera_target_empties", text="Create Empty Targets", icon="EMPTY_AXIS")
        col.operator("viewfinder.create_markers_from_selected_camera", text="Create Markers", icon="PMARKER_ACT")

        col.separator()

        col.operator("viewfinder.create_constrainted_camera_from_selected_curves", text="Create Camera From Curves", icon="CAMERA_DATA")
        col.operator("viewfinder.create_and_constraint_curve_from_selected_camera", text="Create Curve From Camera", icon="CON_CLAMPTO")


        col.separator()

        col.label(text="Scene Camera Utility", icon="SCENE_DATA")

        col.operator("view3d.camera_to_view_selected", text="Frame Selected Objects", icon="MESH_PLANE")
        col.operator("view3d.camera_to_view", text="Scene Camera To View", icon="CAMERA_DATA")



        # layout.separator()
        # operator = layout.operator("viewfinder.add_aligned_camera", text="Front Camera", icon="VIEW_CAMERA")
        # operator.side = "FRONT"
        # operator.Angle = 0
        # operator.Distance = 5


        # operator = layout.operator("viewfinder.add_aligned_camera", text="Top Camera", icon="VIEW_CAMERA")
        # operator.side = "TOP"
        # operator.Angle = 0
        # operator.Distance = 5









        # layout.separator()

        # operator = layout.operator("viewfinder.create_camera_from_view", text="Camera From View", icon="RESTRICT_VIEW_ON")
        # operator = layout.operator("viewfinder.add_camera_booth", text="Camera Booth", icon="SPHERE")
        # operator = layout.operator("viewfinder.add_camera_and_empty_target", text="Camera And Empty Target", icon="CON_CAMERASOLVER")


        # layout.separator()
        # layout.label(text="Camera Preset")
        # layout.operator("viewfinder.create_curve_fly_through_cam", text="Create Curve Fly Through Cam", icon="CON_CLAMPTO")
        # layout.operator("viewfinder.create_curve_cam_with_aim", text="Create Curve Cam With Aim", icon="CON_CLAMPTO")


        # layout.separator()

        # layout.operator("viewfinder.create_camera_target_empties", text="Target Empties From Selected", icon="EMPTY_AXIS")
        # layout.operator("viewfinder.create_markers_from_selected_camera", text="Markers From Selected Camera", icon="PMARKER_ACT")
        # # layout.operator("viewfinder.create_clamped_camera_from_selected_curves", text="Clamped Camera From Selected Curves", icon="CON_CLAMPTO")

        # layout.separator()
        # layout.label(text="Camera Curve Tools")

        # layout.operator("viewfinder.constraint_camera_to_curve", text="Constraint Camera To Curve", icon="EMPTY_AXIS")
        # layout.operator("viewfinder.create_constrainted_camera_from_selected_curves", text="Camera From Curves", icon="CON_CLAMPTO")
        # layout.operator("viewfinder.create_and_constraint_curve_from_selected_camera", text="Curve From Camera", icon="CON_CLAMPTO")




        # layout.separator()
        # layout.label(text="Blender Tools")

        # layout.operator("view3d.camera_to_view_selected", text="Active Camera View Selected", icon="MESH_PLANE")
        # layout.operator("view3d.camera_to_view", text="Active Camera To View", icon="CAMERA_DATA")





addon_keymaps = []

classes = [VIEWFINDER_MT_Viewfinder_Menu]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu", type="C", value="PRESS", shift=True, ctrl=True, alt=True)
        kmi.properties.name = "VIEWFINDER_MT_viewfinder_menu"
        addon_keymaps.append([km, kmi])


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    addon_keymaps.clear()


if __name__ == "__main__":
    register()
