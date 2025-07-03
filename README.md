# Procedural Terrain Generator (PTG) - Blender Addon
## Content
- Blender Addon Installation Guide
  - Install Python
  - Install Microsoft c++ 14.0 or higher
  - Install the python library dependencies
  - Install the addon in blender 
- Blender Quick Tutorial and Demo
- Why noise lib over Builtin Blender Noise
- Perlin Noise Preimer
- Addon - code - documentation
## PTG Blender-Addon Installation Guide
>📌
>The **"Procedural Terrain Generator"** addon uses the `noise` Python library for Perlin noise. Since `noise` is a C extension, it requires Python development headers, which are not included in Blender's embedded Python.
>
>To work around this and keep Blender responsive, we use Inter-Process Communication (IPC). This means:
>- Blender's Python handles the UI and Blender API.
>- A separate, globally installed Python (with the noise library) performs the heavy noise calculations. This offloads computation and prevents Blender from freezing.
>
> **To use this addon, you need:**
> - Python 3.x (globally installed on your system)
> - Microsoft Visual C++ 14.0 or higher (for Windows, a C++ compiler for noise library compilation)

### Install Python
<details>
  <summary>How to install Python (click to expand)</summary>

  >**Python 3.x (globally installed on your system)**
  >
  > Having a global Python installation is crucial for your Blender addon's IPC system.
  >
  > Steps to install:
  >
  > **For Windows:**
  > - **Download the Installer:**
  >     - Go to the official Python website: https://python.org/downloads/windows/
  >     - Look for the latest stable **Python 3.x.x** version (e.g., Python 3.10.x, 3.11.x, or 3.12.x).
  >     - Download the "**Windows installer (64-bit)**" executable.
  > - **Run the Installer:**
  >     - Locate the downloaded `.exe` file and double-click it to run.
  >     - **Crucial Step:** On the first screen of the installer, check the box that says "**Add Python X.Y to PATH**" (where X.Y is your Python version). This is very important for your addon to find Python.
  >     - Select "**Install Now**" (recommended for most users).
  >     - If prompted by User Account Control (UAC), click "Yes".
  > - **Complete Installation**
  >     - The installation will proceed. Once finished, you might see a "Setup was successful" message.
  >     - Click "Close".
  > - **Verify Installation:**
  >     - Open a **new** Command Prompt window (search for `cmd` in Start Menu).
  >     - Type `python --version` and press Enter.
  >     - You should see the installed Python version (e.g., `Python 3.10.10`).
  >     - If it says "Python is not recognized...", close the Command Prompt and open a new one. If it still doesn't work, you might need to manually add Python to your PATH or reinstall, ensuring the "Add to PATH" box was checked.
 >
 > **For macOS:**
 > - **Check for Pre-installed Python (and Homebrew):**
 >      - macOS often comes with an older Python 2.x. For Python 3.x, it's highly recommended to use a package manager like Homebrew.
 >      - Open **Terminal** (Applications > Utilities > Terminal).
 >      - Check if Homebrew is installed: `brew --version`
 >      - If not installed, install Homebrew:
 >      ````
 >       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
 >       
 >>  Follow the on-screen instructions, which might include running `brew doctor` and adding Homebrew to your PATH.
 > - **Install Python 3 using Homebrew:**
 >      - Once Homebrew is installed, run:
 > 
 >       brew install python
 >      - Homebrew will install the latest Python 3.x and link it correctly.
 > - **Verify Installation:**
 >      - In the same Terminal window (or open a new one), type `python3 --version` and press Enter.
 >      - You should see the installed Python 3.x version (e.g., `Python 3.10.10`).
 >      - `python --version` might still point to an older Python 2.x, but `python3` will point to the Homebrew installed version. Your addon's `util.py` is designed to find `python` or `python3`.
 >
 >**For Linux (Ubuntu/Debian-based):**
 > - **Check for Python 3:**
 >      - Most modern Linux distributions come with Python 3 pre-installed.
 >      - Open **Terminal**.
 >      - Type `python3 --version` and press Enter. You'll likely see a version like `Python 3.8.10` or newer.
 > - **Install if Missing or for Specific Version:**
 >      - If Python 3 is not installed or you need a specific version, use your distribution's package manager.
 >      - For Ubuntu/Debian-based systems:
 >        ````
>         sudo apt update
>         sudo apt install python3
>         sudo apt install python3-pip # Install pip for Python 3
>         sudo apt install python3-dev # Essential for compiling C extensions like 'noise'
 >         ````
 >          - `python3-dev` (or similar package name like `python3-devel` on Fedora/RHEL) provides the necessary Python development headers.
 > - **Verify Installation:**
 >       -  Type `python3 --version` and `pip3 --version` to confirm.


</details>

### Install Microsoft Visual C++ 14.0 or greater

<details>
  <summary>How to install Microsoft Visual C++ (click to expand)</summary>

  >**Microsoft Visual C++ 14.0 or greater is required**
  >
  >Steps to install:
  >
  >- Download Visual Studio Build Tools:
  >    - Go to the official Visual Studio downloads page: https://visualstudio.microsoft.com/downloads/
  >    - Scroll down to the "Tools for Visual Studio" section.
  >    - Look for "Build Tools for Visual Studio 2022" (or the latest available version, e.g., 2019). Click the `Download` button next to it.
  >- Run the Installer:
  >    - Once the `vs_buildtools__*.exe` file is downloaded, run it.
  >    - The Visual Studio Installer will open.
  >- Select Workloads:
  >    - In the installer, go to the `Workloads` tab.
  >    - Crucially, select `Desktop development with C++`. This workload includes the C++ compilers and libraries that Python needs.
  >- Install:
  >    - Click the `Install` button. The installation might take some time as it downloads and sets up the components.
  >- Restart (Optional but Recommended):
  >    - After the installation completes, it's a good idea to restart your computer, although it's not always strictly necessary. This ensures all environment variables are correctly set.
</details>

###  Install the python library dependencies
After installing the Python and Microsoft Visual C++, download the Addon Installer Package [from here]() 

open your terminal/command prompt in the downloaded directory and run:

```Bash
pip install -r requirements.txt
```
## Random Noise vs Perlin Noise

<img src ="Images/random_vs_perlin.png" width = "1500">

## Perlin Noise - Normal (Bell Curve) Behaviour
<img src ="Images/perlin_bell_curve.png" width = "1500">

## Perlin Noise (2 Dimensional) (simple 2d map geneartion)
<img src ="Images/perlin_2d_map_generation_seed_1000.png" width = "1500">

> Image generation through matplotlib is costly (heavy time consuming). Hence PIL library in python for image manipulation is used.


## Terrain Generation (Composite perlin noise approach)
<img src ="Images/terrain_3d.png" width = "1500">
