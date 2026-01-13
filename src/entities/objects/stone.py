# Stone Class

from src.entities.base import GameObject
from src.game.constants import COLOR_STONE


class Stone(GameObject):
    """Stone object that is rough and heavy"""
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        
        # Stone properties
        self.set_property('solid', True)
        self.set_property('pushable', True)
        self.set_property('fragile', False)  # Cannot be destroyed
        self.set_property('affected_by_gravity', True)
        self.set_property('supports_weight', True)
        self.set_property('interactive', False)
        self.set_property('height', 1)
        self.set_property('weight', 3)
        
        # Stone-specific properties
        self.set_property('is_firm', False)  # Stones can be pushed
        self.set_property('surface_type', 'rough')  # Rough surface
        self.set_property('push_distance', 1)  # Only moves 1 grid
        self.set_property('heat_resistant', True)  # Can be placed on hot pot
    
    def get_type(self) -> str:
        return "stone"
    
    def get_color(self) -> tuple:
        return COLOR_STONE
    
    def update(self, dt: float):
        """Update stone physics"""
        super().update(dt)
        
        # Update firm status
        self._update_firm_status()
    
    def _update_firm_status(self):
        """Update whether stone is firm (attached)"""
        # TODO: Implement firm status checking when we have access to game_world
        # For now, stone is not firm by default (can be pushed)
        pass
    
    def check_firm_status(self, game_world) -> bool:
        """Check if stone is firm (attached to something)"""
        x, y = self.grid_x, self.grid_y
        
        # Check if attached to sides
        left_obj = game_world.get_object_at(x - 1, y)
        right_obj = game_world.get_object_at(x + 1, y)
        
        if (left_obj and left_obj.is_solid()) or (right_obj and right_obj.is_solid()):
            self.set_property('is_firm', True)
            return True
        
        # Check if has support below
        if y > 0:
            below_obj = game_world.get_object_at(x, y - 1)
            if below_obj and below_obj.is_solid():
                self.set_property('is_firm', True)
                return True
        
        # Not attached to anything solid
        self.set_property('is_firm', False)
        return False
    
    def is_firm(self) -> bool:
        """Check if stone is firm"""
        return self.get_property('is_firm', False)
    
    def can_be_pushed(self) -> bool:
        """Check if stone can be pushed"""
        return self.is_pushable() and not self.is_firm()
    
    def get_push_distance(self) -> int:
        """Get how far stone can be pushed"""
        return self.get_property('push_distance', 1)
    
    def get_surface_type(self) -> str:
        """Get surface type for physics calculations"""
        return self.get_property('surface_type', 'rough')
    
    def is_heat_resistant(self) -> bool:
        """Check if stone is heat resistant"""
        return self.get_property('heat_resistant', True)
    
    def can_be_placed_on_hot_pot(self) -> bool:
        """Check if stone can be placed on hot pot"""
        return self.is_heat_resistant()
    
    def on_collision(self, other: GameObject):
        """Handle collision with another object"""
        if other.get_type() == "flame":
            # Stone is heat resistant, not affected by flame
            pass
        elif other.get_type() == "hot_pot":
            # Stone can survive on hot pot
            pass
    
    def can_slide(self) -> bool:
        """Check if stone can slide (always false for rough surface)"""
        return False
    
    def can_stop_sliding_object(self) -> bool:
        """Check if stone can stop sliding objects (true for rough surface)"""
        return self.get_surface_type() == 'rough'