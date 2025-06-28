import bpy

# Addon information (essential for proper addon setup)
bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Khritish Kumar Behera",
    "version": (1, 0),
    "blender": (3, 0, 0), # Minimum Blender version
    "location": "3D View > Sidebar > My Tools Tab",
    "description": "A simple custom panel in the 3D Viewport.",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

class Procedural_Terrain_Generator(bpy.types.Panel):
    bl_label = "Terrain Generator Properties" # The name displayed at the top of the panel
    bl_idname = "PTG_properties" # Unique identifier for the panel
    bl_space_type = 'VIEW_3D' # Where the panel will appear (e.g., 'VIEW_3D', 'PROPERTIES', 'NODE_EDITOR')
    bl_region_type = 'UI' # Which region within that space (e.g., 'UI' for N-panel, 'TOOLS' for T-panel)
    bl_category = "PTG Tools" # The tab name in the N-panel

    # The 'draw' method is where you define the layout of your UI elements.
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        # dimension
        layout.label(text = "|-- Terrain Dimension / Offsets:")
        layout.label(text = "|---- Dimension:")
        # terrain length 
        layout.prop(scene, "tarrain_length_prop")
        # terrain width 
        layout.prop(scene, "tarrain_width_prop")
        layout.label(text = "|---- Offsets:") 
        layout.prop(scene, "offset_x_prop")
        layout.prop(scene, "offset_y_prop")
        
        # terrain properties
        layout.label(text = "|-- Terrain Properties:")
        
        layout.prop(scene, "terrain_seed_prop")
        layout.prop(scene, "terrain_scale_prop")
        layout.prop(scene, "terrain_octaves_prop")
        layout.prop(scene, "terrain_persistence_prop")
        layout.prop(scene, "terrain_lacunarity_prop")
        
        # Height Properties
        layout.label(text = "|-- Terrain Height Properties:")
        layout.prop(scene, "height_seed_prop")
        layout.prop(scene, "height_scale_prop")
        layout.prop(scene, "height_octaves_prop")
        layout.prop(scene, "height_persistence_prop")
        layout.prop(scene, "height_lacunarity_prop")
        layout.prop(scene, "min_height_prop")
        layout.prop(scene, "max_height_prop")
        
        # toggle
#        layout.prop(scene, "toogle_button", text = "Toggle")

# 2. Define custom properties (if needed)
# Properties need to be registered with Blender's data types (like Scene, Object, etc.)
def register_properties():
    
    bpy.types.Scene.tarrain_length_prop = bpy.props.IntProperty(
        name = "Terrain Length",
        description = "Dimension: Length of the terrain",
        default = 100,
        min = 0,
        max = 1000
    )
    bpy.types.Scene.tarrain_width_prop = bpy.props.IntProperty(
        name = "Terrain Width",
        description = "Dimension: Width of the terrain",
        default = 100,
        min = 0,
        max = 1000
    )
    bpy.types.Scene.offset_x_prop = bpy.props.FloatProperty(
        name = "Offest X",
        description = "Shift the noise pattern horizontally (along X axis),allowing you to generate different sections of the 'infinite' noise landscape.",
        default = 0.0,
        min = -1000.0,
        max = 1000.0
    )
    bpy.types.Scene.offset_y_prop = bpy.props.FloatProperty(
        name = "Offest Y",
        description = "Shift the noise pattern vertically (along Y axis),allowing you to generate different sections of the 'infinite' noise landscape.",
        default = 0.0,
        min = -1000.0,
        max = 1000.0
    )
    bpy.types.Scene.terrain_seed_prop = bpy.props.IntProperty(
        name = "Terrain Seed",
        description = "An integer seed value to generate a specific, reproducible noise pattern",
        default = 0,
        min = -10000,
        max = 10000
    )
    bpy.types.Scene.terrain_scale_prop = bpy.props.FloatProperty(
        name = "Terrain Scale",
        description = "Zoom level of the noise features.\n\n --- Larger scale values (e.g., 100.0): Zoom out on the noise, making features larger and smoother.\n\n --- Smaller scale values (e.g., 10.0) : Zoom in on the noise, making features smaller and more jagged/detailed.",
        default = 100.0,
        min = 1.0,
        max = 1000.0
    )
    bpy.types.Scene.terrain_octaves_prop = bpy.props.IntProperty(
        name = "Terrain Octaves",
        description = "The number of layers of noise (fractal sum) used to generate the final value.More octaves add more detail.\n --- Higher values add more computational cost and finer details",
        default = 6,
        min = 1,
        max = 10
    )
    bpy.types.Scene.terrain_persistence_prop = bpy.props.FloatProperty(
        name = "Terrain Persistence",
        description = "How much each successive octave contributes to the overall amplitude (controls detail roughness).\n --- 0.0: Each successive octave has no amplitude, resulting in very flat noise (only the first octave contributes).\n --- 0.5: A common value, meaning each subsequent octave has half the amplitude of the previous one. This creates a good balance of large features and fine detail (fractal Brownian motion, or fBm).\n ---Values closer to 1.0 make higher octaves contribute more, leading to a 'rougher,' more chaotic, or spiky appearance.",
        default = 0.5,
        min = 0.0,
        max = 1.0
    )
    bpy.types.Scene.terrain_lacunarity_prop = bpy.props.FloatProperty(
        name = "Terrain Lacunarity",
        description = "Determines how zoomed in or out the noise appears.Smaller values create smoother, larger features. \n --- 2.0: A common and traditional value, meaning each successive octave has double the frequency (details are twice as small). This creates a good fractal-like appearance. \n --- Values greater than 1.0 increase the frequency, making details smaller and more frequent. \n --- Values closer to 1.0 (but greater than 1) will make the details less distinct between octaves.",
        default = 2.0,
        min = 1.0,
        max = 3.5
    )
    bpy.types.Scene.height_seed_prop = bpy.props.IntProperty(
        name = "Height Seed",
        description = "An integer seed value to generate a specific, reproducible noise pattern",
        default = 0,
        min = -10000,
        max = 10000
    )
    bpy.types.Scene.height_scale_prop = bpy.props.FloatProperty(
        name = "Height Scale",
        description = "Zoom level of the noise features.\n\n --- Larger scale values (e.g., 100.0): Zoom out on the noise, making features larger and smoother.\n\n --- Smaller scale values (e.g., 10.0) : Zoom in on the noise, making features smaller and more jagged/detailed.",
        default = 100.0,
        min = 1.0,
        max = 1000.0
    )
    bpy.types.Scene.height_octaves_prop = bpy.props.IntProperty(
        name = "Height Octaves",
        description = "The number of layers of noise (fractal sum) used to generate the final value.More octaves add more detail.\n --- Higher values add more computational cost and finer details",
        default = 6,
        min = 1,
        max = 10
    )
    bpy.types.Scene.height_persistence_prop = bpy.props.FloatProperty(
        name = "Height Persistence",
        description = "How much each successive octave contributes to the overall amplitude (controls detail roughness).\n --- 0.0: Each successive octave has no amplitude, resulting in very flat noise (only the first octave contributes).\n --- 0.5: A common value, meaning each subsequent octave has half the amplitude of the previous one. This creates a good balance of large features and fine detail (fractal Brownian motion, or fBm).\n ---Values closer to 1.0 make higher octaves contribute more, leading to a 'rougher,' more chaotic, or spiky appearance.",
        default = 0.5,
        min = 0.0,
        max = 1.0
    )
    bpy.types.Scene.height_lacunarity_prop = bpy.props.FloatProperty(
        name = "Height Lacunarity",
        description = "Determines how zoomed in or out the noise appears.Smaller values create smoother, larger features. \n --- 2.0: A common and traditional value, meaning each successive octave has double the frequency (details are twice as small). This creates a good fractal-like appearance. \n --- Values greater than 1.0 increase the frequency, making details smaller and more frequent. \n --- Values closer to 1.0 (but greater than 1) will make the details less distinct between octaves.",
        default = 2.0,
        min = 1.0,
        max = 3.5
    )
    bpy.types.Scene.min_height_prop = bpy.props.FloatProperty(
        name = "Min Height",
        description = "Minimum height of the terrain mesh generated.",
        default = 10.0,
        min = 0.0,
        max = 1000.0
    )
    bpy.types.Scene.max_height_prop = bpy.props.FloatProperty(
        name = "Max Height",
        description = "Maximum height of the terrain mesh generated.",
        default = 100.0,
        min = 0.0,
        max = 1000.0
    )
    
    bpy.types.Scene.toogle_button = bpy.props.BoolProperty(
    name = "Tick me")

def unregister_properties():
    if hasattr(bpy.types.Scene.terrain_scale_prop):
        del bpy.types.Scene.terrain_scale_prop
    if hasattr(bpy.types.Scene.tarrain_length_prop):
        del bpy.types.Scene.tarrain_length_prop
    if hasattr(bpy.types.Scene.tarrain_width_prop):
        del bpy.types.Scene.tarrain_width_prop
    if hasattr(bpy.types.Scene.offset_x_prop):
        del bpy.types.Scene.offset_x_prop
    if hasattr(bpy.types.Scene.offset_y_prop):
        del bpy.types.Scene.offset_y_prop
        
    if hasattr(bpy.types.Scene.terrain_seed_prop):
        del bpy.types.Scene.terrain_seed_prop
        
    if hasattr(bpy.types.Scene.terrain_scale_prop):
        del bpy.types.Scene.terrain_scale_prop
        
    if hasattr(bpy.types.Scene.terrain_octaves_prop):
        del bpy.types.Scene.terrain_octaves_prop
        
    if hasattr(bpy.types.Scene.terrain_persistence_prop):
        del bpy.types.Scene.terrain_persistence_prop
        
    if hasattr(bpy.types.Scene.terrain_lacunarity_prop):
        del bpy.types.Scene.terrain_lacunarity_prop
        
    if hasattr(bpy.types.Scene.height_seed_prop):
        del bpy.types.Scene.height_seed_prop
        
    if hasattr(bpy.types.Scene.height_scale_prop):
        del bpy.types.Scene.height_scale_prop
        
    if hasattr(bpy.types.Scene.height_octaves_prop):
        del bpy.types.Scene.height_octaves_prop
        
    if hasattr(bpy.types.Scene.height_persistence_prop):
        del bpy.types.Scene.height_persistence_prop
        
    if hasattr(bpy.types.Scene.height_lacunarity_prop):
        del bpy.types.Scene.height_lacunarity_prop
        
    if hasattr(bpy.types.Scene.min_height_prop):
        del bpy.types.Scene.min_height_prop
        
    if hasattr(bpy.types.Scene.max_height_prop):
        del bpy.types.Scene.max_height_prop
        
    if hasattr(bpy.types.Scene.toogle_button):
        del bpy.types.Scene.toogle_button


# 3. Register and Unregister functions
# These are crucial for Blender to load/unload your addon correctly.
classes = (
    Procedural_Terrain_Generator,
)

def register():
    # Register all classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    register_properties() # Register custom properties

    print("My Custom Panel Registered!")

def unregister():
    # Unregister all classes in reverse order of registration (good practice)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    unregister_properties() # Unregister custom properties

# This makes the script runnable directly from Blender's Text Editor for testing
if __name__ == "__main__":
    register()
    # To unregister for testing:
    # unregister()

