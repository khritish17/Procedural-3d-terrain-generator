import bpy 

_update_timer_handle = None

def update_terrain_mesh_debounced(self, context):
    global _update_timer_handle

    if _update_timer_handle is not None:
        try:
            bpy.app.timers.unregister(_update_timer_handle)
            _update_timer_handle = None
        except ValueError:
            _update_timer_handle = None
    if "PTG_Terrain_object" in bpy.data.objects and bpy.data.objects["PTG_Terrain_object"].type == 'MESH':

        def update_terrain_mesh():
            # invoke the terrain generation functions
            print("UPdate trigred in ui_properties")
            bpy.ops.ptg.generate_terrain('INVOKE_DEFAULT')
            global _update_timer_handle
            _update_timer_handle = None
            return None
        _update_timer_handle = bpy.app.timers.register(update_terrain_mesh, first_interval=0.05)

class PTG_Properties(bpy.types.PropertyGroup):
    """
        Custom property group for the ui panel
    """
    terrain_length: bpy.props.IntProperty(
        name = "Terrain Length",
        description = "Dimension: Length of the terrain (number of vertices along X)\n\nDefault value = 100",
        default = 100,
        min = 2, # Minimum 2 to form a plane
        max = 1000
    )
    terrain_width: bpy.props.IntProperty(
        name = "Terrain Width",
        description = "Dimension: Width of the terrain (number of vertices along Y)\n\nDefault value = 100",
        default = 100,
        min = 2, # Minimum 2 to form a plane
        max = 1000
    )
    offset_x: bpy.props.FloatProperty(
        name = "Offset X",
        description = "Shift the noise pattern horizontally (along X axis), allowing you to generate different sections of the 'infinite' noise landscape.\n\nDefault value = 0.0",
        default = 0.0,
        min = -10000.0,
        max = 10000.0,
        step = 100, # Adjust step for finer control
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    offset_y: bpy.props.FloatProperty(
        name = "Offset Y",
        description = "Shift the noise pattern vertically (along Y axis), allowing you to generate different sections of the 'infinite' noise landscape.\n\nDefault value = 0.0",
        default = 0.0,
        min = -10000.0,
        max = 10000.0,
        step = 100,
        precision = 2,
        update = update_terrain_mesh_debounced
    )

    # Perlin noise parameters for terrain (base)
    terrain_seed: bpy.props.IntProperty(
        name = "Terrain Seed",
        description = "An integer seed value to generate a specific, reproducible noise pattern for the base terrain.\n\nDefault value = 0",
        default = 0,
        min = -100000,
        max = 100000,
        update = update_terrain_mesh_debounced
    )
    terrain_scale: bpy.props.FloatProperty(
        name = "Terrain Scale",
        description = (
            "Zoom level of the noise features.\n\n"
            "--- Larger scale values (e.g., 100.0): Zoom out on the noise, making features larger and smoother.\n\n"
            "--- Smaller scale values (e.g., 10.0): Zoom in on the noise, making features smaller and more jagged/detailed.\n\nDefault value = 100.0"
        ),
        default = 100.0,
        min = 1.0,
        max = 1000.0,
        step = 10,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    terrain_octaves: bpy.props.IntProperty(
        name = "Terrain Octaves",
        description = (
            "The number of layers of noise (fractal sum) used to generate the final value. More octaves add more detail.\n"
            "--- Higher values add more computational cost and finer details.\n\nDefault value = 6"
        ),
        default = 6,
        min = 1,
        max = 10,
        update = update_terrain_mesh_debounced
    )
    terrain_persistence: bpy.props.FloatProperty(
        name = "Terrain Persistence",
        description = (
            "How much each successive octave contributes to the overall amplitude (controls detail roughness).\n"
            "--- 0.0: Each successive octave has no amplitude, resulting in very flat noise (only the first octave contributes).\n"
            "--- 0.5: A common value, meaning each subsequent octave has half the amplitude of the previous one. This creates a good balance of large features and fine detail (fractal Brownian motion, or fBm).\n"
            "--- Values closer to 1.0 make higher octaves contribute more, leading to a 'rougher,' more chaotic, or spiky appearance.\n\nDefault value = 0.5"
        ),
        default = 0.5,
        min = 0.0,
        max = 1.0,
        step = 1,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    terrain_lacunarity: bpy.props.FloatProperty(
        name = "Terrain Lacunarity",
        description = (
            "Determines how zoomed in or out the noise appears. Smaller values create smoother, larger features.\n"
            "--- 2.0: A common and traditional value, meaning each successive octave has double the frequency (details are twice as small). This creates a good fractal-like appearance.\n"
            "--- Values greater than 1.0 increase the frequency, making details smaller and more frequent.\n"
            "--- Values closer to 1.0 (but greater than 1) will make the details less distinct between octaves.\n\nDefault value = 2.0"
        ),
        default = 2.0,
        min = 1.0,
        max = 3.5,
        step = 1,
        precision = 2,
        update = update_terrain_mesh_debounced
    )

    # Perlin noise parameters for height modulation
    height_seed: bpy.props.IntProperty(
        name = "Height Seed",
        description = "An integer seed value to generate a specific, reproducible noise pattern for height modulation.\n\nDefault value = 0",
        default = 0,
        min = -100000,
        max = 100000,
        update = update_terrain_mesh_debounced
    )
    height_scale: bpy.props.FloatProperty(
        name = "Height Scale",
        description = (
            "Zoom level of the noise features for height modulation.\n\n"
            "--- Larger scale values (e.g., 100.0): Zoom out on the noise, making features larger and smoother.\n\n"
            "--- Smaller scale values (e.g., 10.0): Zoom in on the noise, making features smaller and more jagged/detailed.\n\nDefault value = 100.0"
        ),
        default = 100.0,
        min = 1.0,
        max = 1000.0,
        step = 10,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    height_octaves: bpy.props.IntProperty(
        name = "Height Octaves",
        description = (
            "The number of layers of noise (fractal sum) used for height modulation. More octaves add more detail.\n"
            "--- Higher values add more computational cost and finer details.\n\nDefault value = 6"
        ),
        default = 6,
        min = 1,
        max = 10,
        update = update_terrain_mesh_debounced
    )
    height_persistence: bpy.props.FloatProperty(
        name = "Height Persistence",
        description = (
            "How much each successive octave contributes to the overall amplitude for height modulation.\n"
            "--- 0.0: Each successive octave has no amplitude, resulting in very flat noise.\n"
            "--- 0.5: A common value, creates a good balance of large features and fine detail.\n"
            "--- Values closer to 1.0 make higher octaves contribute more, leading to a 'rougher,' more chaotic, or spiky appearance.\n\nDefault value = 0.5"
        ),
        default = 0.5,
        min = 0.0,
        max = 1.0,
        step = 1,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    height_lacunarity: bpy.props.FloatProperty(
        name = "Height Lacunarity",
        description = (
            "Determines how zoomed in or out the noise appears for height modulation.\n"
            "--- 2.0: A common and traditional value, each successive octave has double the frequency.\n"
            "--- Values greater than 1.0 increase the frequency, making details smaller and more frequent.\n"
            "--- Values closer to 1.0 (but greater than 1) will make the details less distinct between octaves.\n\nDefault value = 2.0"
        ),
        default = 2.0,
        min = 1.0,
        max = 3.5,
        step = 1,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    min_height: bpy.props.FloatProperty(
        name = "Min Height",
        description = "Minimum height of the terrain mesh generated.\n\nDefault value = 10.0",
        default = 10.0,
        min = -1000.0, # Allow negative heights for underwater terrain
        max = 1000.0,
        step = 10,
        precision = 2,
        update = update_terrain_mesh_debounced
    )
    max_height: bpy.props.FloatProperty(
        name = "Max Height",
        description = "Maximum height of the terrain mesh generated.\n\nDefault value = 100.0",
        default = 100.0,
        min = -1000.0,
        max = 1000.0,
        step = 10,
        precision = 2,
        update = update_terrain_mesh_debounced
    )