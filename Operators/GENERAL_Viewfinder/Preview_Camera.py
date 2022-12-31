
import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_texture_2d


from Viewfinder import Utility_Functions



def redraw_viewport(context):
    for area in context.window.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()







def get_camera(context):

    preferences = Utility_Functions.get_addon_preferences()

    camera = None
    scn = context.scene


    if preferences.PREVIEWER_Target == "BOTH":

        if context.scene.camera:
            if context.scene.camera.type == "CAMERA":
                camera = context.scene.camera

        if context.object:
            if context.object.type == "CAMERA":
                if context.object.select_get():
                    camera = context.object

    if preferences.PREVIEWER_Target == "ACTIVE":
        if context.object:
            if context.object.type == "CAMERA":
                
                if context.object.select_get():
                    camera = context.object
    
    if preferences.PREVIEWER_Target == "SCENE":
        if context.scene.camera:
            if context.scene.camera.type == "CAMERA":
                camera = context.scene.camera
    


    return camera


def draw_camera_name(camera, x, y, width, margin, font_size, color):

    font_id = 0  # XXX, need to find out how best to get this.


    if camera:

        text = camera.name

        blf.enable(font_id, blf.SHADOW)
        blf.color(font_id, color[0], color[1], color[2], color[3])


        blf.size(font_id, font_size, 72)
        dimensions = blf.dimensions(font_id, text)

        blf.position(font_id, x, y-(dimensions[1]*margin), 0)

        blf.draw(font_id, text)

        blf.disable(font_id, blf.SHADOW)


def draw_camera_target(context, camera, x, y, width, height, margin, font_size, target, color):

    if camera:
        if target == "SCENE":
            text = "Scene Camera"

        if target == "ACTIVE":
            text = "Active Camera"

        if target == "BOTH":
            if camera == context.scene.camera:
                text = "Scene Camera"
            if context.active_object == camera:
                if camera.select_get():
                    text = "Active Camera"

        font_id = 0  # XXX, need to find out how best to get this.



        blf.enable(font_id, blf.SHADOW)

        blf.color(font_id, color[0], color[1], color[2], color[3])

        blf.size(font_id, font_size, 72)
        dimensions = blf.dimensions(font_id, text)

        blf.position(font_id, x, y+((dimensions[1]*margin)+height-dimensions[1]), 0)

        blf.draw(font_id, text)

        blf.disable(font_id, blf.SHADOW)







def draw_camera(context, camera, offset_x , offset_y ,width, height, border_thickness, color, offscreen, hide_overlay):

    scene = context.scene

    if camera is not None:

        if camera.type == "CAMERA":
            


            current_overlay_state = context.space_data.overlay.show_overlays
            # current_shading_state = context.space_data.shading.type

            if hide_overlay:
                context.space_data.overlay.show_overlays = False
                # context.space_data.shading.type = "SOLID"

            view_matrix = camera.matrix_world.inverted()
            projection_matrix = camera.calc_matrix_camera(
            context.evaluated_depsgraph_get(), x=width, y=height)




            offscreen.draw_view3d(
                scene,
                context.view_layer,
                context.space_data,
                context.region,
                view_matrix,
                projection_matrix,
                do_color_management=False)

            gpu.state.depth_mask_set(False)

            context.space_data.overlay.show_overlays = current_overlay_state
            # context.space_data.shading.type = current_shading_state

            draw_texture_2d(offscreen.texture_color, (offset_x, offset_y), width, height)



            draw_outline(offset_x, offset_y, width, height, border_thickness, color)





def draw_outline(x, y, width, height, thickness, color):

    vertices = [(x, y), (x+width, y), (x+width, y+height), (x, y+height), (x, y)]

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    gpu.state.blend_set('ALPHA')
    gpu.state.line_width_set(thickness)
    batch = batch_for_shader(shader, 'LINE_STRIP', {"pos": vertices})

    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

    gpu.state.line_width_set(1.0)
    gpu.state.blend_set('NONE')


handler = None
active_operator = None


def draw_camera_preview(self):



    context = bpy.context

    scn = context.scene
    preferences = Utility_Functions.get_addon_preferences()
    camera = None


    self.Percentage = preferences.PREVIEWER_Render_Percentage / 100

    if preferences.PREVIEWER_Offset_Mode == "RELATIVE":
        self.Offset_X = preferences.PREVIEWER_Offset_X_Rel * context.region.width
        self.Offset_Y = preferences.PREVIEWER_Offset_Y_Rel * context.region.height

    if preferences.PREVIEWER_Offset_Mode == "ABSOLUTE":
        self.Offset_X = preferences.PREVIEWER_Offset_X_Abs
        self.Offset_Y = preferences.PREVIEWER_Offset_Y_Abs

    self.Width = int(context.scene.render.resolution_x * self.Percentage)
    self.Height = int(context.scene.render.resolution_y * self.Percentage)


    


    if self.Height or self.Width:
        aspect_ratio = self.Height / self.Width
    else:
        aspect_ratio = 0

    if preferences.PREVIEWER_Width_Mode == "RELATIVE":
        self.Display_Width = int(context.region.width * preferences.PREVIEWER_Width_Rel)

    if preferences.PREVIEWER_Width_Mode == "ABSOLUTE":

        self.Display_Width = int(preferences.PREVIEWER_Width_Abs)



    self.Display_Height = int(self.Display_Width * aspect_ratio)



    if self.offscreen:
        if self.offscreen.width == self.Width and self.offscreen.height == self.Height:
            pass
        else:
            self.offscreen.free()
            self.offscreen = gpu.types.GPUOffScreen(self.Width, self.Height)
    else:
        self.offscreen = gpu.types.GPUOffScreen(self.Width, self.Height)



    camera = get_camera(context)




    offscreen = self.offscreen


    color = preferences.PREVIEWER_Border_Color_Normal
    thickness = preferences.PREVIEWER_Border_Thickness

    if self.mouse_region_x > self.Offset_X and self.mouse_region_x < self.Offset_X + self.Display_Width:
        if self.mouse_region_y > self.Offset_Y and self.mouse_region_y < self.Offset_Y + self.Display_Height:

            if self.ctrl:
                color = preferences.PREVIEWER_Border_Color_Hover



            if self.lmb_down:

                if self.ctrl:
                    self.set_and_view_camera(context, camera, self.active_area)


    # if self.MouseInside:

    #     if preferences.PREVIEWER_Border_Use_Hover:
    #         color = preferences.PREVIEWER_Border_Color_Hover
    #         thickness = preferences.PREVIEWER_Border_Thickness_Hover

    self.camera = context.object

    show_preview = True

    if preferences.PREVIEWER_Hide_In_Camera_View:


        if context.area:
        # if self.active_area:
            if context.area.type == "VIEW_3D":
                if context.area.spaces[0].region_3d.view_perspective == "CAMERA":
                    show_preview = False
            # if self.active_area.spaces[0].region_3d.view_perspective == "CAMERA":

        if preferences.PREVIEWER_Obey_Hide_Overlay:
            if not context.space_data.overlay.show_overlays:
                show_preview = False


    if show_preview:
        hide_overlay = preferences.PREVIEWER_Hide_Overlay_In_Preview

        draw_camera(context, camera,self.Offset_X, self.Offset_Y, self.Display_Width, self.Display_Height, thickness, color, offscreen, hide_overlay)

        if preferences.PREVIEWER_Display_Camera_Name:
            margin = preferences.PREVIEWER_Font_Offset
            font_size = preferences.PREVIEWER_Font_Size
            font_color = preferences.PREVIEWER_Font_Color
            draw_camera_name(camera, self.Offset_X, self.Offset_Y, self.Display_Width, margin, font_size, font_color)

            target = preferences.PREVIEWER_Target
            draw_camera_target(context, camera, self.Offset_X, self.Offset_Y, self.Display_Width, self.Display_Height, margin, font_size, target, font_color)
    







class VIEWFINDER_Preview_Camera(bpy.types.Operator):
    """Preview Camera"""
    bl_idname = "viewfinder.preview_camera"
    bl_label = "Preview Camera"
    bl_options = {'UNDO', 'REGISTER'}


    shift = False
    ctrl = False

    offscreen = None
    _mouseX = 0
    _mouseY = 0

    mouse_region_x = 0
    mouse_region_y = 0

    lmb_down = False
    rmb_down = False

    active_area = None



    Offset_X = 0
    Offset_Y = 0
    Width = 0
    Height = 0


    def getActiveViewportRegion(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                if (area.x <= self._mouseX < (area.x+area.width) and
                    area.y <= self._mouseY < (area.y+area.height)):
                    return area
        return None

    def handle_event(self, context, event):






        self.rmb_down = False
        self.lmb_down = False

        if event.shift:
            self.shift = True
        else:
            self.shift = False

        if event.ctrl:
            self.ctrl= True
        else:
            self.ctrl= False

        if event.type == "LEFTMOUSE":
            if event.value == "PRESS":
                self.lmb_down = True

        if event.type == "RIGHTMOUSE":
            if event.value == "PRESS":
                self.rmb_down = True



    def set_and_view_camera(self, context, camera, area):

        if context.scene.camera != camera:
            context.scene.camera = camera
        area.spaces[0].region_3d.view_perspective = "CAMERA"




        # if not camera.select_get():
        #     camera.select_set(True)
        # if not context.view_layer.objects.active == camera:
        #     context.view_layer.objects.active = camera

    def modal(self, context, event):

        global handler


        self.handle_event(context, event)

        self._mouseX = event.mouse_x 
        self._mouseY = event.mouse_y
        self.active_area = self.getActiveViewportRegion()

        if self.active_area:

            self.active_area.tag_redraw()

            self.mouse_region_x = event.mouse_x - self.active_area.x
            self.mouse_region_y = event.mouse_y - self.active_area.y

                
        return {'PASS_THROUGH'}



    def execute(self, context):

        global handler

        if handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
            handler = None

    def cancel(self, context):

        global handler

        if handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
            handler = None

    def invoke(self, context, event):


        global handler

        if handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
            handler = None
        else:
            global active_operator
            args = (self,)
            handler = bpy.types.SpaceView3D.draw_handler_add(draw_camera_preview, args, 'WINDOW', 'POST_PIXEL')
            active_operator = self
            

            context.window_manager.modal_handler_add(self)

            redraw_viewport(context)


            return {'RUNNING_MODAL'}

        Utility_Functions.update_UI()
        return {'FINISHED'}




class VIEWFINDER_PT_Preview_Camera_Popover(bpy.types.Panel):
    bl_label = "Preview Camera Menu"
    bl_idname = "VIEWFINDER_PT_preview_camera_popover"

    bl_space_type = 'VIEW_3D'
    bl_region_type = "HEADER"
    is_popover = True


    def draw(self, context):
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
















def draw_camera_preview_button(self, context):

    layout = self.layout
    row = layout.row(align=True)
    
    if handler:
        row.operator("viewfinder.preview_camera", text="", icon="VIEW_CAMERA", depress=True)
    else:
        row.operator("viewfinder.preview_camera", text="", icon="VIEW_CAMERA", depress=False)

    row.popover("VIEWFINDER_PT_preview_camera_popover", text="")



classes = [VIEWFINDER_PT_Preview_Camera_Popover, VIEWFINDER_Preview_Camera]

def register():


    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_HT_header.append(draw_camera_preview_button)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_header.remove(draw_camera_preview_button)


    global handler
    if handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        handler = None

if __name__ == "__main__":
    register()




















