

def collides_point(point, rect):
    """Returns true if point is within rect"""
    return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

def collides_point_circle(point, position, radius):
    """Returns true if point is within circle with provided radius"""
    diff_x, diff_y = point[0] - position[0], point[1] - position[1]
    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5
    return distance <= radius