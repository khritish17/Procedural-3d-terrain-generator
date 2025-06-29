import bpy

class PTG_PT_TerrainGeneratorPanel(bpy.types.Panel):
    """
    Blender UI Panel for the Procedural Terrain Generator.
    Displays various properties and buttons for generating terrain.
    """
    bl_label = "Terrain Generator Properties" # The name displayed at the top of the panel
    bl_idname = "PTG_PT_terrain_generator" # Unique identifier for the panel
    bl_space_type = 'VIEW_3D' # Where the panel will appear (e.g., 'VIEW_3D', 'PROPERTIES', 'NODE_EDITOR')
    bl_region_type = 'UI' # Which region within that space (e.g., 'UI' for N-panel, 'TOOLS' for T-panel)
    bl_category = "PTG Tools" # The tab name in the N-panel

    def draw(self, context):
        """
        Draws the UI elements for the panel.
        """
        layout = self.layout
        scene = context.scene
        # Access the custom property group
        ptg_props = scene.ptg_props

        # Terrain Dimension / Offsets
        box = layout.box()
        box.label(text = "Terrain Dimension / Offsets:")
        col = box.column(align=True)
        col.prop(ptg_props, "terrain_length")
        col.prop(ptg_props, "terrain_width")
        col.prop(ptg_props, "offset_x")
        col.prop(ptg_props, "offset_y")

        # Terrain Properties (Base Perlin)
        box = layout.box()
        box.label(text = "Terrain Base Noise Properties:")
        col = box.column(align=True)
        col.prop(ptg_props, "terrain_seed")
        col.prop(ptg_props, "terrain_scale")
        col.prop(ptg_props, "terrain_octaves")
        col.prop(ptg_props, "terrain_persistence")
        col.prop(ptg_props, "terrain_lacunarity")

        # Terrain Height Properties (Height Modulation Perlin)
        box = layout.box()
        box.label(text = "Terrain Height Noise Properties:")
        col = box.column(align=True)
        col.prop(ptg_props, "height_seed")
        col.prop(ptg_props, "height_scale")
        col.prop(ptg_props, "height_octaves")
        col.prop(ptg_props, "height_persistence")
        col.prop(ptg_props, "height_lacunarity")
        col.prop(ptg_props, "min_height")
        col.prop(ptg_props, "max_height")

        # Generate Terrain Button
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 1.5 # Make button taller
        row.operator("ptg.generate_terrain", icon='MESH_PLANE') # Operator for initial generation
        row.operator("ptg.regenerate_terrain", text="Regenerate", icon='FILE_REFRESH') # Operator for regeneration
