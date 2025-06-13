def has_significant_scale_difference(obj_a, obj_b, threshold=0.01):
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
