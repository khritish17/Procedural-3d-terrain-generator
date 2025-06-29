import bpy
import os
import sys
import subprocess

# Import your other addon modules
from . import ui_panel
from . import properties
from . import operators
from . import utils

# Addon information
bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Khritish Kumar Behera",
    "version": (1, 0),
    "blender": (3, 0, 0), # Minimum Blender version
    "location": "3D View > Sidebar > Terrain Generator Properties",
    "description": "To generate infinite terrain seamlessly using Perlin noise.",
    "warning": "",
    "doc_url": "",
    "category": "Mesh",
}

classes = [
    properties.PTG_Properties, # PropertyGroup should generally be first if others depend on it
    ui_panel.PTG_PT_TerrainGeneratorPanel,
    operators.PTG_OT_GenerateTerrain,
    operators.PTG_OT_RegenerateTerrain,
]

# --- Main Registration Function ---
def register():
    # Get the addon's root directory reliably
    addon_dir = os.path.dirname(bpy.path.abspath(__file__))
    print(f"DEBUG: Addon root directory detected: {addon_dir}")

    # Ensure the global Python path is found and written to a file
    # This will create 'global_python_path.txt' in the addon's root directory
    utils.find_and_write_global_python_path(addon_dir)

    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ptg_props = bpy.props.PointerProperty(type=properties.PTG_Properties)

    print(f"Addon '{bl_info['name']}' REGISTERED.")

# --- Main Unregistration Function ---
def unregister():
    # Unregister custom properties first
    if hasattr(bpy.types.Scene, 'ptg_props'):
        del bpy.types.Scene.ptg_props

    # Unregister all classes in reverse order of registration (good practice)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    print(f"Addon '{bl_info['name']}' UNREGISTERED.")

# This block allows the script to be run directly from Blender's Text Editor for testing
# without formally installing it as an addon.
# if __name__ == "__main__":
#     register()
    # To unregister for testing:
    # unregister()
