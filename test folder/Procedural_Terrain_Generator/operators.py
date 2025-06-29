import bpy
import os
import subprocess
import json
import numpy as np

class TerrainGeneratorLogic:
    """
    Encapsulates the core logic for terrain generation and IPC,
    separated from Blender's Operator class.
    """
    def __init__(self, addon_dir):
        self.addon_dir = addon_dir
        self.GLOBAL_PYTHON_EXE_PATH_FILE = os.path.join(self.addon_dir, "global_python_path.txt")
        self.PERLIN_PY_FILE = os.path.join(self.addon_dir, "perlin_height_map.py")
        # load the abs path of the python executable from the GLOBAL_PYTHON_EXE_PATH_FILE
        self.global_python_exe = self._get_global_python_exe()

    def _get_global_python_exe(self):
        """Reads the global Python executable path from the file."""
        if not os.path.exists(self.GLOBAL_PYTHON_EXE_PATH_FILE):
            print(f"ERROR: '{self.GLOBAL_PYTHON_EXE_PATH_FILE}' not found. "
                  "Please ensure the addon has run its initial setup correctly.")
            return None
        with open(self.GLOBAL_PYTHON_EXE_PATH_FILE, "r") as f:
            return f.read().strip()

    def terrain_mesh_generator(self, height_map_array, obj_name="Terrain"):
        """
        Generates a mesh in Blender from a 2D NumPy height map.
        Handles mesh creation, vertex assignment, and face generation.
        """
        # Ensure a valid height map array is provided
        if not isinstance(height_map_array, np.ndarray) or height_map_array.ndim != 2:
            print("ERROR: Invalid height_map provided. Expected a 2D NumPy array.")
            return None

        # Clear existing mesh (optional, can be controlled by operator properties)
        # bpy.ops.object.select_all(action='DESELECT')
        # if obj_name in bpy.data.objects:
        #     obj_to_remove = bpy.data.objects[obj_name]
        #     bpy.data.objects.remove(obj_to_remove, do_unlink=True)


        num_verts_x, num_verts_y = height_map_array.shape

        # Assign the vertices with x, y, z coordinates based on height map
        vertices = []
        for x in range(num_verts_x):
            for y in range(num_verts_y):
                vertices.append((x, y, height_map_array[x, y])) # Use [x, y] for numpy indexing

        # Generates the faces
        faces = []
        for x in range(num_verts_x - 1):
            for y in range(num_verts_y - 1):
                # Each square creates two triangles
                p1_index = x * num_verts_y + y
                p2_index = x * num_verts_y + (y + 1)
                p3_index = (x + 1) * num_verts_y + y
                p4_index = (x + 1) * num_verts_y + (y + 1)

                # Triangle 1
                faces.append((p1_index, p2_index, p4_index))
                # Triangle 2
                faces.append((p1_index, p4_index, p3_index))

        # Create new mesh data-block
        mesh_data = bpy.data.meshes.new(obj_name)

        # Populate mesh data from our vertices and faces
        # The second argument is for edges, which we leave empty as faces define edges
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update() # Update the mesh data

        # Create a new object that uses this mesh data
        obj = bpy.data.objects.new(obj_name + "_object", mesh_data)

        # Link the object to the current scene's collection
        bpy.context.collection.objects.link(obj)

        # Select the newly created object and make it active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        print(f"Generated mesh '{obj_name}' with {len(vertices)} vertices and {len(faces)} faces.")
        return obj

    def ipc_external_terrain_generator(self, params):
        """
        Executes the external perlin_height_map.py script to generate height data
        using Inter-Process Communication (IPC).
        """
        if not self.global_python_exe:
            print("ERROR: Global Python executable path not found. Cannot run external script.")
            return None

        if not os.path.exists(self.PERLIN_PY_FILE):
            print(f"ERROR: External Perlin noise script not found at: {self.PERLIN_PY_FILE}")
            return None

        param_json_str = json.dumps(params)
        commands = [self.global_python_exe, self.PERLIN_PY_FILE, param_json_str]

        try:
            print(f"DEBUG: Running external command: {' '.join(commands)}")
            process = subprocess.run(commands, capture_output=True, text=True, check=True)
            # print(f"DEBUG: External script stdout: {process.stdout}")
            # print(f"DEBUG: External script stderr: {process.stderr}")

            # Parse the JSON output from the external script
            height_list = json.loads(process.stdout)

            # Reshape the 1D list back into a 2D NumPy array
            height_map = np.array(height_list, dtype=np.float64).reshape(params['view_height'], params['view_width'])
            return height_map
        except subprocess.CalledProcessError as e:
            print(f"ERROR: External script failed with exit code {e.returncode}")
            print(f"STDOUT:\n{e.stdout}")
            print(f"STDERR:\n{e.stderr}")
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text=f"External script error: {e.stderr[:100]}"),
                title="Terrain Generation Error", icon='ERROR'
            )
            return None
        except json.JSONDecodeError as e:
            print(f"ERROR: Failed to decode JSON from external script output: {e}")
            print(f"Raw output: {process.stdout}")
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text=f"Failed to parse script output: {e}"),
                title="Terrain Generation Error", icon='ERROR'
            )
            return None
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during IPC: {e}")
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text=f"Unexpected error: {e}"),
                title="Terrain Generation Error", icon='ERROR'
            )
            return None


class PTG_OT_GenerateTerrain(bpy.types.Operator):
    """
    Operator to generate a new terrain mesh based on current properties.
    """
    bl_idname = "ptg.generate_terrain"
    bl_label = "Generate Terrain"
    bl_description = "Generates a new procedural terrain mesh."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ptg_props = scene.ptg_props

        # Get addon directory for the TerrainGeneratorLogic
        addon_dir = os.path.dirname(bpy.path.abspath(__file__))
        logic = TerrainGeneratorLogic(addon_dir)

        # Prepare parameters for the external script
        params = {
            'view_height': ptg_props.terrain_length,
            'view_width': ptg_props.terrain_width,
            'terrain_scale': ptg_props.terrain_scale,
            'terrain_octaves': ptg_props.terrain_octaves,
            'terrain_persistence': ptg_props.terrain_persistence,
            'terrain_lacunarity': ptg_props.terrain_lacunarity,
            'terrain_seed': ptg_props.terrain_seed,
            'offset_x': ptg_props.offset_x,
            'offset_y': ptg_props.offset_y,
            'height_scale': ptg_props.height_scale,
            'height_octaves': ptg_props.height_octaves,
            'height_persistence': ptg_props.height_persistence,
            'height_lacunarity': ptg_props.height_lacunarity,
            'height_seed': ptg_props.height_seed,
            'min_height': ptg_props.min_height,
            'max_height': ptg_props.max_height
        }

        # Call the external script via IPC
        height_map = logic.ipc_external_terrain_generator(params=params)

        if height_map is not None:
            # Generate the mesh in Blender
            logic.terrain_mesh_generator(height_map, obj_name="Terrain")
            self.report({'INFO'}, "Terrain generated successfully!")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to generate terrain height map.")
            return {'CANCELLED'}

class PTG_OT_RegenerateTerrain(bpy.types.Operator):
    """
    Operator to regenerate an existing terrain mesh or create a new one if none exists.
    """
    bl_idname = "ptg.regenerate_terrain"
    bl_label = "Regenerate Terrain"
    bl_description = "Regenerates the existing terrain mesh or creates a new one."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ptg_props = scene.ptg_props

        # Get addon directory for the TerrainGeneratorLogic
        addon_dir = os.path.dirname(bpy.path.abspath(__file__))
        logic = TerrainGeneratorLogic(addon_dir)

        # Prepare parameters for the external script
        params = {
            'view_height': ptg_props.terrain_length,
            'view_width': ptg_props.terrain_width,
            'terrain_scale': ptg_props.terrain_scale,
            'terrain_octaves': ptg_props.terrain_octaves,
            'terrain_persistence': ptg_props.terrain_persistence,
            'terrain_lacunarity': ptg_props.terrain_lacunarity,
            'terrain_seed': ptg_props.terrain_seed,
            'offset_x': ptg_props.offset_x,
            'offset_y': ptg_props.offset_y,
            'height_scale': ptg_props.height_scale,
            'height_octaves': ptg_props.height_octaves,
            'height_persistence': ptg_props.height_persistence,
            'height_lacunarity': ptg_props.height_lacunarity,
            'height_seed': ptg_props.height_seed,
            'min_height': ptg_props.min_height,
            'max_height': ptg_props.max_height
        }

        # Call the external script via IPC
        height_map = logic.ipc_external_terrain_generator(params=params)

        if height_map is not None:
            # Remove existing terrain object if it exists and is selected/active
            obj_name = "Terrain_object" # Assuming the object name is consistently "Terrain_object"
            if obj_name in bpy.data.objects:
                obj_to_remove = bpy.data.objects[obj_name]
                bpy.data.objects.remove(obj_to_remove, do_unlink=True)
                print(f"Removed existing object: {obj_name}")

            # Generate the new mesh in Blender
            logic.terrain_mesh_generator(height_map, obj_name="Terrain") # Passing "Terrain" for mesh_data name
            self.report({'INFO'}, "Terrain regenerated successfully!")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to regenerate terrain height map.")
            return {'CANCELLED'}

