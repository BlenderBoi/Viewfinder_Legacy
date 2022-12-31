
import bpy



from . import MT_Viewfinder_Menu
from . import MT_Viewfinder_Camera_Add_Menu

modules = [MT_Viewfinder_Camera_Add_Menu, MT_Viewfinder_Menu]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
