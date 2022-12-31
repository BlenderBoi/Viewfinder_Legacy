import bpy


from . import Scene_Properties
from . import Object_Properties

modules = [Scene_Properties, Object_Properties]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
