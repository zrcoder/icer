# Base GameObject Class

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from src.utils.vector2 import Vector2


class GameObject(ABC):
    """Base class for all game objects"""
    
    def __init__(self, x: int = 0, y: int = 0):
        self.grid_x = x
        self.grid_y = y
        self.position = Vector2(x, y)
        self.is_active = True
        self.properties: Dict[str, Any] = {}
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.grid_x}, {self.grid_y})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @abstractmethod
    def get_type(self) -> str:
        """Get object type identifier"""
        pass
    
    @abstractmethod
    def get_color(self) -> tuple:
        """Get object color for rendering"""
        pass
    
    def update(self, dt: float):
        """Update object logic (called each frame)"""
        pass
    
    def set_position(self, x: int, y: int):
        """Set object position"""
        self.grid_x = x
        self.grid_y = y
        self.position = Vector2(x, y)
    
    def get_position(self) -> Vector2:
        """Get object position"""
        return self.position
    
    def get_grid_position(self) -> tuple:
        """Get grid position as tuple"""
        return (self.grid_x, self.grid_y)
    
    def set_property(self, key: str, value: Any):
        """Set object property"""
        self.properties[key] = value
    
    def get_property(self, key: str, default: Any = None) -> Any:
        """Get object property"""
        return self.properties.get(key, default)
    
    def has_property(self, key: str) -> bool:
        """Check if object has property"""
        return key in self.properties
    
    def is_solid(self) -> bool:
        """Check if object blocks movement"""
        return self.get_property('solid', True)
    
    def is_pushable(self) -> bool:
        """Check if object can be pushed"""
        return self.get_property('pushable', False)
    
    def is_fragile(self) -> bool:
        """Check if object can be destroyed"""
        return self.get_property('fragile', False)
    
    def can_support_weight(self) -> bool:
        """Check if object can support weight above"""
        return self.get_property('supports_weight', True)
    
    def get_weight(self) -> int:
        """Get object weight (for physics calculations)"""
        return self.get_property('weight', 1)
    
    def on_collision(self, other: 'GameObject'):
        """Handle collision with another object"""
        pass
    
    def on_destroy(self):
        """Called when object is destroyed"""
        self.is_active = False
    
    def destroy(self) -> bool:
        """Destroy object"""
        if self.is_fragile():
            self.on_destroy()
            return True
        return False
    
    def activate(self):
        """Activate object"""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate object"""
        self.is_active = False
    
    def is_interactive(self) -> bool:
        """Check if object can be interacted with"""
        return self.get_property('interactive', False)
    
    def interact(self, actor: 'GameObject') -> bool:
        """Interact with object"""
        if self.is_interactive():
            return self.on_interact(actor)
        return False
    
    def on_interact(self, actor: 'GameObject') -> bool:
        """Called when object is interacted with"""
        return True
    
    def stop_sliding(self):
        """Stop sliding - default implementation does nothing"""
        self.set_property('sliding', False)
        self.set_property('slide_direction', None)
    
    def can_ignite(self) -> bool:
        """Check if object can be ignited - default implementation returns False"""
        return False
    
    def can_be_placed_on_hot_pot(self, hot_pot_y: int = 0) -> bool:
        """Check if object can be placed on hot pot - default implementation returns False"""
        return False
    
    def is_firm(self) -> bool:
        """Check if object is firm (attached to something) - default implementation returns False"""
        return self.get_property('is_firm', False)
    
    def get_push_distance(self) -> int:
        """Get how far object can be pushed - default implementation returns 1"""
        return self.get_property('push_distance', 1)
    
    def check_firm_status(self, game_world) -> bool:
        """Check and update firm status - default implementation returns False"""
        self.set_property('is_firm', False)
        return False