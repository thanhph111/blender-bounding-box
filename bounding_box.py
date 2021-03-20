import bpy
from bpy_types import Object
from mathutils import Vector, Euler
from typing import Tuple, List


def set_object_origin_location(origin_location: Vector) -> None:
    """Set object origin with global coordinate.

    Args:
        origin_location (Vector): New origin coordinate to be set.
    """
    # Store the location of current 3d cursor
    old_cursor_location = bpy.context.scene.cursor.location.copy()

    # Give 3d cursor new location
    bpy.context.scene.cursor.location = origin_location

    # Set the origin on the current object to the 3d cursor location
    bpy.ops.object.origin_set(type="ORIGIN_CURSOR")

    # Set 3d cursor location back to the stored location
    bpy.context.scene.cursor.location = old_cursor_location
    del old_cursor_location


def set_bounding_box_origin_to_corner(bounding_box: Object) -> None:
    """Set bounding box origin to first corner.

    Args:
        bounding_box (Object): Bounding box or cube.
    """
    # Get first corner location
    new_origin_location = (
        bounding_box.matrix_world @ bounding_box.data.vertices[0].co
    )
    set_object_origin_location(new_origin_location)


def get_selected_objects_vertices(
    selected_objects: List[Object],
    active_object: Object = None,
    is_align_active_object: bool = False,
) -> List[Vector]:
    """Get all vertices from selected objects in world coordinate system or
    active object coordinate system.

    Args:
        selected_objects (List[Object]): List of objects.
        active_object (Object, optional): Active object. Defaults to None.
        is_align_active_object (bool, optional): Control vertices' coordinates
        based on world coordinate system or active object coordinate system.
        Defaults to False.

    Returns:
        List[Vector]: List of vertices collected from selected objects in
        active object coordinate system.
    """
    vertices = []
    for object in selected_objects:
        vertices.extend(
            [
                object.matrix_world @ vertex.co
                for vertex in object.data.vertices
            ]
        )
    if is_align_active_object:
        vertices = [
            active_object.matrix_world.inverted() @ vertex
            for vertex in vertices
        ]
    return vertices


def get_bounding_box_range(vertices: List[Vector]) -> Tuple[tuple]:
    """Get bounding box vertices range by X, Y, Z axes.

    Args:
        vertices (List[Vector]): List of vertices.

    Returns:
        Tuple[tuple]: List of X, Y, Z ranges
    """
    x_range = [vertex.x for vertex in vertices]
    x_range = (min(x_range), max(x_range))

    y_range = [vertex.y for vertex in vertices]
    y_range = (min(y_range), max(y_range))

    z_range = [vertex.z for vertex in vertices]
    z_range = (min(z_range), max(z_range))

    bounding_box_range = (x_range, y_range, z_range)

    return bounding_box_range


def get_bounding_box_dimensions(
    bounding_box_range: Tuple[tuple],
    active_object: Object = None,
    is_align_active_object: bool = False,
) -> Vector:
    """Get bounding box dimensions in world coordinate system.

    Args:
        bounding_box_range (Tuple[tuple]): List of X, Y, Z ranges
        active_object (Object, optional): Active object. Defaults to None.
        is_align_active_object (bool, optional): Control whether function does
        extra jobs to convert active object coordinate system to world
        coordinate system. Defaults to False.

    Returns:
        Vector: Bounding box dimensions in world coordinate system.
    """
    bounding_box_dimensions = Vector(
        (axis_range[1] - axis_range[0]) for axis_range in bounding_box_range
    )
    if is_align_active_object:
        bounding_box_dimensions = Vector(
            first * second
            for first, second in zip(
                bounding_box_dimensions, active_object.scale
            )
        )
    return bounding_box_dimensions


def get_bounding_box_corner_location(
    bounding_box_range: Tuple[tuple],
    active_object: Object = None,
    is_align_active_object: bool = False,
) -> Vector:
    """Get bounding box corner location in world coordinates system.

    Args:
        bounding_box_range (Tuple[tuple]): List of X, Y, Z ranges
        active_object (Object, optional): Active object. Defaults to None.
        is_align_active_object (bool, optional): Control whether function does
        extra jobs to convert active object coordinate system to world
        coordinate system. Defaults to False.

    Returns:
        Vector: Bounding box corner location in world coordinate system.
    """
    bounding_box_corner_location = Vector(
        axis_range[0] for axis_range in bounding_box_range
    )
    if is_align_active_object:
        bounding_box_corner_location = (
            active_object.matrix_world @ bounding_box_corner_location
        )
    return bounding_box_corner_location


def create_basic_bounding_box(
    bounding_box_corner_location: Vector,
    bounding_box_dimensions: Vector,
    bounding_box_rotation: Euler,
) -> Object:
    """Create bounding box by basic information.

    Args:
        bounding_box_corner_location (Vector): Bounding box corner location.
        bounding_box_dimensions (Vector): Bounding box dimensions.
        bounding_box_rotation (Euler): Bounding box rotations.

    Returns:
        Object: Bounding box
    """
    # Add default cube
    bpy.ops.mesh.primitive_cube_add()
    bounding_box = bpy.context.active_object

    # Move its origin to its corner
    set_bounding_box_origin_to_corner(bounding_box)

    # Assign parameters to the cube
    bounding_box.dimensions = bounding_box_dimensions
    bounding_box.location = bounding_box_corner_location
    bounding_box.rotation_euler = bounding_box_rotation

    return bounding_box


def create_bounding_box(
    selected_objects: List[Object],
    active_object: Object = None,
    is_align_active_object: bool = False,
) -> Object:
    """Create bounding box from selected objects and active object.

    Args:
        selected_objects (List[Object]): List of objects.
        active_object (Object, optional): Active object. Defaults to None.
        is_align_active_object (bool, optional): Control bounding box based on
        world coordinate system or active object coordinate system. Defaults to
        False.

    Returns:
        Object: Bounding box
    """
    # Get bounding box information
    selected_objects_vertices = get_selected_objects_vertices(
        selected_objects=selected_objects,
        active_object=active_object,
        is_align_active_object=is_align_active_object,
    )
    bounding_box_range = get_bounding_box_range(selected_objects_vertices)
    bounding_box_corner_location = get_bounding_box_corner_location(
        bounding_box_range=bounding_box_range,
        active_object=active_object,
        is_align_active_object=is_align_active_object,
    )
    bounding_box_dimensions = get_bounding_box_dimensions(
        bounding_box_range=bounding_box_range,
        active_object=active_object,
        is_align_active_object=is_align_active_object,
    )
    bounding_box_rotation = (
        active_object.rotation_euler
        if is_align_active_object
        else Euler((0, 0, 0), "XYZ")
    )

    # Create bounding box
    bounding_box = create_basic_bounding_box(
        bounding_box_corner_location,
        bounding_box_dimensions,
        bounding_box_rotation,
    )

    # Reset origin and set to bounds display
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")

    return bounding_box


def get_selected_objects_and_active_object(
    is_separate_active_object: bool = False,
) -> Tuple[List[Object], Object]:
    """Return selected objects and active object from context.

    Args:
        is_separate_active_object (bool, optional): Control whether active
        object contribute vertices. Defaults to False.

    Returns:
        Tuple[List[Object], Object]: Selected objects and active object.
    """
    # Get only mesh objects
    selected_objects = [
        object
        for object in bpy.context.selected_objects
        if object.type == "MESH"
    ]
    active_object = bpy.context.active_object

    if is_separate_active_object:
        if active_object:
            if (
                active_object.type == "MESH"
                and active_object in selected_objects
                and selected_objects != [active_object]
            ):
                selected_objects.remove(active_object)
        else:
            if selected_objects and active_object not in selected_objects:
                active_object = selected_objects[0]
    else:
        if active_object:
            if not selected_objects and active_object.type == "MESH":
                selected_objects = [active_object]
        else:
            if selected_objects and active_object not in selected_objects:
                active_object = selected_objects[0]

    return (selected_objects, active_object)


class MESH_OT_bounding_box(bpy.types.Operator):
    """Create a bounding box from selected objects"""

    bl_idname = "mesh.bounding_box"
    bl_label = "Insert Bounding Box"
    bl_options = {"REGISTER", "UNDO"}

    # Define Variables
    coordinate_system: bpy.props.EnumProperty(
        items=[
            (
                "active_object",
                "Active object",
                "Coordinate system of the active object",
            ),
            ("world", "World", "World coordinate system"),
        ],
        name="Coordinate system",
        description="Choose coordinate system to create bounding box",
        default="active_object",
    )
    is_separate_active_object: bpy.props.BoolProperty(
        name="Separate active object",
        description="Active object contribute vertices",
        default=False,
    )
    is_wireframe: bpy.props.BoolProperty(
        name="Wireframe",
        description="Bounding box inserted under wireframe",
        default=False,
    )
    is_render: bpy.props.BoolProperty(
        name="Render", description="Bounding box show in render", default=True
    )

    @classmethod
    def poll(_cls, context):
        (selected_objects, _) = get_selected_objects_and_active_object(
            is_separate_active_object=True
        )
        return bool(selected_objects) and context.area.type == "VIEW_3D"

    def execute(self, _context):
        (
            selected_objects,
            active_object,
        ) = get_selected_objects_and_active_object(
            is_separate_active_object=self.is_separate_active_object
        )

        # Is bounding box based on world coordinate system or active object
        # coordinate system?
        is_align_active_object = (
            True if self.coordinate_system == "active_object" else False
        )

        # Insert bounding box
        if selected_objects and active_object:
            bounding_box = create_bounding_box(
                selected_objects=selected_objects,
                active_object=active_object,
                is_align_active_object=is_align_active_object,
            )

        # Display bounding box under wireframe
        if self.is_wireframe:
            bounding_box.display_type = "WIRE"

        # Whether render bounding box
        bounding_box.hide_render = not self.is_render

        return {"FINISHED"}


def add_menu_draw(self, _context):
    """Draw on Add Menu"""
    self.layout.operator(
        operator=MESH_OT_bounding_box.bl_idname,
        text="Bounding box",
        icon="SHADING_BBOX",
    )


classes = [MESH_OT_bounding_box]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_add.prepend(add_menu_draw)


def unregister():
    bpy.types.VIEW3D_MT_add.remove(add_menu_draw)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
