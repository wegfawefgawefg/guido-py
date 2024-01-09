def transform_mouse_to_normalized_subsurface_coords(
    normalized_mouse_pos, surface_res, subsurface_pos, subsurface_res
):
    # Calculate the normalized position and size of the subsurface
    subsurface_norm_pos = subsurface_pos / surface_res
    subsurface_norm_size = subsurface_res / surface_res

    # Transform the mouse coordinates to the subsurface
    transformed = (normalized_mouse_pos - subsurface_norm_pos) / subsurface_norm_size

    return transformed
