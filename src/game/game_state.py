# Game State Management

from enum import Enum
from typing import Optional, Dict, Any


class GameState(Enum):
    """Game state enumeration"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    WIN = "win"
    LOSE = "lose"


class GameData:
    """Game data container"""
    
    def __init__(self):
        self.current_level: int = 1
        self.max_unlocked_level: int = 1
        self.score: int = 0
        self.moves: int = 0
        self.time_elapsed: float = 0.0
        
    def reset_level_data(self):
        """Reset level-specific data"""
        self.moves = 0
        self.time_elapsed = 0.0


class GameStateManager:
    """Manages game state transitions and data"""
    
    def __init__(self):
        self.current_state: GameState = GameState.MENU
        self.previous_state: Optional[GameState] = None
        self.game_data: GameData = GameData()
        self.state_data: Dict[str, Any] = {}
        
    def change_state(self, new_state: GameState, **kwargs):
        """Change to a new game state"""
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_data.update(kwargs)
        
    def is_state(self, state: GameState) -> bool:
        """Check if currently in specified state"""
        return self.current_state == state
        
    def get_state_data(self, key: str, default: Any = None) -> Any:
        """Get state-specific data"""
        return self.state_data.get(key, default)
        
    def set_state_data(self, key: str, value: Any):
        """Set state-specific data"""
        self.state_data[key] = value