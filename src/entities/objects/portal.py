# Portal Class - Transportation pipes

from src.entities.base import GameObject
from src.game.constants import COLOR_PORTAL
from typing import Optional, List, Tuple


class Portal(GameObject):
    """Portal object for player transportation"""
    
    def __init__(self, x: int = 0, y: int = 0, portal_id: str = "default"):
        super().__init__(x, y)
        
        # Portal properties
        self.set_property('solid', False)  # Player can walk into portals
        self.set_property('pushable', False)
        self.set_property('fragile', False)
        self.set_property('affected_by_gravity', False)
        self.set_property('supports_weight', False)  # Can't stand on portals
        self.set_property('interactive', True)
        self.set_property('height', 1)
        self.set_property('weight', 0)
        
        # Portal-specific properties
        self.set_property('portal_id', portal_id)
        self.set_property('is_entrance', True)
        self.set_property('is_exit', True)
        self.set_property('bidirectional', True)
        self.set_property('active', True)
        self.set_property('linked_portal', None)
        
        # Portal entry requirements
        self.set_property('requires_player_below', True)  # Player must be lower
        self.set_property('height_difference', 1)  # Max height difference
    
    def get_type(self) -> str:
        return "portal"
    
    def get_color(self) -> tuple:
        return COLOR_PORTAL
    
    def get_portal_id(self) -> str:
        """Get portal identifier"""
        return self.get_property('portal_id', 'default')
    
    def is_active(self) -> bool:
        """Check if portal is active"""
        return self.get_property('active', True)
    
    def can_player_enter(self, player_pos_x: int, player_pos_y: int) -> bool:
        """Check if player can enter this portal"""
        if not self.is_active():
            return False
        
        x, y = self.grid_x, self.grid_y
        
        # Check height requirement
        if self.get_property('requires_player_below', True):
            if player_pos_y >= y:
                return False
            height_diff = y - player_pos_y
            max_diff = self.get_property('height_difference', 1)
            if height_diff > max_diff:
                return False
        
        return True
    
    def link_to_portal(self, other_portal: 'Portal'):
        """Link this portal to another portal"""
        if other_portal and other_portal != self:
            self.set_property('linked_portal', other_portal)
            other_portal.set_property('linked_portal', self)
    
    def get_linked_portal(self) -> Optional['Portal']:
        """Get the linked portal"""
        return self.get_property('linked_portal')
    
    def transport_player(self, player, game_world) -> bool:
        """Transport player to linked portal"""
        if not self.can_player_enter(player.grid_x, player.grid_y):
            return False
        
        linked_portal = self.get_linked_portal()
        if not linked_portal:
            return False
        
        # Check if linked portal can accept player
        if not linked_portal.can_player_accept_player(player, game_world):
            return False
        
        # Transport player
        new_x, new_y = self._get_transport_destination(player, linked_portal)
        
        # Remove player from current position and add to new position
        game_world.remove_object(player)
        game_world.add_object(player, new_x, new_y)
        player.set_position(new_x, new_y)
        
        return True
    
    def can_player_accept_player(self, player, game_world) -> bool:
        """Check if this portal can accept a transported player"""
        new_x, new_y = self._get_transport_destination(player, self)
        
        # Check if destination is valid
        if not game_world.is_valid_position(new_x, new_y):
            return False
        
        # Check if destination is empty
        if not game_world.is_empty(new_x, new_y):
            return False
        
        # Check if player can stand at destination (need support)
        if new_y > 0:
            below_obj = game_world.get_object_at(new_x, new_y - 1)
            if below_obj is None:
                return False
        
        return True
    
    def _get_transport_destination(self, player, target_portal: 'Portal') -> Tuple[int, int]:
        """Get destination coordinates for transport"""
        # Place player at the portal position
        return (target_portal.grid_x, target_portal.grid_y)
    
    def unlink(self):
        """Unlink from connected portal"""
        linked_portal = self.get_linked_portal()
        if linked_portal:
            linked_portal.set_property('linked_portal', None)
            self.set_property('linked_portal', None)
    
    def update(self, dt: float):
        """Update portal state"""
        super().update(dt)
        
        # Portal could have visual effects or animations here
        pass
    
    def on_interact(self, actor: GameObject) -> bool:
        """Handle player interaction with portal"""
        if actor.get_type() == "player":
            # Portal interaction happens through movement, not direct interaction
            return True
        return False
    
    def get_connection_info(self) -> dict:
        """Get information about portal connection"""
        linked = self.get_linked_portal()
        
        info = {
            'portal_id': self.get_portal_id(),
            'position': (self.grid_x, self.grid_y),
            'active': self.is_active(),
            'linked_to': None
        }
        
        if linked:
            info['linked_to'] = {
                'portal_id': linked.get_portal_id(),
                'position': (linked.grid_x, linked.grid_y)
            }
        
        return info
    
    @staticmethod
    def create_portal_pair(x1: int, y1: int, x2: int, y2: int, portal_id: str) -> Tuple['Portal', 'Portal']:
        """Create a pair of linked portals"""
        portal1 = Portal(x1, y1, portal_id)
        portal2 = Portal(x2, y2, portal_id)
        
        portal1.link_to_portal(portal2)
        
        return portal1, portal2
    
    @staticmethod
    def find_portal_by_id(portal_id: str, game_world) -> List['Portal']:
        """Find all portals with specific ID"""
        portals = []
        
        for x, y, obj in game_world.grid:
            if obj and obj.get_type() == "portal":
                if obj.get_portal_id() == portal_id:
                    portals.append(obj)
        
        return portals