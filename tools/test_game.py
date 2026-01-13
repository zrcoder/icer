#!/usr/bin/env python3
"""
Quick test script to verify ICER game functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, '.')

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        import src.game.constants
        from src.game.constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT
        print("✓ Constants imported")
    except Exception as e:
        print(f"✗ Constants import failed: {e}")
        return False
    
    try:
        from src.game.game_state import GameStateManager, GameState
        print("✓ Game state imported")
    except Exception as e:
        print(f"✗ Game state import failed: {e}")
        return False
    
    try:
        from src.entities.base import GameObject
        from src.entities.player import Player
        from src.entities.objects.wall import Wall
        from src.entities.objects.ice_block import IceBlock
        print("✓ Entities imported")
    except Exception as e:
        print(f"✗ Entities import failed: {e}")
        return False
    
    try:
        from src.world.game_world import GameWorld
        from src.world.grid import Grid
        print("✓ World system imported")
    except Exception as e:
        print(f"✗ World system import failed: {e}")
        return False
    
    try:
        from src.physics.physics_engine import PhysicsEngine
        from src.physics.ice_system import IceBlockSystem
        print("✓ Physics system imported")
    except Exception as e:
        print(f"✗ Physics system import failed: {e}")
        return False
    
    try:
        from src.rules.game_rules import GameRulesSystem
        from src.levels.level_manager import LevelManager
        print("✓ Rules and levels imported")
    except Exception as e:
        print(f"✗ Rules and levels import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic game functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from src.world.game_world import GameWorld
        from src.entities.objects.wall import Wall
        from src.entities.player import Player
        from src.physics.physics_engine import PhysicsEngine
        
        # Create world
        world = GameWorld()
        print("✓ Game world created")
        
        # Add objects
        wall = Wall(5, 0)
        world.add_object(wall, 5, 0)
        print("✓ Wall added to world")
        
        player = Player(3, 1)
        world.add_object(player, 3, 1)
        print("✓ Player added to world")
        
        # Create physics engine
        physics = PhysicsEngine(world)
        print("✓ Physics engine created")
        
        # Test physics update
        physics.update(0.016)  # 60 FPS
        print("✓ Physics update works")
        
        # Test GameObject methods
        assert hasattr(player, 'stop_sliding')
        assert hasattr(player, 'can_ignite')
        assert hasattr(player, 'is_firm')
        assert hasattr(player, 'get_push_distance')
        print("✓ GameObject methods exist")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_level_loading():
    """Test level loading"""
    print("\nTesting level loading...")
    
    try:
        from src.world.game_world import GameWorld
        from src.physics.physics_engine import PhysicsEngine
        from src.physics.ice_system import IceBlockSystem
        from src.rules.game_rules import GameRulesSystem
        from src.levels.level_manager import LevelManager
        
        # Create systems
        world = GameWorld()
        physics = PhysicsEngine(world)
        ice_system = IceBlockSystem()
        rules = GameRulesSystem(world, physics, ice_system)
        level_manager = LevelManager(world, rules, physics, ice_system)
        
        # Load tutorial level
        success = level_manager.load_level("tutorial_1")
        if success:
            print("✓ Tutorial level loaded successfully")
            
            # Check objects were created
            objects = list(world.grid)
            print(f"✓ {len(objects)} objects in level")
            
            return True
        else:
            print("✗ Failed to load tutorial level")
            return False
            
    except Exception as e:
        print(f"✗ Level loading test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ICER Game Quick Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_level_loading
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print(f"❌ {test.__name__} failed")
            break
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! ICER game is working correctly!")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)