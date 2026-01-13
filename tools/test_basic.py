# Simple test script without pygame

from src.game.game_state import GameStateManager, GameState
from src.utils.vector2 import Vector2

def test_basic_functionality():
    """Test basic game functionality without pygame"""
    print("Testing ICER game components...")
    
    # Test Vector2
    v1 = Vector2(3, 4)
    v2 = Vector2(1, 2)
    v3 = v1 + v2
    print(f"Vector2 test: {v1} + {v2} = {v3}")
    print(f"Vector2 magnitude: {v1.magnitude()}")
    
    # Test GameStateManager
    state_manager = GameStateManager()
    print(f"Initial state: {state_manager.current_state}")
    
    state_manager.change_state(GameState.PLAYING)
    print(f"Changed state: {state_manager.current_state}")
    
    print("Basic functionality test completed!")
    print("\nNote: Pygame is required for full game functionality.")
    print("Install pygame with: pip install pygame")

if __name__ == "__main__":
    test_basic_functionality()