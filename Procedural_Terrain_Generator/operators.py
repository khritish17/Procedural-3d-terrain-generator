import bpy
import os
import json
import subprocess
import numpy as np

class PTG_Generate_Terrain_Mesh:
    """
        The whole terrain generation module
    """
    def __init__(self, addon_dir):
        self.addon_dir = addon_dir
        self.PYTHON_EXE = self.get_python_exe()
        self.PERLIN_FILE = os.path.join(self.addon_dir, "perlin_height_map.py")
    
    def get_python_exe(self):
        # reads the global python executable path from 'python_exe_path.txt'
        # if the file does not exist, error in initialization
        try:
            python_exe_path = os.path.join(self.addon_dir, "python_exe_path.txt")
            with open(python_exe_path, "r") as f:
                lines = f.readlines()
                return lines[0].strip("\n")
        except:
            print("-> PTG log: [Error] No Python executable found !!!!")
            return None
    
    def terrain_mesh_generator(self, height_map_array, obj_name="PTG_Terrain_object"):
        # Generates a mesh in Blender from a 2D NumPy height map.
        # Handles mesh creation, vertex assignment, and face generation.
        
        # Ensure a valid height map array is provided
        if not isinstance(height_map_array, np.ndarray) or height_map_array.ndim != 2:
            print("ERROR: Invalid height_map provided. Expected a 2D NumPy array.")
            return None

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
        
        # retrieve the object in the scene, with the object name
        obj = bpy.data.objects.get(obj_name)
        mesh_data = None
        if obj and obj.type == 'MESH':
            # if the object with the object name is a mesh object (i.e generate terrain) 
            mesh_data = obj.data
            print(f"-> PTG log: Updating existing mesh data for object: {obj_name}")
        else:
            # if no such object exists, create a mesh object with the object name
            mesh_data = bpy.data.meshes.new(obj_name + "_Mesh")
            obj = bpy.data.objects.new(obj_name, mesh_data)
            bpy.context.collection.objects.link(obj)
            print(f"-> PTG log: Created new mesh object: {obj_name}")

        if bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode='OBJECT')

        mesh_data.clear_geometry()
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update(calc_edges=True)
        mesh_data.validate()

        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        print(f"-> PTG log: Mesh '{obj_name}' updated/generated with {len(vertices)} vertices and {len(faces)} faces.")
        return obj

    def ipc_perin_map_computation(self, params):
        
        params_json_str = json.dumps(params)
        commands = [self.PYTHON_EXE, self.PERLIN_FILE, params_json_str]

        try:
            process = subprocess.run(commands, capture_output = True, text = True, check = True)
            height_list = json.loads(process.stdout)
            height_map = np.array(height_list, dtype=np.float64).reshape(params['view_height'], params['view_width'])
            return height_map
        except Exception as e:
            print(f"-> PTG log: [Error] {e}")
        return None


class PTG_Generate_Operator(bpy.types.Operator):
    bl_idname = "ptg.generate_terrain"
    bl_label = "Generate Terrain"
    bl_description = "Generates a new procedural terrain mesh."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        ptg_props = scene.ptg_props
        # here goes the code for to call the Terrain Generation
        # configure the parameters for terrain generation
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
        addon_dir = os.path.dirname(bpy.path.abspath(__file__))
        mesh_generator = PTG_Generate_Terrain_Mesh(addon_dir=addon_dir)
        height_map = mesh_generator.ipc_perin_map_computation(params=params)

        if height_map is not None:
            mesh_generator.terrain_mesh_generator(height_map_array=height_map, obj_name="PTG_Terrain_object")
            self.report({'INFO'}, "Terrain generated successfully!")
            return {'FINISHED'}
        else:
            print("-> PTG log: [Error] issues in generating height_map !!!")
            self.report({'ERROR'}, "Failed to generate terrain height map.")
            return {'CANCELLED'}

