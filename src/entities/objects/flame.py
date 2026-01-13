# Flame Class

from src.entities.base import GameObject
from src.game.constants import COLOR_FLAME


class Flame(GameObject):
    """Flame object that needs to be extinguished"""
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        
        # Flame properties
        self.set_property('solid', True)
        self.set_property('pushable', False)
        self.set_property('fragile', True)  # Can be extinguished by ice
        self.set_property('affected_by_gravity', False)
        self.set_property('supports_weight', True)
        self.set_property('interactive', False)
        self.set_property('height', 1)
        self.set_property('weight', 0)
        
        # Flame-specific properties
        self.set_property('burning', True)
        self.set_property('can_extinguish_ice_above', False)  # Ice above doesn't melt
    
    def get_type(self) -> str:
        return "flame"
    
    def get_color(self) -> tuple:
        return COLOR_FLAME
    
    def update(self, dt: float):
        """Update flame animation"""
        super().update(dt)
        # TODO: Add flame animation
    
    def on_collision(self, other: GameObject):
        """Handle collision with other objects"""
        if other.get_type() == "ice_block":
            # Ice extinguishes flame
            self.destroy()
    
    def is_burning(self) -> bool:
        """Check if flame is still burning"""
        return self.get_property('burning', True)
    
    def extinguish(self):
        """Extinguish the flame"""
        self.set_property('burning', False)
        self.destroy()
    
    def can_melt_ice_above(self) -> bool:
        """Check if flame can melt ice directly above"""
        return self.get_property('can_extinguish_ice_above', False)