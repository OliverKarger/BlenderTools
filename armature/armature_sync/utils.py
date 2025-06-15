def has_significant_scale_difference(obj_a, obj_b, threshold=0.01):
    """
    Determines whether two objects have a significant difference in their
    average scale values. This function also checks if the objects have
    uniform scale across all dimensions.

    Parameters:
    obj_a: Object
        The first object to compare. Must have a `scale` property that consists
        of three numerical values representing the scale in x, y, and z
        dimensions.
    obj_b: Object
        The second object to compare. Must have a `scale` property that consists
        of three numerical values representing the scale in x, y, and z
        dimensions.
    threshold: float, optional
        The threshold value used to determine if the average scales of the
        objects differ significantly. Defaults to 0.01.

    Returns:
    bool
        Returns True if the average scales of the objects differ by more than
        the threshold, or if either object is not uniform in scale. Otherwise,
        returns False.
    """

    def is_uniform(obj, epsilon=1e-4):
        sx, sy, sz = obj.scale
        return abs(sx - sy) < epsilon and abs(sx - sz) < epsilon and abs(sy - sz) < epsilon

    if not is_uniform(obj_a) or not is_uniform(obj_b):
        print("Rigs are not uniform in Scale!")
        return True

    avg_a = sum(obj_a.scale) / 3
    avg_b = sum(obj_b.scale) / 3

    result = abs(avg_a - avg_b) > threshold

    if result:
        print("Armatures differ significantly in Scale!")
    else:
        print("Armature Scale is withing expected Parameters")

    return result
