
import bpy

from . import Duplicate_Camera
from . import Find_Camera
from . import Select_Camera
from . import Add_Camera_Marker
from . import View_Camera
from . import Remove_Camera

from . import Add_Camera_To_List
from . import Resolution_Match_Scene

modules = [Resolution_Match_Scene, Add_Camera_To_List, Remove_Camera, Duplicate_Camera, Find_Camera, Select_Camera, Add_Camera_Marker, View_Camera]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
