def parse_shape(shape_lines: list[str]) -> list[tuple[int, int]]:
    """
    Parse a shape and return coordinates of '#' positions.
    """
    coords = []
    for r, line in enumerate(shape_lines):
        for c, char in enumerate(line):
            if char == '#':
                coords.append((r, c))
    return coords

def normalize_shape(coords: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Normalize shape to start at (0, 0).
    """
    if not coords:
        return []
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return [(r - min_r, c - min_c) for r, c in coords]

def get_all_orientations(coords: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """
    Get all unique rotations and flips of a shape.
    """
    orientations = set()
    
    for flip in [False, True]:
        current = coords[:]
        if flip:
            current = [(r, -c) for r, c in current]
        
        for _ in range(4):
            normalized = tuple(sorted(normalize_shape(current)))
            orientations.add(normalized)
            current = [(c, -r) for r, c in current]
    
    return [list(o) for o in orientations]

def can_place(grid: list[list[str]], shape: list[tuple[int, int]], row: int, col: int, rows: int, cols: int) -> bool:
    """
    Check if shape can be placed on grid at (row, col).
    """
    for dr, dc in shape:
        r, c = row + dr, col + dc
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '.':
            return False
    return True

def place_shape(grid: list[list[str]], shape: list[tuple[int, int]], row: int, col: int, mark: str) -> None:
    """
    Place shape on grid with given mark.
    """
    for dr, dc in shape:
        grid[row + dr][col + dc] = mark

def remove_shape(grid: list[list[str]], shape: list[tuple[int, int]], row: int, col: int) -> None:
    """
    Remove shape from grid.
    """
    for dr, dc in shape:
        grid[row + dr][col + dc] = '.'

def solve_region(rows: int, cols: int, present_counts: list[int], all_orientations: list[list[list[tuple[int, int]]]]) -> bool:
    """
    Try to fit all presents into the region using backtracking.
    """
    grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    presents_to_place = []
    for shape_idx, count in enumerate(present_counts):
        for _ in range(count):
            presents_to_place.append(shape_idx)
    
    last_placement = [None] * len(presents_to_place)
    
    def backtrack(idx):
        if idx == len(presents_to_place):
            return True
        
        shape_idx = presents_to_place[idx]
        
        min_pos = 0
        if idx > 0 and presents_to_place[idx - 1] == shape_idx and last_placement[idx - 1] is not None:
            min_pos = last_placement[idx - 1]
        
        for orientation in all_orientations[shape_idx]:
            for row in range(rows):
                for col in range(cols):
                    pos = row * cols + col
                    if pos < min_pos:
                        continue
                        
                    if can_place(grid, orientation, row, col, rows, cols):
                        place_shape(grid, orientation, row, col, str(idx))
                        last_placement[idx] = pos
                        
                        if backtrack(idx + 1):
                            return True
                        
                        last_placement[idx] = None
                        remove_shape(grid, orientation, row, col)
        
        return False
    
    return backtrack(0)

if __name__ == "__main__":
    shapes = []
    regions = []
    presents = []
    current_shape = []
    reading_shape = False
    
    with open("inputs/day12.txt") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")
            
            if not line:
                if reading_shape and current_shape:
                    shapes.append(current_shape)
                    current_shape = []
                    reading_shape = False
                continue
            
            if line.endswith(":") and line[:-1].isdigit():
                reading_shape = True
                current_shape = []
                continue
            
            if ":" in line and "x" in line:
                region_part, numbers_part = line.split(":", 1)
                regions.append(region_part.strip())
                presents.append(list(map(int, numbers_part.split())))
                reading_shape = False
                continue
            
            if reading_shape:
                current_shape.append(line)
        
        if reading_shape and current_shape:
            shapes.append(current_shape)

    shape_coords = [parse_shape(shape) for shape in shapes]
    all_orientations = [get_all_orientations(coords) for coords in shape_coords]
    
    valid_regions = 0
    for i, (region, present_counts) in enumerate(zip(regions, presents)):
        width, height = map(int, region.split('x'))
        
        region_area = width * height
        total_present_area = sum(len(shape_coords[j]) * count for j, count in enumerate(present_counts))
        
        if total_present_area <= region_area:   # Only try if area fits
            if solve_region(height, width, present_counts, all_orientations):
                valid_regions += 1
    
    print(f"{valid_regions} regions can fit all of their presents.")