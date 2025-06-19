import bpy
import os
import subprocess
import json
import numpy as np

GLOBAL_PYTHON_EXE = r"C:\Users\HP\AppData\Local\Programs\Python\Python310\python.exe"
TERRAIN_PY_FILE = r"D:\Codes\Projects\Procedural 3D Terrain Generator\perlin_height_map.py"

def terrain_mesh_generator(height_map):
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

def ipc_external_terrain_generator(param = None, height = 100, width = 100):
    
    commands = [GLOBAL_PYTHON_EXE, TERRAIN_PY_FILE]
    if param != None:
        commands = [GLOBAL_PYTHON_EXE, TERRAIN_PY_FILE, param]
    
    try:
        process = subprocess.run(commands, capture_output = True, text = True, check = True)
        height_list = json.loads(process.stdout)
        height_map = np.array(height_list, dtype=np.float64).reshape(height, width)
        terrain_mesh_generator(height_map)   
    except Exception as e:
        print(f"Error:{e}")

ipc_external_terrain_generator()
