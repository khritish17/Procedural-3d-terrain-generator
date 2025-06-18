"""
This is the core file for height map generation using composite 
2D Perlin noise.
This code is used for the purpose of IPC - Inter Process Communication
"""

import numpy as np
import noise 
import json
import sys

def perlin_height_map_api(json_param):
    # Create a Perlin_height_map object
    PHM = Perlin_Height_Map()
    if json_param:
        param = json.loads(json_param)
        view_height = param['view_height']
        view_width = param['view_width']
        terrain_scale = param['terrain_scale']
        terrain_octaves = param['terrain_octaves']
        terrain_persistence = param['terrain_persistence']
        terrain_lacunarity = param['terrain_lacunarity']
        terrain_seed = param['terrain_seed']
        offset_x = param['offset_x']
        offset_y = param['offset_y']
        height_scale = param['height_scale']
        height_octaves = param['height_octaves']
        height_persistence = param['height_persistence']
        height_lacunarity = param['height_lacunarity']
        height_seed = param['height_seed']
        min_height = param['min_height']
        max_height = param['max_height']
        PHM.set_parameters(view_height = view_height, view_width = view_width, 
                       terrain_scale = terrain_scale, terrain_octaves = terrain_octaves, 
                       terrain_persistence = terrain_persistence, terrain_lacunarity = terrain_lacunarity, 
                       terrain_seed = terrain_seed, 
                       offset_x = offset_x, offset_y = offset_y,
                       height_scale = height_scale, height_octaves = height_octaves,
                       height_persistence = height_persistence, height_lacunarity = height_lacunarity,
                       height_seed = height_seed, min_height = min_height, max_height = max_height)
    height_map = PHM.generate_terrain_map()
    return height_map.flatten().tolist()

class Perlin_Height_Map:
    def __init__(self, view_height = 256, view_width = 256):
        self.shape = (view_height, view_width) 
        self.offset = (0, 0) # (offset_x, offset_y)
        
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
        """
        Parameters:
            shape (tuple):        The dimensions of the noise array (width, height).
            scale (float):        Determines how zoomed in or out the noise appears.
                                  Smaller values create smoother, larger features.
            octaves (int):        The number of noise layers to combine. More octaves
                                  add more detail.
            persistence (float):  How much each successive octave contributes to the
                                  overall shape. Values typically between 0 and 1.
            lacunarity (float):   How much the frequency increases for each successive
                                  octave. A value of 2.0 means each octave is twice
                                  as fine as the previous one.
            seed (int): A seed for the random number generator, ensuring
                                  reproducible noise patterns. If None, a random
                                  seed will be used.
        """
    
    def set_parameters(self, view_height = 256, view_width = 256, 
                       terrain_scale = 100.0, terrain_octaves = 6, 
                       terrain_persistence = 0.5, terrain_lacunarity = 2.0, 
                       terrain_seed = 1000, 
                       offset_x = 0, offset_y = 0,
                       height_scale = 1000, height_octaves = 6,
                       height_persistence = 0.5, height_lacunarity = 2.0,
                       height_seed = 200, min_height = 10, max_height = 200):
        # perlin noise parameters for terrain (base)
        self.shape = (view_height, view_width)
        self.terrain_scale = terrain_scale
        self.terrain_octaves = terrain_octaves
        self.terrain_persistence = terrain_persistence
        self.terrain_lacunarity = terrain_lacunarity
        self.terrain_seed = terrain_seed
        self.offset = (offset_x, offset_y)
        
        # perlin noise parameters for height
        self.height_scale = height_scale
        self.height_octaves = height_octaves
        self.height_persistence = height_persistence
        self.height_lacunarity = height_lacunarity
        self.height_seed = height_seed
        self.min_height = min_height
        self.max_height = max_height

    def generate_terrain_map(self):
        view_port = np.zeros(self.shape)
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                new_x = (x + self.offset[0]) / self.terrain_scale
                new_y = (y  + self.offset[1]) / self.terrain_scale
                # 2D perlin noise for the terrain 
                base_noise = noise.snoise2(new_x, new_y, 
                                         octaves = self.terrain_octaves,
                                         persistence = self.terrain_persistence,
                                         lacunarity = self.terrain_lacunarity,
                                         base = self.terrain_seed,
                                         repeatx = self.shape[0],
                                         repeaty = self.shape[1])
                # 2D perlin noise for the height manipulation
                height_noise = noise.snoise2(new_x, new_y, 
                                         octaves = self.height_octaves,
                                         persistence = self.height_persistence,
                                         lacunarity = self.height_lacunarity,
                                         base = self.height_seed,
                                         repeatx = self.shape[0],
                                         repeaty = self.shape[1])
                normalized_height_noise = (height_noise + 1)/2

                modulated_height  = base_noise * normalized_height_noise
                # linear interpolation to map the modulated height range from [-1, 1] to [min_height, max_height]
                height = self.min_height + (modulated_height + 1) * ((self.max_height - self.min_height)/2)
                view_port[x][y] = height
        return view_port

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # parameters has been provided 
        json_param = sys.argv[1]
    else:
        # go with the default values
        json_param = None
    try:
        height_list = perlin_height_map_api(json_param=json_param)
        # print the height map output to std out
        print(json.dumps(height_list))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

