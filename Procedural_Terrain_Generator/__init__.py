import bpy 
import os 
from . import util

# Addon Information
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
classes = []

def register():
    # entry point of the addon
    # check and configure 
    adon_dir = os.path.dirname(bpy.path.abspath(__file__))
    util.check_and_configure(adon_dir)
    pass

def unregister():
    pass
