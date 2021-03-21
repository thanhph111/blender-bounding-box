# Blender bounding box generator

A Blender add-on for creating simple bounding boxes from selected objects. It creates AABB (axis-aligned bounding box) which based on the active object's coordinate system or world coordinate system.

This add-on will be useful when you need to create a hole on the wall (using *Boolean*) to place your windows or when you need to calculate the size of an object group.

## Installation

1. Open Blender
1. Go to *Edit* > *Preferences*
1. In the *Add-ons* tab, select *Install*
1. Choose the ZIP file downloaded from Github
1. Check the checkbox of the add-on

## Usage

### How it works

The add-on create a bounding box based on selected object and active object.

There are 2 coordinate systems the bounding box axes can align:

- The active object coordinate system: The bounding box axes will align with the axes of the active object.
- The world coordinate system: The bounding box axes will align with the global coordinate system.

There are some helpful switches :

- Separate active object: Active object will not contribute vertices to the bounding box.
- Display as wireframe: Display bounding box under wireframe display type.
- Show in Renders: Show bounding box in rendered scenes.

Active object can be various types of object (*Empties*, *Lights*, *Cameras*...) but only mesh objects in selected objects affect the result. All scenarios are shown in the table below.

### How to call

You can run the operator from the *Search Menu* (`F3`) or from *Add Menu* (`Shift` + `A`).\
If you cannot find the operator or the *Bounding box* button is fade out, you need to select something first.

### A demo

![Demo](assets/screencast.gif)

### A list of scenarios

| Separate active object | Selected objects                           | Active object | Behavior                                                     |
| :--------------------- | :----------------------------------------- | :------------ | :----------------------------------------------------------- |
| TRUE                   | None                                       | None          | ~~Cancel~~                                                   |
| TRUE                   | None                                       | **Mesh**      | ~~Cancel~~                                                   |
| TRUE                   | None                                       | *not Mesh*    | ~~Cancel~~                                                   |
| TRUE                   | **List of meshes contain active object**   | None          | ~~Unknown~~                                                  |
| TRUE                   | **List of meshes contain active object**   | **Mesh**      | **Remove active object from selected objects**               |
| TRUE                   | **List of meshes contain active object**   | *not Mesh*    | ~~Unknown~~                                                  |
| TRUE                   | *List of meshes not contain active object* | None          | **Pick first object from selected objects as active object** |
| TRUE                   | *List of meshes not contain active object* | **Mesh**      | *Create bounding box normally*                               |
| TRUE                   | *List of meshes not contain active object* | *not Mesh*    | *Create bounding box normally*                               |
| FALSE                  | None                                       | None          | ~~Cancel~~                                                   |
| FALSE                  | None                                       | **Mesh**      | **Selected objects is active object**                        |
| FALSE                  | None                                       | *not Mesh*    | ~~Cancel~~                                                   |
| FALSE                  | **List of meshes contain active object**   | None          | ~~Unknown~~                                                  |
| FALSE                  | **List of meshes contain active object**   | **Mesh**      | *Create bounding box normally*                               |
| FALSE                  | **List of meshes contain active object**   | *not Mesh*    | ~~Unknown~~                                                  |
| FALSE                  | *List of meshes not contain active object* | None          | **Pick first object from selected objects as active object** |
| FALSE                  | *List of meshes not contain active object* | **Mesh**      | *Create bounding box normally*                               |
| FALSE                  | *List of meshes not contain active object* | *not Mesh*    | *Create bounding box normally*                               |

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
