import noise
from matplotlib import pyplot as plt
import math

length=500
scale=100.0
octaves=6
persistence=0.5
lacunarity=2.0


perlin_freq = {}
for i in range(100000):
    p = noise.pnoise1(i / scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeat=length,base=1)
    p = round(p, 3)
    if p in perlin_freq:
        perlin_freq[p] += 1
    else:
        perlin_freq[p] = 1
x, y = [], []
for k, v in perlin_freq.items():
    x.append(k)
    y.append(v)
plt.subplot(2, 1, 1)
ax = plt.gca()
ax.set_facecolor(color="#434343")
plt.bar(x, y, width=0.001, color = "#ead289")
plt.xlabel("Perlin Value")
plt.ylabel("Frequency")
plt.show()