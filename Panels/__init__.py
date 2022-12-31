import bpy



from . import PANEL_Viewfinder_Operators
from . import PANEL_Camera_List

modules = [PANEL_Camera_List, PANEL_Viewfinder_Operators]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
