# Game World Class

from typing import Optional, List, Tuple, Dict, Any
from src.world.grid import Grid
from src.entities.base import GameObject
from src.game.constants import GRID_WIDTH, GRID_HEIGHT


class GameWorld:
    """Main game world that manages grid and all game objects"""
    
    def __init__(self, width: int = GRID_WIDTH, height: int = GRID_HEIGHT):
        self.grid = Grid(width, height)
        self.width = width
        self.height = height
        self.objects: Dict[str, GameObject] = {}  # ID to object mapping
        self.next_object_id = 1
        
        # World properties
        self.gravity_enabled = True
        self.physics_enabled = True
    
    def __str__(self) -> str:
        return f"GameWorld({self.width}x{self.height}, {len(self.objects)} objects)"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def generate_object_id(self) -> str:
        """Generate unique object ID"""
        obj_id = f"obj_{self.next_object_id}"
        self.next_object_id += 1
        return obj_id
    
    def add_object(self, obj: GameObject, x: int, y: int) -> bool:
        """Add object to world at specified position"""
        if not self.grid.is_valid_position(x, y):
            return False
        
        if not self.grid.is_empty(x, y):
            return False
        
        obj_id = self.generate_object_id()
        self.objects[obj_id] = obj
        obj.set_position(x, y)
        self.grid.set_cell(x, y, obj)
        return True
    
    def remove_object(self, obj: GameObject) -> bool:
        """Remove object from world"""
        x, y = obj.get_grid_position()
        if self.grid.get_cell(x, y) == obj:
            self.grid.set_cell(x, y, None)
            
            # Find and remove from objects dict
            to_remove = None
            for obj_id, world_obj in self.objects.items():
                if world_obj == obj:
                    to_remove = obj_id
                    break
            
            if to_remove:
                del self.objects[to_remove]
                return True
        
        return False
    
    def remove_object_at(self, x: int, y: int) -> Optional[GameObject]:
        """Remove object at position and return it"""
        obj = self.grid.get_cell(x, y)
        if obj is not None:
            self.remove_object(obj)
            return obj
        return None
    
    def move_object(self, obj: GameObject, new_x: int, new_y: int) -> bool:
        """Move object to new position"""
        old_x, old_y = obj.get_grid_position()
        
        if not self.grid.is_valid_position(new_x, new_y):
            return False
        
        if not self.grid.is_empty(new_x, new_y):
            return False
        
        # Move in grid
        self.grid.set_cell(old_x, old_y, None)
        self.grid.set_cell(new_x, new_y, obj)
        obj.set_position(new_x, new_y)
        return True
    
    def move_object_to(self, obj: GameObject, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        """Move object from specific position to new position"""
        if self.grid.get_cell(from_x, from_y) != obj:
            return False
        
        if not self.grid.is_valid_position(to_x, to_y):
            return False
        
        if not self.grid.is_empty(to_x, to_y):
            return False
        
        # Move in grid
        self.grid.set_cell(from_x, from_y, None)
        self.grid.set_cell(to_x, to_y, obj)
        obj.set_position(to_x, to_y)
        return True
    
    def get_object_at(self, x: int, y: int) -> Optional[GameObject]:
        """Get object at specific position"""
        return self.grid.get_cell(x, y)
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is valid in world"""
        return self.grid.is_valid_position(x, y)
    
    def is_empty(self, x: int, y: int) -> bool:
        """Check if position is empty"""
        return self.grid.is_empty(x, y)
    
    def is_blocked(self, x: int, y: int) -> bool:
        """Check if position is blocked"""
        return self.grid.is_blocked(x, y)
    
    def find_objects_of_type(self, object_type: type) -> List[Tuple[int, int, GameObject]]:
        """Find all objects of specific type"""
        return self.grid.find_objects_of_type(object_type)
    
    def count_objects_of_type(self, object_type: type) -> int:
        """Count objects of specific type"""
        return self.grid.count_objects_of_type(object_type)
    
    def get_objects_in_area(self, x1: int, y1: int, x2: int, y2: int) -> List[GameObject]:
        """Get all objects in rectangular area"""
        objects = []
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                obj = self.get_object_at(x, y)
                if obj is not None:
                    objects.append(obj)
        
        return objects
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int, GameObject]]:
        """Get neighboring objects"""
        neighbors = []
        for nx, ny in self.grid.get_neighbors(x, y):
            obj = self.get_object_at(nx, ny)
            if obj is not None:
                neighbors.append((nx, ny, obj))
        return neighbors
    
    def update(self, dt: float):
        """Update all objects in world"""
        if not self.physics_enabled:
            return
        
        # Update all objects
        for obj in list(self.objects.values()):
            if obj.is_active:
                obj.update(dt)
        
        # Apply physics if enabled
        if self.gravity_enabled:
            self.apply_gravity()
    
    def apply_gravity(self):
        """Apply gravity to objects that can fall"""
        # Process from bottom to top to avoid cascading issues
        for y in range(self.height - 2, -1, -1):  # Skip bottom row
            for x in range(self.width):
                obj = self.get_object_at(x, y)
                if obj is not None and self._should_fall(obj, x, y):
                    self._make_object_fall(obj, x, y)
    
    def _should_fall(self, obj: GameObject, x: int, y: int) -> bool:
        """Check if object should fall"""
        if not obj.get_property('affected_by_gravity', True):
            return False
        
        # Check if there's solid support below
        if y > 0:
            below_obj = self.get_object_at(x, y - 1)
            if below_obj is not None and below_obj.can_support_weight():
                return False
        
        return True
    
    def _make_object_fall(self, obj: GameObject, x: int, y: int):
        """Make object fall down"""
        fall_distance = 0
        
        # Calculate how far it can fall
        for check_y in range(y - 1, -1, -1):
            if self.is_empty(x, check_y):
                fall_distance += 1
            else:
                below_obj = self.get_object_at(x, check_y)
                if below_obj is not None and below_obj.can_support_weight():
                    break
                else:
                    break
        
        # Apply fall
        if fall_distance > 0:
            new_y = y - fall_distance
            self.move_object(obj, x, new_y)
            
            # Trigger fall event
            obj.set_property('falling', True)
            obj.set_property('fall_distance', fall_distance)
    
    def clear(self):
        """Clear all objects from world"""
        self.grid.clear()
        self.objects.clear()
        self.next_object_id = 1
    
    def get_state(self) -> Dict[str, Any]:
        """Get world state for saving/loading"""
        state = {
            'width': self.width,
            'height': self.height,
            'objects': []
        }
        
        for obj_id, obj in self.objects.items():
            x, y = obj.get_grid_position()
            obj_data = {
                'id': obj_id,
                'type': obj.get_type(),
                'position': (x, y),
                'properties': obj.properties
            }
            state['objects'].append(obj_data)
        
        return state
    
    def load_state(self, state: Dict[str, Any]):
        """Load world state from data"""
        self.clear()
        
        for obj_data in state.get('objects', []):
            # TODO: Create objects based on type
            pass
    
    def get_size(self) -> Tuple[int, int]:
        """Get world dimensions"""
        return (self.width, self.height)
    
    def __iter__(self):
        """Iterate over all objects in world"""
        return iter(self.objects.values())
    
    def get_objects_by_position(self) -> Dict[Tuple[int, int], GameObject]:
        """Get dictionary mapping positions to objects"""
        position_map = {}
        for x, y, obj in self.grid:
            if obj is not None:
                position_map[(x, y)] = obj
        return position_map