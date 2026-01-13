# Player Class for ICER Character

from typing import Optional, Tuple
from src.entities.base import GameObject
from src.game.constants import COLOR_PLAYER
from src.utils.vector2 import Vector2


class Player(GameObject):
    """Player character ICER"""
    
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        
        # Player properties
        self.set_property('solid', False)  # Player doesn't block other objects
        self.set_property('pushable', False)
        self.set_property('fragile', False)
        self.set_property('affected_by_gravity', False)
        self.set_property('supports_weight', True)
        self.set_property('interactive', True)
        self.set_property('jump_height', 1)  # Can jump 1 unit high
        self.set_property('move_cooldown', 0.2)  # Seconds between moves
        self.set_property('jump_cooldown', 0.3)  # Seconds between jumps
        
        # Movement state
        self.last_move_time = 0.0
        self.last_jump_time = 0.0
        self.is_jumping = False
        self.jump_start_time = 0.0
        self.jump_duration = 0.3  # Seconds for jump animation
        
        # Ice block creation state
        self.ice_creation_cooldown = 0.1  # Seconds between ice operations
        self.last_ice_time = 0.0
    
    def get_type(self) -> str:
        return "player"
    
    def get_color(self) -> tuple:
        return COLOR_PLAYER
    
    def can_move_to(self, new_x: int, new_y: int, game_world) -> Tuple[bool, str]:
        """Check if player can move to position"""
        if not game_world.is_valid_position(new_x, new_y):
            return False, "out_of_bounds"
        
        # Check for obstacles
        obj_at_target = game_world.get_object_at(new_x, new_y)
        if obj_at_target:
            if obj_at_target.is_solid():
                # Check if we can jump over it
                if obj_at_target.get_property('height', 1) <= self.get_property('jump_height', 1):
                    # Try to jump to the position above the obstacle
                    jump_x, jump_y = new_x, new_y + 1
                    if self._can_jump_to(jump_x, jump_y, game_world):
                        return True, "jump"
                    else:
                        return False, "blocked_by_jumpable"
                else:
                    return False, "blocked_by_tall"
            else:
                return False, "blocked_by_object"
        
        return True, "clear"
    
    def _can_jump_to(self, jump_x: int, jump_y: int, game_world) -> bool:
        """Check if player can jump to position"""
        if not game_world.is_valid_position(jump_x, jump_y):
            return False
        
        obj_at_jump = game_world.get_object_at(jump_x, jump_y)
        if obj_at_jump and obj_at_jump.is_solid():
            return False
        
        # Check if there's support for landing
        if jump_y > 0:
            below_obj = game_world.get_object_at(jump_x, jump_y - 1)
            if below_obj is None:
                return False  # Need something to land on
        
        return True
    
    def try_move(self, dx: int, dy: int, game_world, current_time: float) -> bool:
        """Try to move player in direction"""
        # Check cooldown
        if current_time - self.last_move_time < self.get_property('move_cooldown', 0.2):
            return False
        
        new_x, new_y = self.grid_x + dx, self.grid_y + dy
        
        # Check if move is possible
        can_move, reason = self.can_move_to(new_x, new_y, game_world)
        
        if can_move:
            if reason == "jump":
                # Perform jump
                return self._jump_to(new_x, new_y + 1, game_world, current_time)
            else:
                # Normal move
                if game_world.move_object(self, new_x, new_y):
                    self.last_move_time = current_time
                    return True
        
        return False
    
    def _jump_to(self, jump_x: int, jump_y: int, game_world, current_time: float) -> bool:
        """Perform jump to position"""
        if current_time - self.last_jump_time < self.get_property('jump_cooldown', 0.3):
            return False
        
        if game_world.move_object(self, jump_x, jump_y):
            self.is_jumping = True
            self.jump_start_time = current_time
            self.last_jump_time = current_time
            self.last_move_time = current_time
            return True
        
        return False
    
    def update(self, dt: float):
        """Update player state"""
        current_time = self.get_property('current_time', 0.0)
        
        # Update jump animation state
        if self.is_jumping:
            if current_time - self.jump_start_time > self.jump_duration:
                self.is_jumping = False
    
    def can_create_ice_at(self, ice_x: int, ice_y: int, game_world, current_time: float) -> Tuple[bool, str]:
        """Check if player can create ice block at position"""
        # Check cooldown
        if current_time - self.last_ice_time < self.ice_creation_cooldown:
            return False, "cooldown"
        
        # Check if position is valid
        if not game_world.is_valid_position(ice_x, ice_y):
            return False, "out_of_bounds"
        
        # Check if position is empty
        if not game_world.is_empty(ice_x, ice_y):
            obj = game_world.get_object_at(ice_x, ice_y)
            if obj.get_type() == "ice_block":
                return True, "remove_existing"  # Can remove existing ice block
            else:
                return False, "occupied"
        
        # Check if position is adjacent to player (left or right below)
        dx = abs(ice_x - self.grid_x)
        dy = ice_y - self.grid_y
        
        if dy == -1 and dx == 0:  # Directly below player
            return True, "valid_below"
        elif dy == -1 and dx == 1:  # Right below player
            return True, "valid_right_below"
        elif dy == -1 and dx == -1:  # Left below player
            return True, "valid_left_below"
        else:
            return False, "too_far"
    
    def can_create_ice_left(self, game_world, current_time: float) -> Tuple[bool, str, Tuple[int, int]]:
        """Check if player can create ice block to left-below"""
        ice_x, ice_y = self.grid_x - 1, self.grid_y - 1
        can_create, reason = self.can_create_ice_at(ice_x, ice_y, game_world, current_time)
        return can_create, reason, (ice_x, ice_y)
    
    def can_create_ice_right(self, game_world, current_time: float) -> Tuple[bool, str, Tuple[int, int]]:
        """Check if player can create ice block to right-below"""
        ice_x, ice_y = self.grid_x + 1, self.grid_y - 1
        can_create, reason = self.can_create_ice_at(ice_x, ice_y, game_world, current_time)
        return can_create, reason, (ice_x, ice_y)
    
    def create_ice_block(self, ice_x: int, ice_y: int, game_world, current_time: float) -> bool:
        """Create ice block at position"""
        can_create, reason = self.can_create_ice_at(ice_x, ice_y, game_world, current_time)
        
        if reason == "remove_existing":
            # Remove existing ice block
            ice_obj = game_world.get_object_at(ice_x, ice_y)
            if ice_obj and ice_obj.get_type() == "ice_block":
                game_world.remove_object(ice_obj)
                self.last_ice_time = current_time
                return True
        elif can_create:
            # Create new ice block
            from src.entities.objects.ice_block import IceBlock
            ice_block = IceBlock(ice_x, ice_y)
            if game_world.add_object(ice_block, ice_x, ice_y):
                self.last_ice_time = current_time
                return True
        
        return False
    
    def is_jumping_animation(self) -> bool:
        """Check if player is in jumping animation"""
        return self.is_jumping
    
    def get_jump_progress(self, current_time: float) -> float:
        """Get jump animation progress (0.0 to 1.0)"""
        if not self.is_jumping:
            return 0.0
        
        elapsed = current_time - self.jump_start_time
        progress = min(elapsed / self.jump_duration, 1.0)
        return progress
    
    def on_interact(self, actor: GameObject) -> bool:
        """Handle interaction with player"""
        # Player can't be interacted with by other objects
        return False
    
    def get_render_offset(self, current_time: float) -> Tuple[int, int]:
        """Get rendering offset for animations"""
        offset_x, offset_y = 0, 0
        
        if self.is_jumping:
            progress = self.get_jump_progress(current_time)
            # Simple jump arc: go up then down
            jump_height = 20 * (1.0 - abs(2 * progress - 1.0))  # Parabolic arc
            offset_y = int(jump_height)
        
        return (offset_x, offset_y)