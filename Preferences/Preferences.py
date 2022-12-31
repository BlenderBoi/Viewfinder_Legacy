import bpy
import os
import pathlib
import rna_keymap_ui

from . import Preferences
from Viewfinder import Utility_Functions
from Viewfinder import Panels
from Viewfinder import Data


addon_keymaps = []



def set_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu", type="C", value="PRESS", shift=True, alt=True, ctrl=True)
        kmi.properties.name = "VIEWFINDER_MT_viewfinder_menu"
        addon_keymaps.append([km, kmi])

        kmi = km.keymap_items.new("viewfinder.preview_camera", type="ACCENT_GRAVE", value="PRESS", shift=True, alt=True, ctrl=True)
        addon_keymaps.append([km, kmi])


def unset_keymaps():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


def get_menu(km, operator, menu):
    for idx, kmi in enumerate(km.keymap_items):
        if km.keymap_items.keys()[idx] == operator:
            if km.keymap_items[idx].properties.name == menu:
                return kmi
    return None

def get_operator(km, operator):
    for idx, kmi in enumerate(km.keymap_items):
        if km.keymap_items.keys()[idx] == operator:
            return kmi
    return None


def draw_keymaps(self, context, layout):
    col = layout.column()
    kc = context.window_manager.keyconfigs.user # addon
    km = kc.keymaps['3D View'] #
    keymap_items = km.keymap_items
    kmi = get_menu(km, 'wm.call_menu', 'VIEWFINDER_MT_viewfinder_menu')
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)


    kmi = get_operator(km, 'viewfinder.preview_camera')
    rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)













def update_panel(self, context):

    addon_preferences = Utility_Functions.get_addon_preferences()
    message = ": Updating Panel locations has failed"

    panels = []


    pt = Panels.PANEL_Camera_List.VIEWFINDER_PT_Camera_List_Panel
    catagory = addon_preferences.PANEL_Camera_List_Panel_Category
    label = addon_preferences.PANEL_Camera_List_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)

    pt = Panels.PANEL_Viewfinder_Operators.VIEWFINDER_PT_Viewfinder_Operators_Panel
    catagory = addon_preferences.PANEL_Viewfinder_Operators_Panel_Category
    label = addon_preferences.PANEL_Viewfinder_Operators_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)




    try:
        pass
        for item in panels:

            panel = item[0]
            category = item[1]
            label = item[2]

            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

            panel.bl_category = category
            panel.bl_label = label

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass




def POLL_Camera(self, object):
    if object.type == "CAMERA":
        if bpy.context.view_layer.objects.get(object.name):
            return True



ENUM_Preview_Target = [("BOTH", "Both", ""),("ACTIVE","Active Object (Camera)","Active Selection"),("SCENE","Scene Camera","Camera")]
ENUM_Offset_Mode = [("RELATIVE", "Relative", ""),("ABSOLUTE","Absolute","")]


ENUM_Tabs = [("GENERAL", "Panels", "Panels"), ("ADD_OPERATOR", "Add Menu Operators", "Add Operators"), ("PREVIEWER","Camera Previewer","Camera Previewer"),("KEYMAPS", "Keymap", "Keymap")]

class Viewfinder_user_preferences(bpy.types.AddonPreferences):

    bl_idname = Utility_Functions.get_addon_name()



    TABS_Preferences: bpy.props.EnumProperty(items=ENUM_Tabs)

    # Camera_Previwer_Settings: bpy.props.PointerProperty(type=Camera_Previewer_Properties)


    PANEL_Viewfinder_Operators_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Viewfinder_Operators_Panel_Category: bpy.props.StringProperty(default="Viewfinder", update=update_panel)
    PANEL_Viewfinder_Operators_Panel_Label: bpy.props.StringProperty(default="Viewfinder Operators", update=update_panel)

    PANEL_Camera_Previewer_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Camera_Previewer_Panel_Category: bpy.props.StringProperty(default="Viewfinder", update=update_panel)
    PANEL_Camera_Previewer_Panel_Label: bpy.props.StringProperty(default="Viewfinder Previewer", update=update_panel)



    PANEL_Camera_List_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Camera_List_Panel_Category: bpy.props.StringProperty(default="Viewfinder", update=update_panel)
    PANEL_Camera_List_Panel_Label: bpy.props.StringProperty(default="Viewfinder Camera List", update=update_panel)

    Add_Menu: bpy.props.BoolProperty(default=True)

    OP_Front_Camera: bpy.props.BoolProperty(default=True)
    OP_Top_Camera: bpy.props.BoolProperty(default=True)
    OP_Camera_From_View: bpy.props.BoolProperty(default=True)
    OP_Camera_Booth: bpy.props.BoolProperty(default=True)
    OP_Camera_And_Empty_Target: bpy.props.BoolProperty(default=True)
    OP_Target_Empty_From_Selected: bpy.props.BoolProperty(default=True)
    OP_Marker_From_Selected_Camera: bpy.props.BoolProperty(default=True)
    OP_Clamped_Camera_From_Selected_Curve: bpy.props.BoolProperty(default=True)


    OP_Camera_Preset: bpy.props.BoolProperty(default=True)


    SHOW_Camera_List_Icon_Expose: bpy.props.BoolProperty(default=False)

    ICON_Camera_List_Select_Camera: bpy.props.BoolProperty(default=False)
    ICON_Camera_List_View_Camera: bpy.props.BoolProperty(default=True)
    ICON_Camera_List_Set_Marker: bpy.props.BoolProperty(default=True)
    ICON_Camera_List_Find_Camera: bpy.props.BoolProperty(default=False)
    ICON_Camera_List_Duplicate_Camera: bpy.props.BoolProperty(default=False)
    ICON_Camera_List_Remove_Camera: bpy.props.BoolProperty(default=True)

    ICON_Camera_List_Resolution: bpy.props.BoolProperty(default=False)




    # Previewer

    PREVIEWER_Target: bpy.props.EnumProperty(items=ENUM_Preview_Target)
    PREVIEWER_Render_Percentage: bpy.props.FloatProperty(default=25, subtype="PERCENTAGE", min=0, soft_max=100)

    PREVIEWER_Width_Rel: bpy.props.FloatProperty(default=0.25, min=0, soft_max=0.5)
    PREVIEWER_Width_Abs: bpy.props.FloatProperty(default=400, min=0,soft_min=50, soft_max=2000, subtype="PIXEL")
    PREVIEWER_Width_Mode: bpy.props.EnumProperty(items=ENUM_Offset_Mode, default="RELATIVE") # Relative | Absolute

    PREVIEWER_Hide_Overlay_In_Preview: bpy.props.BoolProperty(default=False) # Relative | Absolute


    # Offset in Pixels
    # PREVIEWER_Offset_Origin: bpy.props.EnumProperty() # Center | Bottom Left
    # PREVIEWER_Offset_Horizontal_Side: bpy.props.EnumProperty() # Left | Right 
    # PREVIEWER_Offset_Vertical_Side: bpy.props.EnumProperty() # Top | Bottom

    PREVIEWER_Offset_Mode: bpy.props.EnumProperty(items=ENUM_Offset_Mode, default="RELATIVE") # Relative | Absolute

    PREVIEWER_Offset_X_Rel: bpy.props.FloatProperty(default=0.1, soft_min=0.0, soft_max=1.0)
    PREVIEWER_Offset_Y_Rel: bpy.props.FloatProperty(default=0.1, soft_min=0.0, soft_max=1.0)

    PREVIEWER_Offset_X_Abs: bpy.props.FloatProperty(default=100, subtype="PIXEL")
    PREVIEWER_Offset_Y_Abs: bpy.props.FloatProperty(default=100, subtype="PIXEL")

    PREVIEWER_Font_Offset: bpy.props.FloatProperty(default=1.5, soft_min=0.0, soft_max=10.0)
    PREVIEWER_Font_Size: bpy.props.FloatProperty(default=15.0, min=0.0, soft_max=100.0)


    PREVIEWER_Display_Camera_Name: bpy.props.BoolProperty(default=True)

    PREVIEWER_Border_Use_Hover: bpy.props.BoolProperty(default=True)
    PREVIEWER_Border_Thickness: bpy.props.FloatProperty(default=4.0, min=0.0, max=10.0)
    PREVIEWER_Border_Color_Normal: bpy.props.FloatVectorProperty(default=[0.157, 0.157, 0.157, 1.0], size=4,subtype="COLOR", min=0.0, max=1.0)
    PREVIEWER_Border_Color_Hover: bpy.props.FloatVectorProperty(default=[1.0, 0.478, 0.0, 1.0], size=4,subtype="COLOR", min=0.0, max=1.0)
    PREVIEWER_Hide_In_Camera_View: bpy.props.BoolProperty(default=True)

    PREVIEWER_Font_Color: bpy.props.FloatVectorProperty(default=[1.0, 1.0, 1.0, 1.0], size=4,subtype="COLOR", min=0.0, max=1.0)
    PREVIEWER_Disable_Click: bpy.props.BoolProperty(default=False)


    PREVIEWER_Obey_Hide_Overlay: bpy.props.BoolProperty(default=True)

    PREVIEWER_Auto_Enable: bpy.props.BoolProperty(default=False)
    PREVIEWER_State: bpy.props.BoolProperty(default=False)







    def draw_previewer_settings(self, context, layout):

        layout = self.layout
        layout.label(text="Preview Camera Settings")

        preferences = Utility_Functions.get_addon_preferences()

        col = layout.column(align=True)

        col.prop(preferences, "PREVIEWER_Target", text="")
        row = col.row(align=True)
        row.prop(preferences, "PREVIEWER_Render_Percentage", text="Resolution")

        col.prop(preferences, "PREVIEWER_Hide_In_Camera_View", text="Hide Preview In Camera View")
        col.prop(preferences, "PREVIEWER_Obey_Hide_Overlay", text="Obey Hide Overlay")
        col.prop(preferences, "PREVIEWER_Hide_Overlay_In_Preview", text="Hide Overlay in Preview")

        col.prop(preferences, "PREVIEWER_Display_Camera_Name", text="Display Camera Name")

        if preferences.PREVIEWER_Display_Camera_Name:
            col.label(text="Label Font")
            col.prop(preferences, "PREVIEWER_Font_Color", text="")
            col.prop(preferences, "PREVIEWER_Font_Offset", text="Font Offset")
            col.prop(preferences, "PREVIEWER_Font_Size", text="Font Size")

        col = layout.column(align=True)

        col.label(text="Width")
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(preferences, "PREVIEWER_Width_Mode", text="Width Mode", expand=True)
        if preferences.PREVIEWER_Width_Mode=="RELATIVE":
            col.prop(preferences, "PREVIEWER_Width_Rel", text="Display")
        if preferences.PREVIEWER_Width_Mode=="ABSOLUTE":
            col.prop(preferences, "PREVIEWER_Width_Abs", text="Width")


        col = layout.column(align=True)

        col.label(text="Offset")
        row = col.row(align=True)
        row.prop(preferences, "PREVIEWER_Offset_Mode", text="Mode", expand=True)

        row = col.row(align=True)

        if preferences.PREVIEWER_Offset_Mode == "RELATIVE":
            row.prop(preferences, "PREVIEWER_Offset_X_Rel", text="X Position")
            row.prop(preferences, "PREVIEWER_Offset_Y_Rel", text="Y Position")

        if preferences.PREVIEWER_Offset_Mode == "ABSOLUTE":
            row.prop(preferences, "PREVIEWER_Offset_X_Abs", text="X Position")
            row.prop(preferences, "PREVIEWER_Offset_Y_Abs", text="Y Position")

        col = layout.column(align=True)

        col.label(text="Border")

        col.prop(preferences, "PREVIEWER_Border_Thickness", text="Thickness")
        col.separator()
        row = col.row(align=True)
        row.prop(preferences, "PREVIEWER_Border_Color_Normal", text="Normal")
        row = col.row(align=True)
        row.prop(preferences, "PREVIEWER_Border_Color_Hover", text="Activate")






























    def draw_general(self, context, layout):

        col = layout.column(align=True)

        col.label(text="Panels")


        col.prop(self, "PANEL_Camera_List_Panel", text="Viewfinder Operators Panel")
        if self.PANEL_Viewfinder_Operators_Panel:

            col.prop(self, "PANEL_Camera_List_Panel_Category", text="Category")
            col.prop(self, "PANEL_Camera_List_Panel_Label", text="Label")

        col.separator()

        col.prop(self, "PANEL_Viewfinder_Operators_Panel", text="Viewfinder Operators Panel")
        if self.PANEL_Viewfinder_Operators_Panel:

            col.prop(self, "PANEL_Viewfinder_Operators_Panel_Category", text="Category")
            col.prop(self, "PANEL_Viewfinder_Operators_Panel_Label", text="Label")


        col.separator()

        col.prop(self, "PANEL_Camera_Previewer_Panel", text="Viewfinder Previewer Panel")
        if self.PANEL_Camera_Previewer_Panel:

            col.prop(self, "PANEL_Camera_Previewer_Panel_Category", text="Category")
            col.prop(self, "PANEL_Camera_Previewer_Panel_Label", text="Label")


        col.separator()




    def draw_add_operators(self, context, layout):

        col = layout.column(align=True)

        col.prop(self, "Add_Menu", text="Use Camera Menu")
        col.separator()
        if self.Add_Menu:
            col.label(text="Add Menu Operators")
            col.prop(self, "OP_Front_Camera", text="Front Camera")
            col.prop(self, "OP_Top_Camera", text="Top Camera")
            col.prop(self, "OP_Camera_From_View", text="Camera From View")
            col.prop(self, "OP_Camera_Booth", text="Camera Booth")
            col.prop(self, "OP_Camera_And_Empty_Target", text="Camera And Empty Target")
            col.prop(self, "OP_Target_Empty_From_Selected", text="Empty From Selected")
            col.prop(self, "OP_Marker_From_Selected_Camera", text="Marker From Selected Camera")
            col.prop(self, "OP_Clamped_Camera_From_Selected_Curve", text="Clamped Camera From Selected Curve")
            col.prop(self, "OP_Camera_Preset", text="Camera Setup")


    def draw_hotkey(self, context, layout):
        draw_keymaps(self, context, layout)

        # layout.label(text="3D View")
        # kc = context.window_manager.keyconfigs.user
        # km = kc.keymaps['3D View']
        # keymap_items = km.keymap_items

        # kmi = get_menu(km, 'wm.call_menu', 'VIEWFINDER_MT_viewfinder_menu')
        # kmi.show_expanded = False

        # rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)



        # layout.label(text="Camera Preview")
        # kc = context.window_manager.keyconfigs.user
        # km = kc.keymaps['3D View']
        # keymap_items = km.keymap_items
        # kmi = km.keymap_items.new("viewfinder.preview_camera", type="ACCENT_GRAVE", value="PRESS", shift=True, ctrl=True, alt=True)
        # kmi.show_expanded = False

        # rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)




    def draw(self, context):

        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "TABS_Preferences", expand=True)

        box = col.box()

        if self.TABS_Preferences == "GENERAL":
            self.draw_general(context, box)
        if self.TABS_Preferences == "KEYMAPS":
            self.draw_hotkey(context, box)
        if self.TABS_Preferences == "ADD_OPERATOR":
            self.draw_add_operators(context, box)
        if self.TABS_Preferences == "PREVIEWER":
            self.draw_previewer_settings(context, box)





classes = [Viewfinder_user_preferences]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)



    update_panel(None, bpy.context)
    set_keymaps()

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    unset_keymaps()

if __name__ == "__main__":
    register()
