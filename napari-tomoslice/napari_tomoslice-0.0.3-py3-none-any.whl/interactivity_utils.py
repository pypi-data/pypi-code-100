from typing import Optional

import napari
import napari.layers
import numpy as np

from napari.utils.geometry import project_point_onto_plane, \
    clamp_point_to_bounding_box


def point_in_bounding_box(point: np.ndarray, bounding_box: np.ndarray) -> bool:
    """Determine whether an nD point is inside an nD bounding box.
    Parameters
    ----------
    point : np.ndarray
        (n,) array containing nD point coordinates to check.
    bounding_box : np.ndarray
        (2, n) array containing the min and max of the nD bounding box.
        As returned by `Layer._extent_data`.
    """
    if np.all(point > bounding_box[0]) and np.all(point < bounding_box[1]):
        return True
    return False


def drag_data_to_projected_distance(
        start_position, end_position, view_direction, vector
):
    """Calculate the projected distance between two mouse events.
    Project the drag vector between two mouse events onto a 3D vector
    specified in data coordinates.
    The general strategy is to
    1) find mouse drag start and end positions, project them onto a
       pseudo-canvas (a plane aligned with the canvas) in data coordinates.
    2) project the mouse drag vector onto the (normalised) vector in data
       coordinates
    Parameters
    ----------
    start_position : np.ndarray
        Starting point of the drag vector in data coordinates
    end_position : np.ndarray
        End point of the drag vector in data coordinates
    view_direction : np.ndarray
        Vector defining the plane normal of the plane onto which the drag
        vector is projected.
    vector : np.ndarray
        (3,) unit vector or (n, 3) array thereof on which to project the drag
        vector from start_event to end_event. This argument is defined in data
        coordinates.
    Returns
    -------
    projected_distance : (1, ) or (n, ) np.ndarray of float
    """
    # enforce at least 2d input
    vector = np.atleast_2d(vector)

    # Store the start and end positions in world coordinates
    start_position = np.array(start_position)
    end_position = np.array(end_position)

    # Project the start and end positions onto a pseudo-canvas, a plane
    # parallel to the rendered canvas in data coordinates.
    start_position_canvas = start_position
    end_position_canvas = project_point_onto_plane(
        end_position, start_position_canvas, view_direction
    )
    # Calculate the drag vector on the pseudo-canvas.
    drag_vector_canvas = np.squeeze(
        end_position_canvas - start_position_canvas
    )

    # Project the drag vector onto the specified vector(s), return the distance
    return np.einsum('j, ij -> i', drag_vector_canvas, vector).squeeze()


def shift_plane_along_normal(viewer, event, layer: Optional[napari.layers.Image] = None):
    """Shift a rendered plane along its normal vector.
    This function will shift a plane along its normal vector when the plane is
    clicked and dragged."""
    # Early exit if plane rendering not enabled or layer isn't visible
    if not (layer.experimental_slicing_plane.enabled and layer.visible):
        return

    # Calculate intersection of click with data bounding box in data coordinates
    near_point, far_point = layer.get_ray_intersections(
        event.position,
        event.view_direction,
        event.dims_displayed,
    )

    # exit if click is outside data bounding box
    if near_point is None and far_point is None:
        return

    # Calculate intersection of click with plane through data in data coordinates
    intersection = layer.experimental_slicing_plane.intersect_with_line(
        line_position=near_point, line_direction=event.view_direction
    )

    # Check if click was on plane by checking if intersection occurs within
    # data bounding box. If not, exit early.
    if not point_in_bounding_box(intersection, layer.extent.data):
        return

    # Store original plane position and disable interactivity during plane drag
    original_plane_position = np.copy(layer.experimental_slicing_plane.position)
    layer.interactive = False

    # Store mouse position at start of drag
    start_position = np.copy(event.position)
    yield

    while event.type == 'mouse_move':
        current_position = event.position
        current_view_direction = event.view_direction
        current_plane_normal = layer.experimental_slicing_plane.normal

        # Project mouse drag onto plane normal
        drag_distance = drag_data_to_projected_distance(
            start_position=start_position,
            end_position=current_position,
            view_direction=current_view_direction,
            vector=current_plane_normal,
        )

        # Calculate updated plane position
        updated_position = original_plane_position + (
                drag_distance * np.array(layer.experimental_slicing_plane.normal)
        )

        clamped_plane_position = clamp_point_to_bounding_box(
            updated_position, layer._display_bounding_box(event.dims_displayed)
        )

        layer.experimental_slicing_plane.position = clamped_plane_position
        yield

    # Re-enable layer interactivity after the drag
    layer.interactive = True


def set_plane_normal_axis(viewer: napari.viewer.Viewer, layer: napari.layers.Image, axis='z'):
    viewer = napari.viewer.current_viewer()
    current_position = viewer.cursor.position
    current_view_direction = viewer.cursor._view_direction
    current_dims_displayed = viewer.dims.displayed

    axis_to_normal = {
        'z': (1, 0, 0),
        'y': (0, 1, 0),
        'x': (0, 0, 1),
    }

    start_point, end_point = layer.get_ray_intersections(
        position=current_position,
        view_direction=current_view_direction,
        dims_displayed=list(current_dims_displayed),
    )
    if start_point is None and end_point is None:
        new_plane_position = np.array(layer.data.shape) // 2
    else:
        new_plane_position = \
            layer.experimental_slicing_plane.intersect_with_line(
            line_position=start_point,
            line_direction=current_view_direction,
        )
    if point_in_layer_bounding_box(new_plane_position, layer) is False:
        new_plane_position = np.array(layer.data.shape) // 2

    layer.experimental_slicing_plane.position = new_plane_position
    layer.experimental_slicing_plane.normal = axis_to_normal[axis]


def point_in_layer_bounding_box(point, layer):
    bbox = layer._display_bounding_box(layer._dims_displayed).T
    if np.any(point < bbox[0]) or np.any(point > bbox[1]):
        return False
    else:
        return True
