import bpy
import os
import subprocess
import json
import numpy as np

GLOBAL_PYTHON_EXE = r"C:\Users\HP\AppData\Local\Programs\Python\Python310\python.exe"
TERRAIN_PY_FILE = r"D:\Codes\Projects\Procedural 3D Terrain Generator\perlin_height_map.py"

class Terrain_Generator:
    def __init__(self):
        self.view_height = 100
        self.view_width = 100
        
        # perlin noise parameters for terrain (base)
        self.terrain_scale = 100.0 
        self.terrain_octaves = 6 
        self.terrain_persistence = 0.5 
        self.terrain_lacunarity = 2.0
        self.terrain_seed = 1000
        
        # perlin noise parameters for height
        self.height_scale = 1000.0
        self.height_octaves = 6
        self.height_persistence = 0.5
        self.height_lacunarity = 2.0
        self.height_seed = 200
        self.min_height = 10
        self.max_height = 200

        self.offset_x = 0
        self.offset_y = 0
        
    def set_parameters(self, view_height = 100, view_width = 100, 
                   terrain_scale = 100.0, terrain_octaves = 6, 
                   terrain_persistence = 0.5, terrain_lacunarity = 2.0, 
                   terrain_seed = 1000, 
                   offset_x = 0, offset_y = 0,
                   height_scale = 1000, height_octaves = 6,
                   height_persistence = 0.5, height_lacunarity = 2.0,
                   height_seed = 200, min_height = 10, max_height = 200):
        
        self.view_height = view_height
        self.view_width = view_width
        
        # perlin noise parameters for terrain (base)
        self.terrain_scale = terrain_scale
        self.terrain_octaves = terrain_octaves 
        self.terrain_persistence = terrain_persistence 
        self.terrain_lacunarity = terrain_lacunarity
        self.terrain_seed = terrain_seed
        
        # perlin noise parameters for height
        self.height_scale = height_scale
        self.height_octaves = height_octaves
        self.height_persistence = height_persistence
        self.height_lacunarity = height_lacunarity
        self.height_seed = height_seed
        self.min_height = min_height
        self.max_height = max_height

        self.offset_x = offset_x
        self.offset_y = offset_y
        param = {
        'view_height': view_height,
        'view_width': view_width,
        'terrain_scale': terrain_scale,
        'terrain_octaves': terrain_octaves,
        'terrain_persistence': terrain_persistence,
        'terrain_lacunarity': terrain_lacunarity,
        'terrain_seed': terrain_seed,
        'offset_x': offset_x,
        'offset_y': offset_y,
        'height_scale': height_scale,
        'height_octaves': height_octaves,
        'height_persistence': height_persistence,
        'height_lacunarity': height_lacunarity,
        'height_seed': height_seed,
        'min_height': min_height,
        'max_height': max_height
        }
        self.ipc_external_terrain_generator(param = param, height = view_height, width = view_width)

    def terrain_mesh_generator(self, height_map):
        # assign the vertices with x, y, z cordinates based on height map
        vertices = []
        num_verts_x = len(height_map)
        num_verts_y = len(height_map[0])
        for x in range(num_verts_x):
            for y in range(num_verts_y):
                vertices.append((x, y, height_map[x][y]))
        
        # Generates the faces
        faces = []
        for x in range(num_verts_x - 1):
            for y in range(num_verts_y - 1):
                p1_index = x * num_verts_y + y
                p2_index = x * num_verts_y + (y + 1)
                p3_index = (x +1) * num_verts_y + y
                p4_index = (x +1) * num_verts_y + (y + 1)
                
                faces.append((p1_index, p2_index, p3_index))
                faces.append((p2_index, p3_index, p4_index))
        
        # use the vertices and faces to generate the mesh
        # deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Create new mesh data-block
        mesh_data = bpy.data.meshes.new("Terrain")
        
        # Populate mesh data from our vertices and faces
        # The second argument is for edges, which we leave empty as faces define edges
        mesh_data.from_pydata(vertices, [], faces)
        mesh_data.update() # Update the mesh data

        # Create a new object that uses this mesh data
        obj = bpy.data.objects.new("Terrain_object", mesh_data)

        # Link the object to the current scene's collection
        bpy.context.collection.objects.link(obj)

        # Select the newly created object and make it active
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

    def ipc_external_terrain_generator(self, param = None, height = 100, width = 100):
        
        commands = [GLOBAL_PYTHON_EXE, TERRAIN_PY_FILE]
        if param != None:
            param_json_str = json.dumps(param)
            commands = [GLOBAL_PYTHON_EXE, TERRAIN_PY_FILE, param_json_str]
            
        try:
            process = subprocess.run(commands, capture_output = True, text = True, check = True)
            height_list = json.loads(process.stdout)
            height_map = np.array(height_list, dtype=np.float64).reshape(height, width)
            self.terrain_mesh_generator(height_map)   
        except Exception as e:
            print(f"Blender Error:{e}")


TG = Terrain_Generator()
TG.set_parameters(view_height = 400, view_width = 200)
