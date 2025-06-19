import bpy
import os
import subprocess
import json
import numpy as np

GLOBAL_PYTHON_EXE = r"C:\Users\HP\AppData\Local\Programs\Python\Python310\python.exe"
TERRAIN_PY_FILE = r"D:\Codes\Projects\Procedural 3D Terrain Generator\perlin_height_map.py"
print("--")
# run the TERRAIN_PY_FILE
try:
    print("Height map init")
    commands = [GLOBAL_PYTHON_EXE, TERRAIN_PY_FILE]
    process = subprocess.run(commands, capture_output=True, text = True, check = True)
    height_list = json.loads(process.stdout)
    height_map = np.array(height_list, dtype=np.float).reshape(100, 100)
    print("Height_map completed")
    print(height_map)
    
    num_verts_y = len(height_map[0])
    num_verts_x = len(height_map)
    vertices = []
    for y in range(num_verts_y): # Outer loop for Y (rows)
        for x in range(num_verts_x): # Inner loop for X (columns)
            vertices.append((x, y, height_map[x][y]))

    # --- 2. Generate Faces (Triangles) ---
    faces = []
    # Iterate over the quads, which are formed by (num_verts_x-1) x (num_verts_y-1) grid cells
    for y_quad_idx in range(num_verts_y - 1):
        for x_quad_idx in range(num_verts_x - 1):
            idx_bottom_left = y_quad_idx * num_verts_x + x_quad_idx
            idx_bottom_right = y_quad_idx * num_verts_x + (x_quad_idx + 1)
            idx_top_left = (y_quad_idx + 1) * num_verts_x + x_quad_idx
            idx_top_right = (y_quad_idx + 1) * num_verts_x + (x_quad_idx + 1)

            faces.append((idx_bottom_left, idx_bottom_right, idx_top_right))
            faces.append((idx_bottom_left, idx_top_right, idx_top_left))

    # --- 3. Create a new Mesh object in Blender ---
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')

    # Create new mesh data-block
    mesh_data = bpy.data.meshes.new("CustomGridMesh")

    # Populate mesh data from our vertices and faces
    # The second argument is for edges, which we leave empty as faces define edges
    mesh_data.from_pydata(vertices, [], faces)
    mesh_data.update() # Update the mesh data

    # Create a new object that uses this mesh data
    obj = bpy.data.objects.new("CustomGridObject", mesh_data)

    # Link the object to the current scene's collection
    bpy.context.collection.objects.link(obj)

    # Select the newly created object and make it active
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

except Exception as e:
    print(f"Error:{e}")