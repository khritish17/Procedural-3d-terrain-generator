# importing standard libraries
import numpy as np
import noise 
import random

class Perlin3d:
    def __init__(self, height = 256, width = 256):
        self.shape = (height, width) 
        self.scale = 100.0 
        self.octaves = 6 
        self.persistence = 0.5 
        self.lacunarity = 2.0
        self.seed = 1000
        self.offset = (0, 0) # (offset_x, offset_y)
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
    
    def set_parameters(self, height = 256, width = 256, scale = 100, octaves = 6, persistence = 0.5, lacunarity = 2.0, seed = 1000, offset_x = 0, offset_y = 0):
        self.shape = (height, width)
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed
        self.offset = (offset_x, offset_y)
        
    def generate_perlin_noise(self):
        perlin_noise = np.zeros(self.shape)
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                new_x = (x + self.offset[0]) / self.scale
                new_y = (y  + self.offset[1]) / self.scale
                perlin_noise[x][y] = noise.snoise2(new_x, new_y, 
                                                        octaves = self.octaves,
                                                        persistence = self.persistence,
                                                        lacunarity = self.lacunarity,
                                                        base = self.seed,
                                                        repeatx = self.shape[0],
                                                        repeaty = self.shape[1])
        return perlin_noise
    
    def generate_height_map(self):
        # get the perlin noise for terrain base
        perlin_noise = self.generate_perlin_noise() # value ranges : [-1, +1]
        random.seed(self.seed)
        random_delta = random.randint(10, 10000)
        scale_delta = random.randint(1, 10)
        self.seed += random_delta
        self.scale *= scale_delta # base terain is (small scale) : generates small bumpy features
                                  # height terain is (high scale): generate large sweeping region 

        # get another perlin noise for using it as a height_multiplier
        height_noise = self.generate_perlin_noise() # value ranges : [-1, +1]

        # back to original parameters 
        self.seed -= random_delta
        self.scale /= scale_delta

        # modulated height

P = Perlin3d()
P.set_parameters(height=2, width=3)
P.generate_perlin_noise()