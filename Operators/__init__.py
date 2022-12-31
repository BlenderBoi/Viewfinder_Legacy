import bpy


from . import GENERAL_Viewfinder
from . import PANEL_Camera_List

modules = [PANEL_Camera_List, GENERAL_Viewfinder]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
