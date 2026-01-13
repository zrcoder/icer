# Input Handler for Game Controls

from typing import Dict, Set, Callable, Optional

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    pygame = None

from src.game.constants import *


class InputHandler:
    """Handles all game input processing"""
    
    def __init__(self):
        self.keys_pressed: Set[int] = set()
        self.keys_just_pressed: Set[int] = set()
        self.keys_just_released: Set[int] = set()
        self.key_bindings: Dict[str, int] = {}
        self.action_callbacks: Dict[str, Callable] = {}
        
        # Initialize default key bindings
        self._setup_default_bindings()
    
    def _setup_default_bindings(self):
        """Setup default key bindings"""
        if not PYGAME_AVAILABLE:
            return
            
        self.key_bindings = {
            'move_left': pygame.K_j,
            'move_right': pygame.K_l,
            'ice_left': pygame.K_a,
            'ice_right': pygame.K_d,
            'alt_left': pygame.K_LEFT,
            'alt_right': pygame.K_RIGHT,
            'pause': pygame.K_ESCAPE,
            'restart': pygame.K_r,
            'menu': pygame.K_TAB,
        }
    
    def update(self):
        """Update input state (call once per frame)"""
        if not PYGAME_AVAILABLE:
            return
            
        # Get current keyboard state
        current_keys = pygame.key.get_pressed()
        current_key_set = set(i for i, pressed in enumerate(current_keys) if pressed)
        
        # Calculate just pressed and just released keys
        self.keys_just_pressed = current_key_set - self.keys_pressed
        self.keys_just_released = self.keys_pressed - current_key_set
        self.keys_pressed = current_key_set
        
        # Process action callbacks
        self._process_actions()
    
    def _process_actions(self):
        """Process action callbacks for just pressed keys"""
        for action, key_code in self.key_bindings.items():
            if self.is_key_just_pressed(key_code):
                callback = self.action_callbacks.get(action)
                if callback:
                    callback()
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed"""
        return key in self.keys_pressed
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if a key was just pressed this frame"""
        return key in self.keys_just_pressed
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if a key was just released this frame"""
        return key in self.keys_just_released
    
    def is_action_pressed(self, action: str) -> bool:
        """Check if an action key is currently pressed"""
        key = self.key_bindings.get(action)
        if key:
            return self.is_key_pressed(key)
        return False
    
    def is_action_just_pressed(self, action: str) -> bool:
        """Check if an action key was just pressed this frame"""
        key = self.key_bindings.get(action)
        if key:
            return self.is_key_just_pressed(key)
        return False
    
    def is_action_just_released(self, action: str) -> bool:
        """Check if an action key was just released this frame"""
        key = self.key_bindings.get(action)
        if key:
            return self.is_key_just_released(key)
        return False
    
    def bind_action(self, action: str, key: int):
        """Bind an action to a key"""
        self.key_bindings[action] = key
    
    def bind_action_callback(self, action: str, callback: Callable):
        """Bind a callback function to an action"""
        self.action_callbacks[action] = callback
    
    def unbind_action_callback(self, action: str):
        """Remove callback for an action"""
        if action in self.action_callbacks:
            del self.action_callbacks[action]
    
    def get_key_for_action(self, action: str) -> Optional[int]:
        """Get the key code bound to an action"""
        return self.key_bindings.get(action)
    
    def get_action_name_for_key(self, key: int) -> Optional[str]:
        """Get the action name bound to a key"""
        for action, key_code in self.key_bindings.items():
            if key_code == key:
                return action
        return None
    
    def is_move_left_pressed(self) -> bool:
        """Check if move left is pressed (J or Left Arrow)"""
        return (self.is_action_pressed('move_left') or 
                self.is_action_pressed('alt_left'))
    
    def is_move_right_pressed(self) -> bool:
        """Check if move right is pressed (L or Right Arrow)"""
        return (self.is_action_pressed('move_right') or 
                self.is_action_pressed('alt_right'))
    
    def is_ice_left_pressed(self) -> bool:
        """Check if ice left is pressed (A key)"""
        return self.is_action_just_pressed('ice_left')
    
    def is_ice_right_pressed(self) -> bool:
        """Check if ice right is pressed (D key)"""
        return self.is_action_just_pressed('ice_right')
    
    def is_pause_pressed(self) -> bool:
        """Check if pause is pressed (ESC key)"""
        return self.is_action_just_pressed('pause')
    
    def is_restart_pressed(self) -> bool:
        """Check if restart is pressed (R key)"""
        return self.is_action_just_pressed('restart')
    
    def is_menu_pressed(self) -> bool:
        """Check if menu is pressed (TAB key)"""
        return self.is_action_just_pressed('menu')