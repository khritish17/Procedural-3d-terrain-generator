## Setup/Installation
 **Microsoft Visual C++ 14.0 or greater is required**
 
Steps to install:
- Download Visual Studio Build Tools:
  - Go to the official Visual Studio downloads page: https://visualstudio.microsoft.com/downloads/
  - Scroll down to the "Tools for Visual Studio" section.
  - Look for "Build Tools for Visual Studio 2022" (or the latest available version, e.g., 2019). Click the `Download` button next to it.
- Run the Installer:
  - Once the `vs_buildtools__*.exe` file is downloaded, run it.
  - The Visual Studio Installer will open.
- Select Workloads:
  - In the installer, go to the `Workloads` tab.
  - Crucially, select `Desktop development with C++`. This workload includes the C++ compilers and libraries that Python needs.
- Install:
  - Click the `Install` button. The installation might take some time as it downloads and sets up the components.
- Restart (Optional but Recommended):
  - After the installation completes, it's a good idea to restart your computer, although it's not always strictly necessary. This ensures all environment variables are correctly set.

**Steps to setup environment and resolve dependencies:**
1. First create a virtual environment, use the `env_config.py` file and follow the instructions prompted to automatically generate the virtual environment
2. Get the activator syntax and activate the environmet, available in the `env_config.py` file
3. The `env_config.py` file consists of the dependency resolver to install libraries automatically



## Random Noise vs Perlin Noise

<img src ="Images/random_vs_perlin.png" width = "1500">

## Perlin Noise (2 Dimensional) (simple 2d map geneartion)
<img src ="Images/perlin_2d_map_generation_seed_1000.png" width = "1500">

> Image generation through matplotlib is costly (heavy time consuming). Hence PIL library in python for image manipulation is used.
