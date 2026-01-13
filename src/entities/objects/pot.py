# Pot Class - Ice Pot and Hot Pot

from src.entities.base import GameObject
from src.game.constants import COLOR_ICE_POT, COLOR_HOT_POT


class Pot(GameObject):
    """Pot object that can be in ice or hot state"""
    
    def __init__(self, x: int = 0, y: int = 0, is_hot: bool = False):
        super().__init__(x, y)
        
        # Pot properties
        self.set_property('solid', True)
        self.set_property('pushable', False)
        self.set_property('fragile', False)  # Cannot be destroyed
        self.set_property('affected_by_gravity', False)
        self.set_property('supports_weight', True)
        self.set_property('interactive', False)
        self.set_property('height', 1)
        self.set_property('weight', 2)
        
        # Pot-specific properties
        self.set_property('is_hot', is_hot)
        self.set_property('can_ignite', True)
        self.set_property('can_cool', False)  # Once hot, never cools
        self.set_property('player_standable', not is_hot)  # Player can't stand on hot pot
        
        # Initialize state
        if is_hot:
            self._make_hot()
        else:
            self._make_ice()
    
    def get_type(self) -> str:
        return "hot_pot" if self.is_hot() else "ice_pot"
    
    def get_color(self) -> tuple:
        return COLOR_HOT_POT if self.is_hot() else COLOR_ICE_POT
    
    def is_hot(self) -> bool:
        """Check if pot is hot"""
        return self.get_property('is_hot', False)
    
    def is_ice(self) -> bool:
        """Check if pot is ice"""
        return not self.is_hot()
    
    def can_player_stand_on(self) -> bool:
        """Check if player can stand on this pot"""
        return self.get_property('player_standable', True)
    
    def can_ignite(self) -> bool:
        """Check if pot can be ignited"""
        return self.get_property('can_ignite', True)
    
    def ignite(self):
        """Ignite ice pot to hot pot"""
        if not self.is_hot() and self.can_ignite():
            self._make_hot()
    
    def _make_hot(self):
        """Convert to hot pot"""
        self.set_property('is_hot', True)
        self.set_property('can_ignite', False)
        self.set_property('can_cool', False)
        self.set_property('player_standable', False)
    
    def _make_ice(self):
        """Convert to ice pot"""
        self.set_property('is_hot', False)
        self.set_property('can_ignite', True)
        self.set_property('player_standable', True)
    
    def update(self, dt: float):
        """Update pot state"""
        super().update(dt)
        
        # Check for ignition
        if self.is_ice() and self.can_ignite():
            self._check_for_ignition()
    
    def _check_for_ignition(self):
        """Check if pot should be ignited by nearby flame"""
        # TODO: Implement ignition check when we have access to game_world
        # This should check for adjacent flames
        pass
    
    def check_for_ignition(self, game_world):
        """Check if pot should be ignited by nearby flame"""
        if not self.is_ice() or not self.can_ignite():
            return
        
        x, y = self.grid_x, self.grid_y
        
        # Check adjacent positions for flames
        for nx, ny in game_world.grid.get_neighbors(x, y):
            obj = game_world.get_object_at(nx, ny)
            if obj and obj.get_type() == "flame":
                self.ignite()
                return
    
    def on_collision(self, other: GameObject):
        """Handle collision with another object"""
        if other.get_type() == "flame":
            # Flame ignites ice pot
            if self.is_ice() and self.can_ignite():
                self.ignite()
    
    def can_melt_ice_above(self) -> bool:
        """Check if pot can melt ice directly above"""
        return self.is_hot()
    
    def can_support_ice_above(self) -> bool:
        """Check if pot can support ice directly above"""
        # Hot pot will melt ice, ice pot won't
        return not self.is_hot()
    
    def get_heat_level(self) -> int:
        """Get heat level (0 for ice, 1 for hot)"""
        return 1 if self.is_hot() else 0