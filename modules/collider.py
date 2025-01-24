
def collides_point(point, rect):
    """Returns true if point is within rect"""
    return rect[0] < point[0] < rect[0] + rect[2] and rect[1] < point[1] < rect[1] + rect[3]

def collides_point_circle(point, position, radius):
    """Returns true if point is within circle with provided radius"""
    diff_x, diff_y = point[0] - position[0], point[1] - position[1]
    distance = (diff_x ** 2 + diff_y ** 2) ** 0.5
    return distance <= radius

def collides_point_polygon(point, polygon):
    """Returns true if point is within polygon"""
    polygon_min_x = polygon[0][0]
    polygon_max_x = polygon[0][0]
    polygon_min_y = polygon[0][1]
    polygon_max_y = polygon[0][1]
    for i in range(4):
        polygon_min_x = min(polygon_min_x, polygon[i][0])
        polygon_max_x = max(polygon_max_x, polygon[i][0])
        polygon_min_y = min(polygon_min_y, polygon[i][1])
        polygon_max_y = max(polygon_max_y, polygon[i][1])

    return polygon_min_x < point[0] < polygon_max_x and polygon_min_y < point[1] < polygon_max_y