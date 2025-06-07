import noise
from matplotlib import pyplot as plt
import random

length=500
scale=100.0
octaves=6
persistence=0.5
lacunarity=2.0
time = [t for t in range(length)]
random_noise = [random.random() for _ in range(length)]

perlin_noise = [noise.pnoise1(i / scale,octaves=octaves,persistence=persistence,lacunarity=lacunarity,repeat=length,base=0) for i in range(length)]


plt.figure(figsize=(10, 7))

plt.subplot(2, 1, 1)
plt.plot(time, random_noise, color ="#06daff")
plt.xlabel("Time")
plt.ylabel("Random noise")
plt.title("Random noise")
plt.grid()
ax = plt.gca()
ax.set_facecolor(color="#434343")

plt.subplot(2, 1, 2)
plt.plot(time, perlin_noise, color ="orange")
plt.xlabel("Time")
plt.ylabel("Perlin noise")
plt.title("Perlin noise")
plt.grid()
ax = plt.gca()
ax.set_facecolor(color="#434343")


plt.tight_layout()
plt.show()