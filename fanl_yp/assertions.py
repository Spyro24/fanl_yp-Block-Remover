def isVector3(vec):
    "Check if a vector is a vector3int or vector3float"
    try:
        if not isinstance(vec[0], (int, float)):
            return False
        elif not isinstance(vec[1], (int, float)):
            return False
        elif not isinstance(vec[2], (int, float)):
            return False
        else:
            return True
    except IndexError:
        return False

def assertVector(vec):
    pass
