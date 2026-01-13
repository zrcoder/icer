# Ice Block Class

from typing import Optional
from src.entities.base import GameObject
from src.game.constants import COLOR_ICE_BLOCK


class IceBlock(GameObject):
    """Ice block that can be created, pushed, and destroyed"""
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        
        # Ice block properties
        self.set_property('solid', True)
        self.set_property('pushable', True)
        self.set_property('fragile', True)  # Can be destroyed by fire
        self.set_property('affected_by_gravity', True)
        self.set_property('supports_weight', True)
        self.set_property('interactive', False)
        self.set_property('height', 1)
        self.set_property('weight', 1)
        
        # Ice-specific properties
        self.set_property('is_firm', False)  # Whether ice is "firm" (attached)
        self.set_property('sliding', False)  # Currently sliding
        self.set_property('slide_direction', None)  # Direction of sliding
        self.set_property('can_melt_by_hot_pot', True)
        
        # Physics properties
        self.set_property('friction', 0.1)  # Low friction = slides easily
        self.set_property('slide_speed', 2.0)  # Grids per second
    
    def get_type(self) -> str:
        return "ice_block"
    
    def get_color(self) -> tuple:
        return COLOR_ICE_BLOCK
    
    def update(self, dt: float):
        """Update ice block physics"""
        super().update(dt)
        
        # Update firm status
        self._update_firm_status()
        
        # Handle sliding physics
        if self.get_property('sliding', False):
            self._update_sliding(dt)
    
    def _update_firm_status(self):
        """Update whether ice block is firm (attached)"""
        # TODO: Implement firm status checking when we have access to game_world
        # For now, ice is not firm by default
        pass
    
    def _update_sliding(self, dt: float):
        """Update sliding physics"""
        # TODO: Implement sliding physics when we have access to game_world
        # This will need the physics system to be implemented
        pass
    
    def check_firm_status(self, game_world) -> bool:
        """Check if ice block is firm (attached to something)"""
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
        """Check if ice block is firm"""
        return self.get_property('is_firm', False)
    
    def can_be_pushed(self) -> bool:
        """Check if ice block can be pushed"""
        return self.is_pushable() and not self.is_firm()
    
    def can_slide(self) -> bool:
        """Check if ice block can slide"""
        return not self.is_firm()
    
    def start_sliding(self, direction: str):
        """Start sliding in direction"""
        if self.can_slide():
            self.set_property('sliding', True)
            self.set_property('slide_direction', direction)
    
    def stop_sliding(self):
        """Stop sliding"""
        self.set_property('sliding', False)
        self.set_property('slide_direction', None)
    
    def on_collision(self, other: GameObject):
        """Handle collision with another object"""
        if other.get_type() == "flame":
            # Ice extinguishes flame and is destroyed
            self.destroy()
        elif other.get_type() == "hot_pot":
            # Ice melts when touching hot pot
            if self.get_property('can_melt_by_hot_pot', True):
                self.destroy()
    
    def can_be_placed_on_hot_pot(self, hot_pot_y: int) -> bool:
        """Check if ice can be placed on hot pot"""
        ice_y = self.grid_y
        
        # Ice cannot be placed directly on burning hot pot
        # But can be placed higher up
        return ice_y > hot_pot_y