
import bpy
from . import Create_Camera_From_View
from . import Create_Constrainted_Camera_From_Selected_Curves
from . import Add_Aligned_Camera
from . import Add_Camera_And_Empty_Target
from . import Create_Camera_Target_Empties

from . import Add_Camera_Booth
from . import Create_Markers_From_Selected_Camera

from . import Preview_Camera
from . import Selected_Camera_To_View
from . import Frame_Active_Camera_To_Selected_Objects
from . import Constraint_Camera_To_Curve
from . import Create_And_Constraint_Curve_From_Selected_Camera
from . import Create_Curve_Fly_Through_Cam
from . import Create_Curve_Cam_With_Aim
from . import Track_Constriant_Selected_Camera_To_Active

modules = [Track_Constriant_Selected_Camera_To_Active, Create_Curve_Cam_With_Aim, Create_Curve_Fly_Through_Cam, Create_And_Constraint_Curve_From_Selected_Camera, Constraint_Camera_To_Curve, Frame_Active_Camera_To_Selected_Objects, Selected_Camera_To_View, Preview_Camera, Create_Markers_From_Selected_Camera, Add_Camera_Booth, Create_Camera_Target_Empties, Add_Camera_And_Empty_Target, Add_Aligned_Camera, Create_Camera_From_View, Create_Constrainted_Camera_From_Selected_Curves]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
