import bpy
from Viewfinder import Utility_Functions
import mathutils
import math

OPERATOR_POLL_CONTEXT = ["OBJECT","EDIT_MESH","EDIT_CURVE","EDIT_ARMATURE", "POSE"]
bezier_point_type = ["BEZIER"]
point_type = ["POLY", "NURBS"]

#---------------------ENUM AREA---------------------

def ENUM_Aim_Target_Type(self, context):

    items = [("EDITING","Editing Object","Editing Object"),("ELEMENT","Element","Element"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    if self.Mode == "INDIVIDUAL":

        if context.mode == "OBJECT":
            items = [("EDITING","Reference Object","Reference Object"), ("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]
        if context.mode == "EDIT_MESH":
            items = [("EDITING","Editing Object","Editing Object"),("ELEMENT","Element","Element"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    if self.Mode == "MEDIAN":

        if context.mode == "OBJECT":
            items = [("ELEMENT","Midpoint","Midpoint"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]
        if context.mode == "EDIT_MESH":
            items = [("ELEMENT","Midpoint","Midpoint"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    return items

def ENUM_Orientation_Mode(self, context):

    ENUM_Items = [("GLOBAL","Global","Global")]

    if self.Mode == "INDIVIDUAL":

        ENUM_Items.append(("LOCAL","Local","Local"))

        if context.mode == "EDIT_MESH":
            ENUM_Items.append(("NORMAL" ,"Normal" ,"Normal"))

        if context.mode in ["EDIT_ARMATURE", "POSE"]:
            ENUM_Items.append(("BONE" ,"Bone" ,"Bone"))

    # ENUM_Items.append(("TRACK_TO","Track to","Track To"))
    ENUM_Items.append(("CURSOR","3D Cursor","3D Cursor"))

    return ENUM_Items

ENUM_Mode = [("INDIVIDUAL","Individual","Individual"),("MEDIAN","Median","Median")]

ENUM_Position_Mode = [("ORIGIN","Origin","Origin"),("CENTER","Geometry","Geometry"),("BOUNDING_BOX","Bounding Box","Bounding Box")]

ENUM_ELEM_Mesh = [("VERTEX","Vertices","Vertices"),("EDGES","Edges","Edges"),("FACE","Faces","Faces")]

ENUM_ELEM_Armature = [("CENTER","Center","Center"),("HEAD","Head","Head"),("TAIL","Tail","Tail")]

ENUM_Area_Shape = [("SQUARE","Square","Square"),("RECTANGLE","Rectangle","Rectangle"),("DISK","Disk","Disk"),("ELLIPSE","Ellipse","Ellipse")]

#---------------------ENUM AREA---------------------

class VIEWFINDER_OT_Create_Camera_From_Selected(bpy.types.Operator):
    """Create Light At Selected"""
    bl_idname = "viewfinder.create_camera_from_selected"
    bl_label = "Create Camera from Selected"
    bl_options = {'UNDO', 'REGISTER'}

    Base_Name: bpy.props.StringProperty(default="Camera")

    Mode: bpy.props.EnumProperty(items=ENUM_Mode)

    Position_Mode: bpy.props.EnumProperty(items=ENUM_Position_Mode)


    Orientation: bpy.props.EnumProperty(items=ENUM_Orientation_Mode)

    ELEM_Mesh: bpy.props.EnumProperty(default="VERTEX", items=ENUM_ELEM_Mesh)
    ELEM_Armature: bpy.props.EnumProperty(default="HEAD", items=ENUM_ELEM_Armature)
    ELEM_Handle: bpy.props.BoolProperty(default=False)

    Parent: bpy.props.BoolProperty(default=False)

    Use_Hierarchy: bpy.props.BoolProperty(default=True)

    SHOW_Track_to: bpy.props.BoolProperty()

    SHOW_Collection: bpy.props.BoolProperty()
    Use_Collection: bpy.props.BoolProperty(default=False)
    Use_Collection_Picker: bpy.props.BoolProperty(default=True)
    Collection_Name: bpy.props.StringProperty()

    SHOW_Offset: bpy.props.BoolProperty()
    use_offset: bpy.props.BoolProperty(default=True)
    offset: bpy.props.FloatVectorProperty(default=(0, 0, 0))
    rotation: bpy.props.FloatVectorProperty(default=(0, 0, 0), subtype="EULER")

    normal_offset: bpy.props.FloatProperty(default=0)


    flip_direction: bpy.props.BoolProperty(default=False)

    child_bone_pair = []

    @classmethod
    def poll(cls, context):
        if context.mode in OPERATOR_POLL_CONTEXT:
            return True

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    def draw_offset(self, context, layout):

        if Utility_Functions.draw_subpanel(self, self.SHOW_Offset, "SHOW_Offset", "Offset", layout):
            col = layout.column(align=True)
            row = col.row()
            row.prop(self, "use_offset", text="Use Offset")

            if self.use_offset:

                if self.Orientation == "NORMAL":
                    row.prop(self, "normal_offset", text="Normal Offset")

                # row = col.row()
                # row.prop(self, "offset", text="Offset")

                row = col.row()
                row.prop(self, "rotation", text="Rotation")


    def draw_collection(self, context, layout):


        col = layout.column(align=True)

        col.prop(self, "Use_Collection", text="Use Collection")

        if self.Use_Collection:

            row = col.row(align=True)

            if self.Use_Collection_Picker:

                row.prop_search(self, "Collection_Name", bpy.data, "collections", text="")
            else:
                row.prop(self, "Collection_Name", text="")
            row.prop(self, "Use_Collection_Picker", text="", icon="EYEDROPPER")


    def draw_name(self, context, layout):
        layout.prop(self, "Base_Name", text="Name")

    def draw_general(self, context, layout):

        row = layout.row()
        row.prop(self, "Mode", expand=True)

        if context.mode == "OBJECT":
            row = layout.row()
            row.prop(self, "Position_Mode", text="")

    def draw_elements(self, context, layout):

        if self.Mode == "INDIVIDUAL":

            if context.mode == "EDIT_MESH":

                layout.prop(self, "ELEM_Mesh", text="")


        if context.mode in ["EDIT_ARMATURE", "POSE"]:

            layout.prop(self, "ELEM_Armature", text="")

    def draw(self, context):

        layout = self.layout

        preferences = Utility_Functions.get_addon_preferences()

        col = layout.column(align=True)

        self.draw_name(context, col)

        col.separator()

        self.draw_general(context, col)

        self.draw_elements(context, col)


        if context.mode in ["EDIT_MESH", "EDIT_CURVE"]:
            col.prop(self, "Parent", text="Parent to Object (Constraint)")

        if context.mode in ["EDIT_ARMATURE", "POSE"]:
            col.prop(self, "Parent", text="Parent to Bone (Constraint)")

        layout.separator()

        layout.prop(self, "Orientation", text="Orientation")

        if context.mode == "EDIT_MESH":
            if self.Mode == "INDIVIDUAL":
                if self.Orientation == "NORMAL":
                    layout.prop(self, "flip_direction", text="Flip Direction")

        self.draw_collection(context, layout)

        self.draw_offset(context, layout)


    def execute(self, context):

        self.child_bone_pair.clear()

        preferences = Utility_Functions.get_addon_preferences()

        mode = context.mode
        orientation = self.Orientation
        position_mode = self.Position_Mode

        flip_direction = self.flip_direction

        selected_objects = context.selected_objects
        active_object = context.object

        context.view_layer.update()

        parent_constraint_pairs = []


        if self.Mode == "MEDIAN":

            points = []
            mid_point = None

            for object in selected_objects:

                if mode == "OBJECT":
                    points.append(object.matrix_world @ Utility_Functions.get_object_center(object, self.Position_Mode))

                if mode == "EDIT_MESH":
                    Utility_Functions.object_switch_mode(object, "OBJECT")

                    if object.type == "MESH":
                        for vertex in object.data.vertices:
                            if vertex.select:
                                points.append(object.matrix_world @ vertex.co)

                if mode == "EDIT_CURVE":
                    Utility_Functions.object_switch_mode(object, "OBJECT")

                    if object.type == "CURVE":

                        for spline in object.data.splines:
                            for point in spline.points:
                                if point.select:
                                    points.append(object.matrix_world @ point.co)

                            for point in spline.bezier_points:
                                if point.select_control_point:
                                    points.append(object.matrix_world @ point.co)

                if mode == "EDIT_ARMATURE":

                    if object.type == "ARMATURE":
                        for bone in object.data.edit_bones:

                            if bone.select:
                                if self.ELEM_Armature == "HEAD":

                                    points.append(object.matrix_world @ bone.head)

                                if self.ELEM_Armature == "TAIL":

                                    points.append(object.matrix_world @ bone.tail)

                                if self.ELEM_Armature == "CENTER":

                                    points.append(object.matrix_world @ bone.head)
                                    points.append(object.matrix_world @ bone.tail)

                if mode == "POSE":
                    if object.type == "ARMATURE":
                        for bone in object.pose.bones:

                            if bone.bone.select:
                                if self.ELEM_Armature == "HEAD":

                                    points.append(object.matrix_world @ bone.head)

                                if self.ELEM_Armature == "TAIL":

                                    points.append(object.matrix_world @ bone.tail)

                                if self.ELEM_Armature == "CENTER":

                                    points.append(object.matrix_world @ bone.head)
                                    points.append(object.matrix_world @ bone.tail)

            if position_mode == "CENTER":
                mid_point = Utility_Functions.midpoint(points, "CENTER")

            if position_mode == "BOUNDING_BOX":
                mid_point = Utility_Functions.midpoint(points, "BOUNDING_BOX")

            if position_mode == "ORIGIN":
                mid_point = Utility_Functions.midpoint(points, "BOUNDING_BOX")

            if mid_point:
                name = self.Base_Name
                rotation_quaternion = (0, 0, 0, 0)
                rotation_euler = (0, 0, 0)

                if orientation == "GLOBAL":
                    rotation_quaternion = (0, 0, 0, 0)
                    rotation_euler = (0, 0, 0)

                if orientation == "CURSOR":
                    rotation_euler = context.scene.cursor.rotation_euler

                collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)


                camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                camera_object.location = mid_point
                camera_object.rotation_euler = rotation_euler



        if self.Mode == "INDIVIDUAL":

            name = self.Base_Name

            for object in selected_objects:

                if mode == "OBJECT":

                    name = self.Base_Name + "_" + object.name

                    mid_point = object.matrix_world @ Utility_Functions.get_object_center(object, self.Position_Mode)

                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                    rotation_euler = (0, 0, 0)

                    if orientation == "GLOBAL":
                        rotation_euler = (0, 0, 0)

                    if orientation == "CURSOR":
                        rotation_euler = context.scene.cursor.rotation_euler

                    if orientation == "LOCAL":
                        rotation_euler = object.matrix_world.to_euler()

                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                    camera_object.location = mid_point
                    camera_object.rotation_euler = rotation_euler

                if mode == "EDIT_MESH":

                    Utility_Functions.object_switch_mode(object, "OBJECT")

                    if object.type == "MESH":

                        if self.ELEM_Mesh == "VERTEX":

                            vert_counter = -1

                            for count, vertex in enumerate(object.data.vertices):
                                if vertex.select:
                                    vert_counter += 1
                                    name = self.Base_Name + "_" + object.name + "_VERTEX_" + str(vert_counter)

                                    position = object.matrix_world @ vertex.co

                                    if orientation == "GLOBAL":
                                        rotation_quaternion = (0, 0, 0, 0)
                                        rotation_euler = (0, 0, 0)

                                    if orientation == "CURSOR":
                                        rotation_euler = context.scene.cursor.rotation_euler

                                    if orientation == "LOCAL":
                                        rotation_euler = object.matrix_world.to_euler()

                                    if orientation == "NORMAL":
                                        normal = vertex.normal
                                        if flip_direction:
                                            normal = -normal

                                        rotation_euler = Utility_Functions.Normal_To_Orientation(object, vertex.co, normal).to_euler()


                                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)


                                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                                    camera_object.location = position
                                    camera_object.rotation_euler = rotation_euler

                                    rotationMAT = mathutils.Euler(rotation_euler).to_matrix()
                                    rotationMAT.invert()
                                    zVector = mathutils.Vector((0, 0, -self.normal_offset)) @ rotationMAT
                                    camera_object.location = camera_object.location + zVector

                                    camera_object.rotation_euler.rotate_axis("X", self.rotation[0])
                                    camera_object.rotation_euler.rotate_axis("Y", self.rotation[1])
                                    camera_object.rotation_euler.rotate_axis("Z", self.rotation[2])


                                    if self.Parent:

                                        constraint = camera_object.constraints.new("CHILD_OF")
                                        constraint.target = object


                        if self.ELEM_Mesh == "EDGES":

                            edge_counter = -1

                            for count, edge in enumerate(object.data.edges):
                                if edge.select:
                                    edge_counter += 1
                                    name = self.Base_Name + "_" + object.name + "_EDGES_" + str(edge_counter)

                                    edge_center = Utility_Functions.midpoint([object.data.vertices[vertex_index].co for vertex_index in edge.vertices], "CENTER")
                                    position = object.matrix_world @ edge_center

                                    average_normal = Utility_Functions.Average_Normals([object.data.vertices[vertex_index].normal for vertex_index in edge.vertices])

                                    if orientation == "GLOBAL":
                                        rotation_quaternion = (0, 0, 0, 0)
                                        rotation_euler = (0, 0, 0)

                                    if orientation == "CURSOR":
                                        rotation_euler = context.scene.cursor.rotation_euler

                                    if orientation == "LOCAL":
                                        rotation_euler = object.matrix_world.to_euler()

                                    if orientation == "NORMAL":
                                        normal = average_normal
                                        if flip_direction:
                                            normal = -normal

                                        rotation_euler = Utility_Functions.Normal_To_Orientation(object, edge_center, normal).to_euler()


                                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                                    camera_object.location = position
                                    camera_object.rotation_euler = rotation_euler

                                    rotationMAT = mathutils.Euler(rotation_euler).to_matrix()
                                    rotationMAT.invert()
                                    zVector = mathutils.Vector((0, 0, -self.normal_offset)) @ rotationMAT
                                    camera_object.location = camera_object.location + zVector

                                    camera_object.rotation_euler.rotate_axis("X", self.rotation[0])
                                    camera_object.rotation_euler.rotate_axis("Y", self.rotation[1])
                                    camera_object.rotation_euler.rotate_axis("Z", self.rotation[2])


                                    if self.Parent:

                                        constraint = camera_object.constraints.new("CHILD_OF")
                                        constraint.target = object


                        if self.ELEM_Mesh == "FACE":

                            face_counter = -1

                            for count, face in enumerate(object.data.polygons):
                                if face.select:
                                    face_counter += 1
                                    position = object.matrix_world @ face.center

                                    name = self.Base_Name + "_" + object.name + "_FACES_" + str(face_counter)

                                    if orientation == "GLOBAL":
                                        rotation_quaternion = (0, 0, 0, 0)
                                        rotation_euler = (0, 0, 0)

                                    if orientation == "CURSOR":
                                        rotation_euler = context.scene.cursor.rotation_euler

                                    if orientation == "LOCAL":
                                        rotation_euler = object.matrix_world.to_euler()

                                    if orientation == "NORMAL":
                                        normal = face.normal

                                        if flip_direction:
                                            normal = -normal


                                        rotation_euler = Utility_Functions.Normal_To_Orientation(object, face.center, normal).to_euler()

                                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                                    camera_object.location = position
                                    camera_object.rotation_euler = rotation_euler

                                    # camera_object.matrix_world = Utility_Functions.Face_To_Orientation(object, face)



                                    rotationMAT = mathutils.Euler(rotation_euler).to_matrix()
                                    rotationMAT.invert()
                                    zVector = mathutils.Vector((0, 0, -self.normal_offset)) @ rotationMAT
                                    camera_object.location = camera_object.location + zVector



                                    camera_object.rotation_euler.rotate_axis("X", self.rotation[0])
                                    camera_object.rotation_euler.rotate_axis("Y", self.rotation[1])
                                    camera_object.rotation_euler.rotate_axis("Z", self.rotation[2])


                                    if self.Parent:

                                        constraint = camera_object.constraints.new("CHILD_OF")
                                        constraint.target = object

                if mode == "EDIT_CURVE":

                    Utility_Functions.object_switch_mode(object, "OBJECT")

                    if object.type == "CURVE":

                        spline_counter = -1

                        for spline_count, spline in enumerate(object.data.splines):

                            increment_spline_count = True
                            point_counter = -1

                            for count, bezier_point in enumerate(spline.bezier_points):

                                if bezier_point.select_control_point:

                                    if increment_spline_count:
                                        spline_counter += 1
                                        increment_spline_count = False

                                    point_counter += 1

                                    name = self.Base_Name + "_" + object.name + "_SPLINE_" + str(spline_counter)+ "_BEZIER_POINT_" + str(point_counter)

                                    position = object.matrix_world @ bezier_point.co.xyz

                                    if orientation == "GLOBAL":
                                        rotation_quaternion = (0, 0, 0, 0)
                                        rotation_euler = (0, 0, 0)

                                    if orientation == "CURSOR":
                                        rotation_euler = context.scene.cursor.rotation_euler

                                    if orientation == "LOCAL":
                                        rotation_euler = object.matrix_world.to_euler()


                                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                                    camera_object.location = position
                                    camera_object.rotation_euler = rotation_euler

                                    if self.Parent:

                                        constraint = camera_object.constraints.new("CHILD_OF")
                                        constraint.target = object

                            for count, point in enumerate(spline.points):

                                if point.select:

                                    if increment_spline_count:
                                        spline_counter += 1
                                        increment_spline_count = False

                                    point_counter += 1

                                    name = self.Base_Name + "_" + object.name + "_SPLINE_" + str(spline_counter)+ "_NURBS_POINT_" + str(point_counter)

                                    position = object.matrix_world @ point.co.xyz

                                    if orientation == "GLOBAL":
                                        rotation_quaternion = (0, 0, 0, 0)
                                        rotation_euler = (0, 0, 0)

                                    if orientation == "CURSOR":
                                        rotation_euler = context.scene.cursor.rotation_euler

                                    if orientation == "LOCAL":
                                        rotation_euler = object.matrix_world.to_euler()


                                    collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                                    camera_object = Utility_Functions.Create_Camera(name, collection=collection)

                                    camera_object.location = position
                                    camera_object.rotation_euler = rotation_euler

                                    if self.Parent:

                                        constraint = camera_object.constraints.new("CHILD_OF")
                                        constraint.target = object




                if mode in ["EDIT_ARMATURE", "POSE"]:


                    if object.type == "ARMATURE":



                        if mode == "EDIT_ARMATURE":
                            bones = object.data.edit_bones

                        if mode == "POSE":
                            bones = object.pose.bones

                        for count, bone in enumerate(bones):

                            if Utility_Functions.check_bone_select(bone, mode):

                                name = self.Base_Name + "_" + object.name + "_BONE_" + bone.name
                                center = mathutils.Vector([0, 0, 0])

                                if self.ELEM_Armature == "CENTER":

                                    center = Utility_Functions.midpoint([bone.head, bone.tail], "CENTER")

                                if self.ELEM_Armature == "HEAD":

                                    center = bone.head

                                if self.ELEM_Armature == "TAIL":

                                    center = bone.tail

                                position = object.matrix_world @ center

                                if orientation == "GLOBAL":
                                    rotation_euler = (0, 0, 0)

                                if orientation == "CURSOR":
                                    rotation_euler = context.scene.cursor.rotation_euler

                                if orientation == "LOCAL":
                                    rotation_euler = object.matrix_world.to_euler()

                                if orientation == "BONE":
                                    bone_matrix = object.matrix_world @ bone.matrix @ mathutils.Matrix.Rotation(math.radians(90.0), 4, 'X')
                                    rotation_euler = bone_matrix.to_euler()

                                collection = Utility_Functions.Find_Or_Create_Collection(self.Use_Collection, self.Collection_Name)

                                camera_object = Utility_Functions.Create_Camera(name, collection=collection)
                                camera_object.location = position
                                camera_object.rotation_euler = rotation_euler


                                if self.Parent:

                                    parent_constraint_pair = {"camera": camera_object, "bone": bone.name, "object": object}
                                    parent_constraint_pairs.append(parent_constraint_pair)






        if mode in ["EDIT_ARMATURE", "POSE"]:
            if self.Parent:

                bpy.ops.object.mode_set(mode='POSE', toggle=False)

                for parent_constraint_pair in parent_constraint_pairs:

                    camera_object = parent_constraint_pair["camera"]
                    bone = parent_constraint_pair["bone"]
                    object = parent_constraint_pair["object"]

                    if camera_object and object:

                        pose_position = object.data.pose_position

                        if mode == "EDIT_ARMATURE":
                            object.data.pose_position = "REST"

                        constraint = camera_object.constraints.new("CHILD_OF")
                        constraint.target = object
                        constraint.subtarget = bone

                        context.view_layer.update()
                        object.data.pose_position = pose_position


        if mode in ["EDIT_MESH", "EDIT_CURVE", "EDIT_ARMATURE"]:

            for object in selected_objects:
                if object.type in ["MESH", "CURVE", "ARMATURE"]:
                    Utility_Functions.object_switch_mode(object, "EDIT")

        if mode in ["POSE"]:

            for object in selected_objects:
                if object.type in ["ARMATURE"]:
                    Utility_Functions.object_switch_mode(object, "POSE")

        context.view_layer.objects.active = active_object

        return {'FINISHED'}




classes = [VIEWFINDER_OT_Create_Camera_From_Selected]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
