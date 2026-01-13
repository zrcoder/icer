# Wall Class

from src.entities.base import GameObject
from src.game.constants import COLOR_WALL


class Wall(GameObject):
    """Wall object that blocks movement"""
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        
        # Wall properties
        self.set_property('solid', True)
        self.set_property('pushable', False)
        self.set_property('fragile', False)
        self.set_property('affected_by_gravity', False)
        self.set_property('supports_weight', True)
        self.set_property('interactive', False)
        self.set_property('height', 1)  # Standard wall height
        self.set_property('weight', 999)  # Very heavy
    
    def get_type(self) -> str:
        return "wall"
    
    def get_color(self) -> tuple:
        return COLOR_WALL
    
    def can_be_jumped_over(self) -> bool:
        """Check if player can jump over this wall"""
        return self.get_property('height', 1) <= 1