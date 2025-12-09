def segments_intersect(segment1: tuple[tuple[int, int], tuple[int, int]], segment2: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    """
    Check if two line segments intersect    
    Uses the counterclockwise (CCW) test to determine if segments cross
    1. If the segments straddle each other, they intersect.
    2. If they are collinear, check for overlap.
    3. Otherwise, they do not intersect.
    4. Returns True if they intersect, False otherwise.
    """
    (x1, y1), (x2, y2) = segment1
    (x3, y3), (x4, y4) = segment2
    
    # Check general case
    if _ccw((x1, y1), (x3, y3), (x4, y4)) != _ccw((x2, y2), (x3, y3), (x4, y4)) and \
       _ccw((x1, y1), (x2, y2), (x3, y3)) != _ccw((x1, y1), (x2, y2), (x4, y4)):
        return True

    # Check collinear case
    if (x2-x1)*(y3-y1) == (y2-y1)*(x3-x1) and _colinear((x1, y1), (x3, y3), (x2, y2)):
        return True
    if (x2-x1)*(y4-y1) == (y2-y1)*(x4-x1) and _colinear((x1, y1), (x4, y4), (x2, y2)):
        return True
    if (x4-x3)*(y1-y3) == (y4-y3)*(x1-x3) and _colinear((x3, y3), (x1, y1), (x4, y4)):
        return True
    if (x4-x3)*(y2-y3) == (y4-y3)*(x2-x3) and _colinear((x3, y3), (x2, y2), (x4, y4)):
        return True
    
    return False


def _ccw(a, b, c):
    """
    Check if points a, b, c are listed in a counterclockwise order
    """
    return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])


def _colinear(p, q, r):
    """
    Given three collinear points p, q, r, check if point q lies on segment pr
    """
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and \
        min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False


if __name__ == "__main__":
    import numpy as np

    points = []
    with open("inputs/day9.txt") as f:
        for line in f:
            points.append(tuple(map(int, line.strip().split(','))))
    
    positions = np.array(points)
    diffs = np.abs(positions[:, None] - positions[None, :]) + 1
    areas = np.prod(diffs, axis=2)
    
    indices = np.triu_indices(len(points), k=1)
    
    all_rectangles = [
        (areas[i, j], points[i], points[j])
        for i, j in zip(indices[0], indices[1])
    ]

    all_rectangles.sort(reverse=True, key=lambda x: x[0])

    # Part 1: Find largest rectangle
    print(f"Largest area: {all_rectangles[0][0]}")
    
    # Part 2: Find largest rectangle that uses only red and green tiles 
    boundary = []
    for i in range(len(points)):
        boundary.append((points[i], points[(i + 1) % len(points)]))
    
    best_interior_area = 0
    for area, p1, p2 in all_rectangles:
        x1, y1 = p1
        x2, y2 = p2
        
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        
        corners = [
            (x1 + dx, y1 + dy),
            (x2 - dx, y1 + dy),
            (x2 - dx, y2 - dy),
            (x1 + dx, y2 - dy)
        ]
        
        edges = []
        for i in range(4):
            edges.append((corners[i], corners[(i + 1) % 4]))
        
        intersects_boundary = False
        
        for rect_edge in edges:
            for bound_edge in boundary:
                if segments_intersect(rect_edge, bound_edge):
                    intersects_boundary = True
                    break
            if intersects_boundary:
                break
        
        if not intersects_boundary:
            best_interior_area = area
            break
    
    print(f"Largest area using only red and green tiles: {best_interior_area}")
