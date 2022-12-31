import bpy
import mathutils
import numpy
import os
import bpy_extras
import bmesh
import platform
import subprocess

import pathlib

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


def draw_operators(context, layout):

    scn = context.scene
    Viewfinder_Scene_Properties = scn.Viewfinder_Scene_Properties 


    col = layout.column(align=True)

    col.scale_y = 2
    operator = col.operator("viewfinder.create_camera_from_view", text="Camera From View", icon="RESTRICT_VIEW_ON")


    layout.label(text="Create Camera", icon="PLUS")
    col = layout.column(align=True)

    col.scale_y = 2

    row = col.row(align=True)

    operator = col.operator("viewfinder.add_camera_and_empty_target", text="With Empty Target", icon="CON_CAMERASOLVER")
    operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

    operator = row.operator("viewfinder.add_aligned_camera", text="Front", icon="VIEW_CAMERA")
    operator.side = "FRONT"
    operator.Angle = 0
    operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

    operator = row.operator("viewfinder.add_aligned_camera", text="Top", icon="VIEW_CAMERA")
    operator.side = "TOP"
    operator.Angle = 0
    operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic

    col.separator()

    operator = col.operator("viewfinder.add_camera_booth", text="Camera Booth Setup", icon="SPHERE")
    operator.Use_Orthographic = Viewfinder_Scene_Properties.Align_Cam_Use_Orthographic


    col = layout.column(align=True)
    col.scale_y = 1

    col.prop(Viewfinder_Scene_Properties, "Align_Cam_Use_Orthographic", text="Use Orthographic", expand=False)


    col.separator()
    col.separator()

    col.label(text="Create Camera Setup", icon="PRESET")
    col.operator("viewfinder.create_curve_fly_through_cam", text="Curve Cam Fly Through", icon="CON_CLAMPTO")
    col.operator("viewfinder.create_curve_cam_with_aim", text="Curve Cam With Aim", icon="CON_CLAMPTO")


    layout.separator()



    col.separator()
    col.separator()




    col.label(text="Constraint Selected Cameras", icon="CONSTRAINT")

    col.operator("viewfinder.constraint_camera_to_curve", text="To Selected Curve", icon="CONSTRAINT")
    col.operator("viewfinder.track_constraint_selected_camera_to_active", text="Track To Active Object", icon="CON_TRACKTO")

    col.separator()
    col.separator()

    col.label(text="Selected Camera Utility", icon="RESTRICT_SELECT_OFF")

    col.operator("viewfinder.selected_camera_to_view", text="Selected Camera To View", icon="CAMERA_DATA")
    col.operator("viewfinder.frame_active_camera_to_selected_objects", text="Frame Active Camera To Selected Objects", icon="CAMERA_DATA")
    col.separator()
    col.separator()

    col.label(text="From Selected", icon="ADD")

    col.operator("viewfinder.create_camera_target_empties", text="Create Empty Targets", icon="EMPTY_AXIS")
    col.operator("viewfinder.create_markers_from_selected_camera", text="Create Markers", icon="PMARKER_ACT")

    col.separator()

    col.operator("viewfinder.create_constrainted_camera_from_selected_curves", text="Create Camera From Curves", icon="CAMERA_DATA")
    col.operator("viewfinder.create_and_constraint_curve_from_selected_camera", text="Create Curve From Camera", icon="CON_CLAMPTO")


    col.separator()
    col.separator()

    col.label(text="Scene Camera Utility", icon="SCENE_DATA")

    col.operator("view3d.camera_to_view_selected", text="Frame Selected Objects", icon="MESH_PLANE")
    col.operator("view3d.camera_to_view", text="Scene Camera To View", icon="CAMERA_DATA")




def Set_Still_Render_Item_Properties(still_render_item, name, resolution_x, resolution_y, camera, frame, render_directory, filename, use_name, image_format, render_this, film_transparent, render_at_frame, engine, use_compositing, use_sequencer):
    still_render_item.name = name
    still_render_item.resolution_x = resolution_x
    still_render_item.resolution_y = resolution_y
    still_render_item.camera = camera
    still_render_item.frame = frame
    still_render_item.render_at_frame = render_at_frame
    still_render_item.engine = engine
    still_render_item.render_directory = render_directory
    still_render_item.filename = filename
    still_render_item.use_name = use_name
    still_render_item.image_format

def View_Render(context):

    scn = context.scene
    render = scn.render

    Scene_Properties = scn.Viewfinder_Scene_Properties


    if Scene_Properties.Still_Render_Show_Render_After_Render:
        bpy.ops.render.view_show("INVOKE_DEFAULT")

def open_file(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def Open_File_List(self, context):

    scn = context.scene
    render = scn.render
    Scene_Properties = scn.Viewfinder_Scene_Properties

    for path in self.open_file_list:
        open_file(path)

def Render_Save_Image_Bool(self, context, save_image_bool):

    scn = context.scene
    render = scn.render
    Scene_Properties = scn.Viewfinder_Scene_Properties


    if save_image_bool:

        dirname = os.path.dirname(render.filepath)
        render_directory = pathlib.Path(dirname)
        message = None

        if dirname:
            render_directory.mkdir(parents=True, exist_ok=True)

            if os.path.isdir(str(render_directory)):

                bpy.ops.render.render(use_viewport=True, write_still=Scene_Properties.Still_Render_Save_Image)
                self.open_file_list.add(os.path.dirname(render.filepath))

            else:
                message = "Fail to Render, Invalid Path"

        else:
            message = "Fail to Render, Empty Path"

        if message:
            self.report({"ERROR"}, message)

    else:
        bpy.ops.render.render(use_viewport=True)

def Render_Save_Image(self, context):


    scn = context.scene
    render = scn.render
    Scene_Properties = scn.Viewfinder_Scene_Properties

    Render_Save_Image_Bool(self, context, Scene_Properties.Still_Render_Save_Image)


def Render_Slot_Increment(self, context):

    scn = context.scene
    render = scn.render
    Scene_Properties = scn.Viewfinder_Scene_Properties


    for image in bpy.data.images:

        if image.type == "RENDER_RESULT":

            if self.first_loop:

                self.first_loop = False

                image.render_slots.active_index = 0

            else:

                if len(image.render_slots) > image.render_slots.active_index + 1:
                    image.render_slots.active_index += 1
                else:
                    image.render_slots.new(name="Slot " + str(len(image.render_slots)+1))
                    image.render_slots.active_index = len(image.render_slots) -1
                break


def Set_Still_Render_Settings(context, still_render_item):

    scn = context.scene
    render = scn.render

    render.resolution_percentage = still_render_item.resolution_percentage
    render.resolution_x = still_render_item.resolution_custom_x
    render.resolution_y = still_render_item.resolution_custom_y
    scn.camera = still_render_item.camera

    if still_render_item.render_at_frame:
        scn.frame_current = still_render_item.frame

    if still_render_item.engine == "EEVEE":
        render.engine = "BLENDER_EEVEE"
    if still_render_item.engine == "CYCLES":
        render.engine = "CYCLES"
    if still_render_item.engine == "WORKBENCH":
        render.engine = "BLENDER_WORKBENCH"

    render.film_transparent = still_render_item.film_transparent

    render.filepath = still_render_item.output_path

    render.image_settings.file_format = still_render_item.image_format.file_format

    render.use_compositing = still_render_item.use_compositing
    render.use_sequencer = still_render_item.use_sequencer

    render.image_settings.color_mode = still_render_item.image_format.color_mode

    if still_render_item.image_format.file_format in ["PNG", "JPEG2000", "DPX", "OPEN_EXR_MULTILAYER", "OPEN_EXR", "TIFF"]:
        render.image_settings.color_depth = still_render_item.image_format.color_depth

    if still_render_item.image_format.file_format in ["PNG"]:
        render.image_settings.compression = still_render_item.image_format.compression

    if still_render_item.image_format.file_format in ["JPEG", "JPEG2000"]:
        render.image_settings.quality = still_render_item.image_format.quality

    if still_render_item.image_format.file_format in ["JPEG2000"]:
        render.image_settings.jpeg2k_codec = still_render_item.image_format.jpeg2k_codec
        render.image_settings.use_jpeg2k_cinema_preset = still_render_item.image_format.use_jpeg2k_cinema_preset
        render.image_settings.use_jpeg2k_cinema_48 = still_render_item.image_format.use_jpeg2k_cinema_48
        render.image_settings.use_jpeg2k_ycc = still_render_item.image_format.use_jpeg2k_ycc

    if still_render_item.image_format.file_format in ["DPX"]:
        render.image_settings.use_cineon_log = still_render_item.image_format.use_cineon_log

    if still_render_item.image_format.file_format in ["OPEN_EXR_MULTILAYER", "OPEN_EXR"]:
        render.image_settings.exr_codec = still_render_item.image_format.exr_codec
        render.image_settings.use_preview = still_render_item.image_format.use_preview

    if still_render_item.image_format.file_format in ["OPEN_EXR"]:
        render.image_settings.use_zbuffer = still_render_item.image_format.use_zbuffer

    if still_render_item.image_format.file_format in ["TIFF"]:
        render.image_settings.tiff_codec = still_render_item.image_format.tiff_codec















def Restore_Render_Settings(context, SAVED_Render_Settings):

    scn = context.scene
    render = scn.render

    render.image_settings.file_format = SAVED_Render_Settings["SAVE_File_Format"]
    render.image_settings.color_mode = SAVED_Render_Settings["SAVE_Color_Mode"]
    render.image_settings.color_depth = SAVED_Render_Settings["SAVE_Color_Depth"]
    render.image_settings.compression = SAVED_Render_Settings["SAVE_Compression"]
    render.image_settings.quality = SAVED_Render_Settings["SAVE_Quality"]

    render.image_settings.jpeg2k_codec = SAVED_Render_Settings["SAVE_JPEG2K_Codec"]
    render.image_settings.use_jpeg2k_cinema_preset = SAVED_Render_Settings["SAVE_JPEG2K_Cinema_Preset"]
    render.image_settings.use_jpeg2k_cinema_48 = SAVED_Render_Settings["SAVE_JPEG2K_Cinema_48"]
    render.image_settings.use_jpeg2k_ycc = SAVED_Render_Settings["SAVE_JPEG2K_Cinema_YCC"]

    render.image_settings.use_cineon_log = SAVED_Render_Settings["SAVE_Use_Cineon_Log"]

    render.image_settings.tiff_codec = SAVED_Render_Settings["SAVE_Use_TIFF_Codec"]
    render.image_settings.exr_codec = SAVED_Render_Settings["SAVE_Use_EXR_Codec"]

    render.image_settings.use_zbuffer = SAVED_Render_Settings["SAVE_Use_ZBuffer"]
    render.image_settings.use_preview = SAVED_Render_Settings["SAVE_Use_Preview"]


    render.resolution_x = SAVED_Render_Settings["SAVE_Resolution_X"]
    render.resolution_y = SAVED_Render_Settings["SAVE_Resolution_Y"]
    render.resolution_percentage = SAVED_Render_Settings["SAVE_Resolution_Percentage"]

    scn.camera = SAVED_Render_Settings["SAVE_Camera"]
    scn.frame_current = SAVED_Render_Settings["SAVE_Frame"]
    render.engine = SAVED_Render_Settings["SAVE_engine"]

    render.filepath = SAVED_Render_Settings["SAVE_Filepath"]
    render.film_transparent = SAVED_Render_Settings["SAVE_Film_Transparent"]

    render.use_compositing = SAVED_Render_Settings["SAVE_Use_Compositing"]
    render.use_sequencer = SAVED_Render_Settings["SAVE_Use_Sequencer"]



def Save_Render_Settings(context):

    scn = context.scene
    render = scn.render

    Scene_Properties = scn.Viewfinder_Scene_Properties
    item_list = Scene_Properties.Still_Render_List


    SAVED_Render_Settings = {}

    SAVED_Render_Settings["SAVE_File_Format"] = render.image_settings.file_format
    SAVED_Render_Settings["SAVE_Color_Mode"] = render.image_settings.color_mode
    SAVED_Render_Settings["SAVE_Color_Depth"] = render.image_settings.color_depth
    SAVED_Render_Settings["SAVE_Compression"] = render.image_settings.compression
    SAVED_Render_Settings["SAVE_Quality"] = render.image_settings.quality

    SAVED_Render_Settings["SAVE_JPEG2K_Codec"] = render.image_settings.jpeg2k_codec
    SAVED_Render_Settings["SAVE_JPEG2K_Cinema_Preset"] = render.image_settings.use_jpeg2k_cinema_preset
    SAVED_Render_Settings["SAVE_JPEG2K_Cinema_48"] = render.image_settings.use_jpeg2k_cinema_48
    SAVED_Render_Settings["SAVE_JPEG2K_Cinema_YCC"] = render.image_settings.use_jpeg2k_ycc

    SAVED_Render_Settings["SAVE_Use_Cineon_Log"] = render.image_settings.use_cineon_log

    SAVED_Render_Settings["SAVE_Use_TIFF_Codec"] = render.image_settings.tiff_codec
    SAVED_Render_Settings["SAVE_Use_EXR_Codec"] = render.image_settings.exr_codec

    SAVED_Render_Settings["SAVE_Use_ZBuffer"] = render.image_settings.use_zbuffer
    SAVED_Render_Settings["SAVE_Use_Preview"] = render.image_settings.use_preview

    SAVED_Render_Settings["SAVE_Resolution_X"] = render.resolution_x
    SAVED_Render_Settings["SAVE_Resolution_Y"] = render.resolution_y
    SAVED_Render_Settings["SAVE_Resolution_Percentage"] = render.resolution_percentage

    SAVED_Render_Settings["SAVE_Camera"] = scn.camera
    SAVED_Render_Settings["SAVE_Frame"] = scn.frame_current
    SAVED_Render_Settings["SAVE_engine"] = render.engine

    SAVED_Render_Settings["SAVE_Filepath"] = render.filepath
    SAVED_Render_Settings["SAVE_Film_Transparent"] = render.film_transparent

    SAVED_Render_Settings["SAVE_Use_Compositing"] = render.use_compositing
    SAVED_Render_Settings["SAVE_Use_Sequencer"] = render.use_sequencer

    return SAVED_Render_Settings








def get_selected_object_type(context, type, exclude_active=False):

    selected = [object for object in context.selected_objects if object.type in type]

    if exclude_active:

        object = context.active_object

        if object in selected:
            selected.remove(object)

    return selected



def get_addon_name():

    return addon_name

def get_addon_preferences():

    addon_preferences = bpy.context.preferences.addons[addon_name].preferences

    return addon_preferences


def Create_Empty(name):

    object = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(object)

    return object

#Preferences


def get_object_indices(object):

    if object.type == "MESH":
        indices = [vertex.index for vertex in object.data.vertices]
        return indices

    else:
        return None

#Assets

def append_object(filepath, object_name):

    blendfile = filepath
    section   = "\\Object\\"
    object    = object_name

    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(filename=filename, directory=directory)
    selected_objects = [object for object in bpy.context.selected_objects]

    bpy.context.view_layer.objects.active = selected_objects[0]

    if len(selected_objects) == 0:
        return None

    if len(selected_objects) == 1:
        return selected_objects[0]

    if len(selected_objects) > 1:
        return selected_objects

def get_asset_folder():

    script_file = os.path.realpath(__file__)
    addon_directory = os.path.dirname(script_file)
    Assets_Folder = os.path.join(addon_directory, "Assets")

    return Assets_Folder

def get_asset_file(filename):

    Assets_Folder = get_asset_folder()
    filepath = os.path.join(Assets_Folder, filename)

    return filepath

#UI
def update_UI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()





def draw_subpanel(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_left(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_LEFT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_style02(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_LEFT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_checkbox(self, boolean, property, self2, property2, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text="", emboss=False, icon=ICON)
    row.prop(self2, property2, text="")
    row.prop(self, property, text=label, emboss=False)

    return boolean

#Calculation

def get_bounding_box(object):

    bbox_corners = [object.matrix_world * mathutils.Vector(corner) for corner in object.bound_box]

    return bbox_corners

def midpoint(coordinates, mode):

    if len(coordinates) > 0:

        if mode == "BOUNDING_BOX":

            x= []
            y= []
            z= []

            for coordinate in coordinates:
                x.append(coordinate[0])
                y.append(coordinate[1])
                z.append(coordinate[2])

            range_x = (max(x), min(x))
            range_y = (max(y), min(y))
            range_z = (max(z), min(z))

            bounding_box_coordinate = []

            for a in range_x:
                for b in range_y:
                    for c in range_z:
                        bounding_box_coordinate.append((a, b, c))

            return mathutils.Vector(numpy.array(bounding_box_coordinate).mean(axis=0))

        if mode == "CENTER":
            return mathutils.Vector(numpy.array(coordinates).mean(axis=0))
    else:
        return None

def Set_Tags(Tag_Name, object):

    scn = bpy.context.scene
    scn_properties = scn.Radiant_Light_Properties

    Tags_List = scn_properties.Tags_List
    Tags_Check = [Tag.name for Tag in scn_properties.Tags_List]

    if not Tag_Name in Tags_Check:
        scn_properties.Tags_List_Index = len(Tags_List)
        Item = Tags_List.add()
        Item.name = Tag_Name

    object.Radiant_Light_Properties.Tags = Tag_Name

def get_selected_midpoint(mode="BOUNDING_BOX"):

    points = [obj.matrix_world.to_translation() for obj in bpy.context.selected_objects]

    location = (0, 0, 0)

    if len(points) > 0:
        location = midpoint(points, mode)

    return location

def get_object_center(object, mode):

    if mode == "ORIGIN":
        # return object.matrix_world.inverted() @ object.location
        return object.matrix_world.inverted() @ object.matrix_world.to_translation()

    if mode in ["CENTER", "BOUNDING_BOX"]:

        if not object.type in ["MESH","CURVE" , "ARMATURE"]:
            # return object.matrix_world.inverted() @ object.location
            return object.matrix_world.inverted() @ object.matrix_world.to_translation()

        if object.type == "MESH":
            # create_lists = [object.matrix_world @ vert.co for vert in object.data.vertices]
            create_lists = [vert.co for vert in object.data.vertices]

        if object.type == "CURVE":

            create_lists = []

            for spline in object.data.splines:

                for point in spline.points:
                    # create_lists.append(object.matrix_world @ point.co)
                    create_lists.append(point.co.xyz)

                for bezier_point in spline.bezier_points:
                    # create_lists.append(object.matrix_world @ bezier_point.co)
                    create_lists.append(bezier_point.co.xyz)

        if object.type == "ARMATURE":

            create_lists = []

            for bone in object.data.bones:
                # create_lists.append(object.matrix_world @ bone.head)
                # create_lists.append(object.matrix_world @ bone.tail)

                create_lists.append(bone.head)
                create_lists.append(bone.tail)

        if mode == "CENTER":
            return midpoint(create_lists, "CENTER")

        if mode == "BOUNDING_BOX":
            return midpoint(create_lists, "BOUNDING_BOX")

def Blackbody_Color(t):

    blackbody_table_r = [
        [2.52432244e+03, -1.06185848e-03, 3.11067539e+00],
        [3.37763626e+03, -4.34581697e-04, 1.64843306e+00],
        [4.10671449e+03, -8.61949938e-05, 6.41423749e-01],
        [4.66849800e+03, 2.85655028e-05, 1.29075375e-01],
        [4.60124770e+03, 2.89727618e-05, 1.48001316e-01],
        [3.78765709e+03, 9.36026367e-06, 3.98995841e-01],
    ];

    blackbody_table_g = [
        [-7.50343014e+02, 3.15679613e-04, 4.73464526e-01],
        [-1.00402363e+03, 1.29189794e-04, 9.08181524e-01],
        [-1.22075471e+03, 2.56245413e-05, 1.20753416e+00],
        [-1.42546105e+03, -4.01730887e-05, 1.44002695e+00],
        [-1.18134453e+03, -2.18913373e-05, 1.30656109e+00],
        [-5.00279505e+02, -4.59745390e-06, 1.09090465e+00],
    ];

    blackbody_table_b = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [-2.02524603e-11, 1.79435860e-07, -2.60561875e-04, -1.41761141e-02],
        [-2.22463426e-13, -1.55078698e-08, 3.81675160e-04, -7.30646033e-01],
        [6.72595954e-13, -2.73059993e-08, 4.24068546e-04, -7.52204323e-01],
    ];


    if t >= 12000.0:
        return [0.826270103, 0.994478524, 1.56626022];
    if t < 965.0:
        return [4.70366907, 0.0, 0.0]

    i = 0
    if t >= 6365.0:
        i = 5
    elif t >= 3315.0:
        i = 4
    elif t >= 1902.0:
        i = 3
    elif t >= 1449.0:
        i = 2
    elif t >= 1167.0:
        i = 1
    else:
        i = 0

    r = blackbody_table_r[i]
    g = blackbody_table_g[i]
    b = blackbody_table_b[i]

    t_inv = 1 / t
    return [r[0] * t_inv + r[1] * t + r[2],
           g[0] * t_inv + g[1] * t + g[2],
           ((b[0] * t + b[1]) * t + b[2]) * t + b[3]]

#Normals Calculation

def Average_Normals(Normals):
    average_normals = mathutils.Vector(numpy.sum(Normals, axis=0) / len(Normals))
    return average_normals

def Normal_To_Orientation(object, location, normal):

    mw = object.matrix_world.copy()

    o = location
    axis_src = normal
    axis_dst = mathutils.Vector((0, 0, -1))

    matrix_rotate = mw.to_3x3()
    matrix_rotate = matrix_rotate @ axis_src.rotation_difference(axis_dst).to_matrix().inverted()
    matrix_translation = mathutils.Matrix.Translation(mw @ o)

    Normal_Matrix = matrix_translation @ matrix_rotate.to_4x4()

    return Normal_Matrix




def Face_To_Orientation(obj, face):

    mw = obj.matrix_world.copy()

    if bpy.context.mode == "EDIT_MESH":
        bm = bmesh.from_edit_mesh(obj.data)
    else:
        bm = bmesh.new()
        bm.from_mesh(obj.data)

    bm.faces.ensure_lookup_table()
    face = bm.faces[face.index]
    o = face.calc_center_median()

    axis_src = face.normal
    axis_src2 = face.calc_tangent_edge()
    axis_dst = mathutils.Vector((0, 0, -1))
    axis_dst2 = mathutils.Vector((0, 1, 0))

    vec2 = axis_src @ obj.matrix_world.inverted()
    matrix_rotate = axis_dst.rotation_difference(vec2).to_matrix().to_4x4()

    vec1 = axis_src2 @ obj.matrix_world.inverted()
    axis_dst2 = axis_dst2 @ matrix_rotate.inverted()
    mat_tmp = axis_dst2.rotation_difference(vec1).to_matrix().to_4x4()
    matrix_rotate = mat_tmp @ matrix_rotate
    matrix_translation = mathutils.Matrix.Translation(mw @ o) #

    return matrix_translation @ matrix_rotate.to_4x4()












def Normal_To_Offset(object, location, normal, offset):

    mw = object.matrix_world.copy()

    o = location
    axis_src = normal
    axis_dst = mathutils.Vector((0, 0, 1))

    matrix_rotate = mw.to_3x3()
    matrix_rotate = matrix_rotate @ axis_src.rotation_difference(axis_dst).to_matrix().inverted()
    matrix_translation = mathutils.Matrix.Translation(mw @ o)

    Normal_Matrix = matrix_translation @ matrix_rotate.to_4x4() @ mathutils.Vector(offset)
    Normal_Offset = object.matrix_world.inverted() @ Normal_Matrix

    return Normal_Offset

#Utility

def object_switch_mode(object, mode):

    bpy.context.view_layer.update()

    Previous_Mode = object.mode

    if not object.visible_get():

        if not bpy.context.collection.objects.get(object.name):

            bpy.context.collection.objects.link(object)



    object.hide_viewport = False
    object.hide_set(False)

    object.hide_select = False

    if object.visible_get():

        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.mode_set(mode=mode, toggle=False)

        return Previous_Mode

def get_objects(mode, context):

    objects = context.selected_objects

    if mode == "EDIT_MESH":
        objects = [object for object in context.objects_in_mode]

    if mode == "OBJECT":
        objects = [object for object in context.selected_objects]

    return objects

def Add_Aim_Constraint(object, target):
    constraint = object.constraints.new("TRACK_TO")
    constraint.target = target

    return constraint

def Apply_Constraint(object, constraint):

    bpy.context.view_layer.update()
    mw = object.matrix_world.copy()
    object.constraints.remove(constraint)
    object.matrix_world = mw

#Create Object

def Create_Target_Empty(name, collection=None):

    object = bpy.data.objects.new(name, None)

    if collection:
        collection.objects.link(object)
    else:
        bpy.context.collection.objects.link(object)

    return object

def Create_Light_Data(name, type):
    data = bpy.data.lights.new(name, type)
    return data

def Create_Light(name, type="SUN", light_data=None, collection=None):

    if light_data:
        light = light_data
    else:
        light = bpy.data.lights.new(name, type=type)

    object = bpy.data.objects.new(name, light)


    if collection:
        collection.objects.link(object)
    else:
        bpy.context.collection.objects.link(object)

    return object


def Create_Camera(name, collection=None):

    camera = bpy.data.cameras.new(name)
    object = bpy.data.objects.new(name, camera)

    if collection:
        collection.objects.link(object)
    else:
        bpy.context.collection.objects.link(object)

    return object



#Collection
def Find_Or_Create_Collection(use_collection, name):

    bpy.context.view_layer.update()

    Collection = None

    if use_collection:

        Collection = bpy.data.collections.get(name)

        if not Collection:
            Collection = bpy.data.collections.new(name)
            bpy.context.collection.children.link(Collection)

    return Collection

#Nodes
def Get_Node_Inputs(node, slots):

    input = [link.from_node for link in node.inputs[slots].links]
    if len(input) == 0:
        return None
    else:
        return input[0]

def New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot):

    nodes = node_tree.nodes
    new_node = nodes.new(node_type)
    new_node.location = from_node.location
    new_node.location.x -= 250

    node_tree.links.new(from_node.inputs[from_slot], new_node.outputs[to_slot])

    return new_node

def New_Node_To_Slot_Conflict_Check(node_tree, node_type ,from_node, from_slot, to_slot, conflict_solver):

    input_check = Get_Node_Inputs(from_node, from_slot)

    conflict = None

    if input_check:
        if input_check.type == node_type.replace("ShaderNode", "").upper():
            new_node = input_check

        else:

            if conflict_solver == "SKIP":
                message = "Node Tree Confict, Operation Skipped"

                new_node = None
                conflict = message

                return {"node": new_node, "conflict": conflict}

            if conflict_solver == "FORCE":

                new_node = New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot)
                message = "Disconnected " + input_check.name + " and reconnected " + new_node.name + " to " + from_node.name
                conflict = message

                return {"node": new_node, "conflict": conflict}

    else:
        new_node = New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot)
        conflict = None

        return {"node": new_node, "conflict": conflict}

    return {"node": new_node, "conflict": conflict}

def get_input_nodes(self, node, types):

    for input in node.inputs:
        for link in input.links:

            from_node = link.from_node

            get_input_nodes(self, from_node, types)

            if from_node.type in types:
                self.is_emission = True
                self.input_nodes.append(from_node)

def find_input_nodes(self, data, types):

    self.input_nodes = []
    self.is_emission = False

    node_tree = data.node_tree
    output_node = node_tree.get_output_node('CYCLES')

    for input in output_node.inputs:
        for link in input.links:

            from_node = link.from_node

            get_input_nodes(self, from_node, types)

            if from_node.type == "EMISSION":
                self.is_emission = True

            if from_node.type in types:
                self.is_emission = True
                self.input_nodes.append(from_node)



def Append_New_Emission_Material(object, color=(1, 1, 1, 1), strength=1000):

    material = bpy.data.materials.new(object.name)
    object.data.materials.append(material)
    material.use_nodes = True

    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    output_node = material.node_tree.get_output_node("ALL")

    material.node_tree.nodes.remove(principled_bsdf)
    emission = material.node_tree.nodes.new(type="ShaderNodeEmission")

    material.node_tree.links.new(emission.outputs["Emission"], output_node.inputs["Surface"])

    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength

    return material



def check_bone_select(bone, mode):

    if mode == "EDIT_ARMATURE":
        return bone.select

    if mode == "POSE":
        return bone.bone.select

def create_cube(name="Cube"):

    mesh = bpy.data.meshes.new(name)
    object = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(object)

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(mesh)
    bm.free()

    return object
