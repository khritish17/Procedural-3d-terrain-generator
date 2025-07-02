import bpy 
import os 

from . import util
from . import ui_properties
from . import ui
from . import operators
"""
    Entry point of the addon,
"""
# Addon Information
bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Khritish Kumar Behera",
    "version": (1, 0),
    "blender": (3, 0, 0), # Minimum Blender version
    "location": "3D View > Sidebar > Terrain Generator Properties",
    "description": "To generate infinite terrain seamlessly using Perlin noise.",
    "warning": "",
    "doc_url": "https://github.com/khritish17/Procedural-3d-terrain-generator/blob/master/README.md",
    "category": "Mesh",
}
classes = [
    ui_properties.PTG_Properties,
    ui.PTG_UI,
    operators.PTG_Generate_Operator
]

def register():
    # entry point of the addon
    # to run the noise libraray the global python exe is required
    # check_and_configure() in util.py gets the path to the global python exe
    # and add it to a file 'python_exe_path.txt' 
    addon_dir = os.path.dirname(bpy.path.abspath(__file__))
    util.check_and_configure(addon_dir)
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # a pointer to access the custom properties defined in ui_properties.py
    bpy.types.Scene.ptg_props = bpy.props.PointerProperty(type=ui_properties.PTG_Properties)

def unregister():
    
    if ui_properties._update_timer_handle is not None:
        try:
            bpy.app.timers.unregister(ui_properties._update_timer_handle)
            ui_properties._update_timer_handle = None
            print("-> PTG log: Unregistered terrain update timer")
        except ValueError:
            pass
    if hasattr(bpy.types.Scene, 'ptg_props'):
        del bpy.types.Scene.ptg_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
