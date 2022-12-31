bl_info = {
    "name": "Viewfinder",
    "author": "BlenderBoi",
    "version": (1, 4, 1),
    "blender": (3, 1, 0),
    "description": "",
    "wiki_url": "",
    "category": "Camera",
}

import bpy
from . import Preferences
from . import Data
from . import Panels
from . import Operators
from . import Menus

modules = [Data, Panels, Operators, Menus, Preferences]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
















if __name__ == "__main__":
    register()
