# Blender bounding box generator

An Blender add-on for creating simple bounding boxes from selected objects. It have not supported creating minimal bounding boxes yet. It is currently created AABB (axis-aligned bounding box) which based on the active object's coordinate system or world coordinate system.

## Setup environment for development

I am using:
- Editor: **Visual Studio Code**
- Linter: **Flake8**
- Formatter: **Black**
- Environment manager: **pipenv**

These steps will show how to set up a python virtual environment that fits my workflow.

1. Open CLI in the project directory.
1. Run following command `python -m venv .venv`. A **.venv** folder will appear in the project folder.
1. Then run this `pipenv install --dev` to install packages for development.
1. After that, a virtual environment has been setup. You can get in using `pipenv shell` and get out with `exit`. Once activated, you will have all packages you need.
