# importing standard libraries
import numpy as np
import noise 
from matplotlib import cm
from matplotlib import pyplot as plt


class Perlin3d:
    def __init__(self, height = 256, width = 256):
        self.shape = (height, width) 
        self.scale = 100.0 
        self.octaves = 6 
        self.persistence = 0.5 
        self.lacunarity = 2.0
        self.seed = 1000
        self.offset = (0, 0) # (offset_x, offset_y)

        self.scale_height = 1000.0
        self.octaves_height = 6
        self.persistence_height = 0.5
        self.lacunarity_height = 2.0
        self.seed_height = 200
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
    
    def set_parameters(self, height = 256, width = 256, 
                       scale = 100.0, octaves = 6, 
                       persistence = 0.5, lacunarity = 2.0, 
                       seed = 100, 
                       offset_x = 0, offset_y = 0,
                       scale_height = 1000, octaves_height = 6,
                       persistence_height = 0.5, lacunarity_height = 2.0,
                       seed_height = 200, min_height = 10, max_height = 200):
        self.shape = (height, width)
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed
        self.offset = (offset_x, offset_y)
        
        # height noise parameters
        self.scale_height = scale_height
        self.octaves_height = octaves_height
        self.persistence_height = persistence_height
        self.lacunarity_height = lacunarity_height
        self.seed_height = seed_height
        self.min_height = min_height
        self.max_height = max_height
    
    def generate_terrain_data(self):
        view_port = np.zeros(self.shape)
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                new_x = (x + self.offset[0]) / self.scale
                new_y = (y  + self.offset[1]) / self.scale
                base_noise = noise.snoise2(new_x, new_y, 
                                         octaves = self.octaves,
                                         persistence = self.persistence,
                                         lacunarity = self.lacunarity,
                                         base = self.seed,
                                         repeatx = self.shape[0],
                                         repeaty = self.shape[1])
                height_noise = noise.snoise2(new_x, new_y, 
                                         octaves = self.octaves_height,
                                         persistence = self.persistence_height,
                                         lacunarity = self.lacunarity_height,
                                         base = self.seed_height,
                                         repeatx = self.shape[0],
                                         repeaty = self.shape[1])
                normalized_height_noise = (height_noise + 1)/2

                modulated_height  = base_noise * normalized_height_noise
                # linear interpolation to map the modulated height range from [-1, 1] to [min_height, max_height]
                height = self.min_height + (modulated_height + 1) * ((self.max_height - self.min_height)/2)
                view_port[x][y] = height
        return view_port
    
    def plot3d_matplotlib(self):
        view_port = self.generate_terrain_data()
        X = [i for i in range(len(view_port))]
        Y = [i for i in range(len(view_port[0]))]
        X, Y = np.meshgrid(X, Y)
        Z = view_port
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
        plt.show()


P = Perlin3d()
P.set_parameters(height=100, width=100)
P.plot3d_matplotlib()