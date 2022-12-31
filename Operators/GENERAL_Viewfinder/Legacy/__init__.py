
import bpy



from . import Create_Camera_From_View
from . import Create_Camera_From_Selected
from . import Create_Camera_And_Target
from . import Create_Camera_Target_Empties
from . import Create_Camera_Plane

modules = [Create_Camera_Plane, Create_Camera_Target_Empties, Create_Camera_And_Target, Create_Camera_From_View, Create_Camera_From_Selected]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
