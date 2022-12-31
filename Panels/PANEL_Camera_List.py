import bpy
import os
from Viewfinder import Utility_Functions

class VIEWFINDER_PT_Camera_List_Panel(bpy.types.Panel):
    """Viewfinder Camera List"""
    bl_label = "Viewfinder Camera List"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Viewfinder"


    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        return preferences.PANEL_Camera_List_Panel

    def draw_icon_expose(self, context, layout):

        preferences = Utility_Functions.get_addon_preferences()

        if Utility_Functions.draw_subpanel(preferences, preferences.SHOW_Camera_List_Icon_Expose, "SHOW_Camera_List_Icon_Expose", "Icon Expose", layout):

            layout.prop(preferences, "ICON_Camera_List_Select_Camera", text="Select Camera")
            layout.prop(preferences, "ICON_Camera_List_View_Camera", text="View Camera")
            layout.prop(preferences, "ICON_Camera_List_Set_Marker", text="Set Marker")
            layout.prop(preferences, "ICON_Camera_List_Resolution", text="Resolution")

            layout.prop(preferences, "ICON_Camera_List_Find_Camera", text="Find Camera")
            layout.prop(preferences, "ICON_Camera_List_Duplicate_Camera", text="Duplicate Camera")
            layout.prop(preferences, "ICON_Camera_List_Remove_Camera", text="Remove Camera")

    def draw(self, context):

        layout = self.layout
        scn = context.scene
        scn_properties = scn.Viewfinder_Scene_Properties
        col = layout.column(align=True)




        cameras = self.get_cameras(context)



        col.prop(scn_properties, "FILTER_Camera_List", text="Filter")
        col.prop(scn_properties, "FILTER_Name", text="", icon="VIEWZOOM")



        if scn_properties.FILTER_Camera_List == "SCENE":
            col.separator()
            col.prop(context.scene, "camera", text="Scene Camera")

        col.separator()
        row = col.row(align=True)
        row.prop(context.space_data, "lock_camera")
        row.prop(scn_properties, "Set_Resolution", text="Use Resolution")
        col.separator()

        self.draw_camera_list(context, col, cameras)



        self.draw_icon_expose(context, layout)


    def get_cameras(self, context):
        scn = context.scene
        scn_properties = scn.Viewfinder_Scene_Properties

        objects = []

        if scn_properties.FILTER_Camera_List in ["ALL"]:
            objects = [object for object in context.view_layer.objects if object.type == "CAMERA"]

        if scn_properties.FILTER_Camera_List in ["SELECTED"]:
            objects = [object for object in context.selected_objects if object.type == "CAMERA"]

        if scn_properties.FILTER_Camera_List in ["SCENE"]:
            if context.scene.camera:
                objects = [context.scene.camera]

        if scn_properties.FILTER_Camera_List in ["ACTIVE"]:
            if context.active_object:
                objects = [context.active_object]

        if not scn_properties.FILTER_Name == "":
            objects = [object for object in objects if scn_properties.FILTER_Name.lower() in object.name.lower()]




        return objects


    def draw_camera_list(self, context, layout, cameras):
        scn = context.scene
        scn_properties = scn.Viewfinder_Scene_Properties

        preferences = Utility_Functions.get_addon_preferences()
        if len(cameras) > 0:
            for object in cameras:


                box = layout.box()
                row = box.row(align=True)

                Object_Properties = object.Viewfinder_Object_Properties

                Show_Camera_Data = Utility_Functions.draw_subpanel(Object_Properties, Object_Properties.SHOW_Camera_Data_Options, "SHOW_Camera_Data_Options", "", row)


                if preferences.ICON_Camera_List_View_Camera:
                    operator = row.operator("viewfinder.view_camera", text="", icon="RESTRICT_VIEW_ON")
                    operator.object = object.name

                if preferences.ICON_Camera_List_Select_Camera:
                    operator = row.operator("viewfinder.select_camera", text="", icon="RESTRICT_SELECT_OFF")
                    operator.object = object.name

                if preferences.ICON_Camera_List_Find_Camera:
                    operator = row.operator("viewfinder.find_camera", text="", icon="VIEWZOOM")
                    operator.object = object.name



                if context.scene.camera == object:
                    row.prop(object, "name", text="", icon="SCENE_DATA")
                else:
                    row.prop(object, "name", text="")

                if scn_properties.Set_Resolution:
                    if preferences.ICON_Camera_List_Resolution:
                        if Object_Properties.Use_Resolution:
                            row.prop(Object_Properties, "Resolution_X", text="")
                            row.prop(Object_Properties, "Resolution_Y", text="")


                if preferences.ICON_Camera_List_Set_Marker:
                    operator = row.operator("viewfinder.add_camera_marker", text="", icon="MARKER_HLT")
                    operator.object = object.name

                if preferences.ICON_Camera_List_Duplicate_Camera:
                    operator = row.operator("viewfinder.duplicate_camera", text="", icon="DUPLICATE")
                    operator.object = object.name

                if preferences.ICON_Camera_List_Remove_Camera:
                    operator = row.operator("viewfinder.remove_camera", text="", icon="TRASH")
                    operator.object = object.name


                if Show_Camera_Data:
                    self.draw_camera_data(object, box)

                layout.separator()
        else:
            box = layout.box()
            box.label(text="No Camera Found", icon="INFO")
            layout.separator()




        row = layout.row(align=True)

        operator = row.operator("viewfinder.create_camera_from_view", text="New Camera From View", icon="PLUS")

        # operator = row.operator("viewfinder.add_aligned_camera", text="Camera", icon="ADD")
        # operator.side = "FRONT"
        # operator.View_Camera = False
        # operator.position = "CURSOR"
        # operator.Distance = 0



    def draw_camera_data(self, object, layout):

        Object_Properties = object.Viewfinder_Object_Properties

        col = layout.column(align=True)
        col.prop(object.data, "type")

        if object.data.type == "ORTHO":
            col.prop(object.data, "ortho_scale")

        if object.data.type in ["PERSP", "PANO"]:
            row = col.row(align=True)
            row.prop(object.data, "lens_unit", expand=True)

            if object.data.lens_unit == "MILLIMETERS":
                col.prop(object.data, "lens")
            if object.data.lens_unit == "FOV":
                col.prop(object.data, "angle")


        col.separator()
        row = col.row(align=True)
        row.prop(object.data, "shift_x")
        row.prop(object.data, "shift_y")

        row = col.row(align=True)
        row.prop(object.data, "clip_start")
        row.prop(object.data, "clip_end")

        col.separator()

        col.prop(Object_Properties, "Use_Resolution", text="Use Resolution")
        if Object_Properties.Use_Resolution:
            row2 = col.row(align=True)
            row2.prop(Object_Properties, "Resolution_X", text="Resolution X")
            row2.prop(Object_Properties, "Resolution_Y", text="Resolution Y")
            operator = row2.operator("viewfinder.resolution_match_scene", text="", icon="SCENE")
            operator.object = object.name
        col.separator()

        if Utility_Functions.draw_subpanel(Object_Properties, Object_Properties.SHOW_Display_Options, "SHOW_Display_Options", "Display Option", col):
            col.prop(object, "show_in_front")
            col.separator()
            col.prop(object.data, "display_size")
            col.prop(object.data, "show_limits")
            col.prop(object.data, "show_sensor")
            col.prop(object.data, "show_name")
            col.prop(object.data, "show_passepartout")
            if object.data.show_passepartout:
                col.prop(object.data, "passepartout_alpha")

        if Utility_Functions.draw_subpanel(Object_Properties, Object_Properties.SHOW_Sensor_Options, "SHOW_Sensor_Options", "Sensor Fit", col):
            col.prop(object.data, "sensor_fit", text="")
            if object.data.sensor_fit in ["AUTO","HORIZONTAL"]:
                col.prop(object.data, "sensor_width")
            if object.data.sensor_fit in ["VERTICAL"]:
                col.prop(object.data, "sensor_height")

        if Utility_Functions.draw_subpanel(Object_Properties, Object_Properties.SHOW_DOF_Options, "SHOW_DOF_Options", "Depth of Field", col):
            col.prop(object.data.dof, "use_dof")
            if object.data.dof.use_dof:
                col.prop(object.data.dof, "focus_object", text="")
                if not object.data.dof.focus_object:
                    col.prop(object.data.dof, "focus_distance")

                col.label(text="Aperture")

                col.prop(object.data.dof, "aperture_fstop")
                col.prop(object.data.dof, "aperture_blades")
                col.prop(object.data.dof, "aperture_rotation")
                col.prop(object.data.dof, "aperture_ratio")

classes = [VIEWFINDER_PT_Camera_List_Panel]


def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
