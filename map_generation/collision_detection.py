import fcl
import numpy as np
import open3d as o3d

from scipy.spatial.transform import Rotation

def visualise_box(box, translation=np.array([0, 0, 0]), rotation=np.eye(3)):
    """
    Visualize a box shape using Open3D.
    :param box: The FCL box object.
    :param translation: Translation vector for positioning the box.
    :param rotation: Rotation matrix for orienting the box.
    :return: Open3D TriangleMesh object representing the box.
    """
    W, H, D = box.side
    mesh = o3d.geometry.TriangleMesh()
    box_mesh = mesh.create_box(W, H, D).translate(translation - 0.5 * np.array([W, H, D])).rotate(rotation)
    return box_mesh

def visualise_cylinder(cylinder, translation=np.array([0, 0, 0])):
    """
    Visualize a cylinder shape using Open3D.
    :param cylinder: The FCL cylinder object.
    :param translation: Translation vector for positioning the cylinder.
    :return: Open3D TriangleMesh object representing the cylinder.
    """
    radius, H = cylinder.radius, cylinder.lz
    mesh = o3d.geometry.TriangleMesh()
    cylinder_mesh = mesh.create_cylinder(radius, H).translate(translation)
    return cylinder_mesh

def visualise_sphere(sphere, translation=np.array([0, 0, 0])):
    """
    Visualize a sphere shape using Open3D.
    :param sphere: The FCL sphere object.
    :param translation: Translation vector for positioning the sphere.
    :return: Open3D TriangleMesh object representing the sphere.
    """
    radius = sphere.radius
    mesh = o3d.geometry.TriangleMesh()
    sphere_mesh = mesh.create_sphere(radius).translate(translation)
    return sphere_mesh

def visualise(*shapes):
    """
    Visualize multiple shapes in a 3D space using Open3D.
    :param shapes: List of Open3D TriangleMesh objects.
    """
    coordinate_frame = o3d.geometry.TriangleMesh().create_coordinate_frame()
    o3d.visualization.draw_geometries(list(shapes) + [coordinate_frame])

def print_collision_result(result):
    """
    Print the result of a collision check between two shapes.
    :param result: The FCL CollisionResult object.
    """
    print("-" * 30)
    print(f"Collision?: {result.is_collision}")
    print(f"Number of contacts: {len(result.contacts)}")
    print("")

def create_box(w, h, d):
    """
    Create an FCL box shape.
    :param w: Width of the box.
    :param h: Height of the box.
    :param d: Depth of the box.
    :return: FCL Box object.
    """
    return fcl.Box(w, h, d)

def create_cylinder(r, l):
    """
    Create an FCL cylinder shape.
    :param r: Radius of the cylinder.
    :param l: Length of the cylinder.
    :return: FCL Cylinder object.
    """
    return fcl.Cylinder(r, l)

def create_sphere(r):
    """
    Create an FCL sphere shape.
    :param r: Radius of the sphere.
    :return: FCL Sphere object.
    """
    return fcl.Sphere(r)

def add_transform(shape, rotation=None, translation=None):
    """
    Add a transformation (rotation and/or translation) to a shape.
    :param shape: The FCL shape object (Box, Cylinder, Sphere).
    :param rotation: Optional rotation matrix.
    :param translation: Optional translation vector.
    :return: FCL CollisionObject with the shape and transformation applied.
    """
    if rotation is None and translation is None:
        transform = fcl.Transform()
    elif rotation is not None and translation is not None:
        transform = fcl.Transform(rotation, translation)
    elif rotation is not None:
        transform = fcl.Transform(rotation)
    else:
        transform = fcl.Transform(translation)
    return fcl.CollisionObject(shape, transform)

def check_collision(s1, s2):
    """
    Check for collision between two shapes.
    :param s1: FCL CollisionObject 1.
    :param s2: FCL CollisionObject 2.
    :return: FCL CollisionResult indicating if a collision occurred.
    """
    req = fcl.CollisionRequest(enable_contact=True)
    res = fcl.CollisionResult()
    fcl.collide(s1, s2, req, res)   

    return res
