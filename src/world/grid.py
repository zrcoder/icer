# Grid System for Game World

from typing import List, Optional, Tuple, Iterator, TYPE_CHECKING
from src.game.constants import GRID_WIDTH, GRID_HEIGHT

if TYPE_CHECKING:
    from src.entities.base import GameObject


class Grid:
    """2D Grid system for game world"""
    
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        self.width = width
        self.height = height
        # Initialize empty grid (None = empty cell)
        self.cells: List[List[Optional['GameObject']]] = [
            [None for _ in range(height)] for _ in range(width)
        ]
    
    def __str__(self) -> str:
        return f"Grid({self.width}x{self.height})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds"""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell(self, x: int, y: int) -> Optional['GameObject']:
        """Get object at specific cell"""
        if self.is_valid_position(x, y):
            return self.cells[x][y]
        return None
    
    def set_cell(self, x: int, y: int, obj: Optional['GameObject']) -> bool:
        """Set object at specific cell"""
        if self.is_valid_position(x, y):
            self.cells[x][y] = obj
            return True
        return False
    
    def is_empty(self, x: int, y: int) -> bool:
        """Check if cell is empty"""
        return self.get_cell(x, y) is None
    
    def is_blocked(self, x: int, y: int) -> bool:
        """Check if cell is blocked by any object"""
        return not self.is_empty(x, y)
    
    def move_object(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        """Move object from one cell to another"""
        if not self.is_valid_position(from_x, from_y) or not self.is_valid_position(to_x, to_y):
            return False
        
        obj = self.get_cell(from_x, from_y)
        if obj is None:
            return False
        
        if not self.is_empty(to_x, to_y):
            return False
        
        self.set_cell(to_x, to_y, obj)
        self.set_cell(from_x, from_y, None)
        return True
    
    def remove_object(self, x: int, y: int) -> Optional['GameObject']:
        """Remove object from cell and return it"""
        if not self.is_valid_position(x, y):
            return None
        
        obj = self.get_cell(x, y)
        self.set_cell(x, y, None)
        return obj
    
    def add_object(self, x: int, y: int, obj: 'GameObject') -> bool:
        """Add object to cell"""
        if self.is_empty(x, y):
            self.set_cell(x, y, obj)
            return True
        return False
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighbor positions (4-directional)"""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # up, down, right, left
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))
        
        return neighbors
    
    def get_adjacent_objects(self, x: int, y: int) -> List['GameObject']:
        """Get objects in adjacent cells"""
        adjacent_objects = []
        for nx, ny in self.get_neighbors(x, y):
            obj = self.get_cell(nx, ny)
            if obj is not None:
                adjacent_objects.append(obj)
        return adjacent_objects
    
    def find_objects_of_type(self, object_type: type) -> List[Tuple[int, int, 'GameObject']]:
        """Find all objects of specific type"""
        found_objects = []
        for x in range(self.width):
            for y in range(self.height):
                obj = self.get_cell(x, y)
                if obj is not None and isinstance(obj, object_type):
                    found_objects.append((x, y, obj))
        return found_objects
    
    def count_objects_of_type(self, object_type: type) -> int:
        """Count objects of specific type"""
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                obj = self.get_cell(x, y)
                if obj is not None and isinstance(obj, object_type):
                    count += 1
        return count
    
    def clear(self):
        """Clear all objects from grid"""
        self.cells = [[None for _ in range(self.height)] for _ in range(self.width)]
    
    def get_size(self) -> Tuple[int, int]:
        """Get grid dimensions"""
        return (self.width, self.height)
    
    def get_cells_around(self, x: int, y: int, radius: int = 1) -> List[Tuple[int, int]]:
        """Get all cells within radius around position"""
        cells_around = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if self.is_valid_position(nx, ny):
                    cells_around.append((nx, ny))
        return cells_around
    
    def is_line_clear(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """Check if line between two points is clear"""
        if x1 == x2:  # Vertical line
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if not self.is_empty(x1, y):
                    return False
        elif y1 == y2:  # Horizontal line
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if not self.is_empty(x, y1):
                    return False
        else:
            # Diagonal lines not supported for grid-based movement
            return False
        
        return True
    
    def get_path_between(self, x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """Get path between two points (simple straight line)"""
        path = []
        
        if not self.is_valid_position(x1, y1) or not self.is_valid_position(x2, y2):
            return path
        
        if x1 == x2:  # Vertical path
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                if self.is_valid_position(x1, y):
                    path.append((x1, y))
        elif y1 == y2:  # Horizontal path
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                if self.is_valid_position(x, y1):
                    path.append((x, y1))
        
        return path
    
    def clone(self) -> 'Grid':
        """Create a deep copy of the grid"""
        new_grid = Grid(self.width, self.height)
        for x in range(self.width):
            for y in range(self.height):
                new_grid.cells[x][y] = self.cells[x][y]
        return new_grid
    
    def __iter__(self) -> Iterator[Tuple[int, int, Optional['GameObject']]]:
        """Iterate over all cells"""
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y, self.get_cell(x, y))