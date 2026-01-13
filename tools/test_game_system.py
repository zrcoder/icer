# Test script for game rules and level system

from src.world.game_world import GameWorld
from src.levels.level_manager import LevelManager
from src.entities.player import Player
from src.entities.objects.wall import Wall
from src.entities.objects.flame import Flame
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.stone import Stone
from src.entities.objects.pot import Pot
from src.entities.objects.portal import Portal
from src.game.constants import GRID_WIDTH, GRID_HEIGHT
from src.physics.physics_engine import PhysicsEngine
from src.physics.ice_system import IceBlockSystem
from src.rules.game_rules import GameRulesSystem


def test_level_system():
    """Test level loading and management"""
    print("Testing Level System...")
    
    world = GameWorld(20, 15)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    level_manager = LevelManager(world, GameRulesSystem(world, physics, ice_system), physics, ice_system)
    
    # Test loading first level
    success = level_manager.load_level("tutorial_1")
    assert success, "Should load tutorial level 1"
    
    # Check that level was loaded
    available_levels = level_manager.get_available_levels()
    assert len(available_levels) >= 2, "Should have at least 2 levels"
    assert available_levels[0]['level_id'] == "tutorial_1", "First level should be tutorial_1"
    assert available_levels[0]['is_unlocked'], "Tutorial level should be unlocked"
    assert not available_levels[0]['is_completed'], "Tutorial level should not be completed"
    
    print("✓ Game system tests passed!")


def test_game_rules():
    """Test game rule enforcement"""
    print("\nTesting Game Rules...")
    
    world = GameWorld(15, 10)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    rules = GameRulesSystem(world, physics, ice_system)
    
    # Create floor
    for x in range(10):
        world.add_object(Wall(x, 0), x, 0)
    
    # Create flame and ice block
    flame = Flame(5, 1)
    ice = IceBlock(6, 1)
    
    world.add_object(flame, 5, 1)
    world.add_object(ice, 6, 1)
    
    # Move ice block into flame
    world.move_object(ice, 5, 1)
    
    # Update rules (should extinguish flame)
    rules.update(1.0)
    
    # Check that both are destroyed
    assert not flame.is_active, "Flame should be extinguished"
    assert not ice.is_active, "Ice should be destroyed"
    assert world.is_empty(5, 1), "Position should be empty"
    
    print("✓ Game rules tests passed!")


def test_pot_ignition():
    """Test pot ignition mechanics"""
    print("\nTesting Pot Ignition...")
    
    world = GameWorld(15, 10)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    rules = GameRulesSystem(world, physics, ice_system)
    
    # Create floor
    for x in range(10):
        world.add_object(Wall(x, 0), x, 0)
    
    # Create ice pot and flame
    ice_pot = Pot(3, 1, False)
    flame = Flame(3, 1)
    
    world.add_object(ice_pot, 3, 1)
    world.add_object(flame, 4, 1)
    
    # Update rules (should ignite pot)
    rules.update(1.0)
    
    # Check that pot became hot
    assert ice_pot.is_hot(), "Ice pot should be ignited"
    
    print("✓ Pot ignition tests passed!")


def test_portal_system():
    """Test portal transportation"""
    print("\nTesting Portal System...")
    
    world = GameWorld(20, 12)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    rules = GameRulesSystem(world, physics, ice_system)
    level_manager = LevelManager(world, rules, physics, ice_system)
    
    # Create floor
    for x in range(20):
        world.add_object(Wall(x, 0), x, 0)
    
    # Create player and portals
    player = Player(2, 1)
    world.add_object(player, 2, 1)
    
    portal1, portal2 = Portal.create_portal_pair(5, 5, 15, 5, "test_portal")
    world.add_object(portal1, 5, 5)
    world.add_object(portal2, 15, 5)
    
    # Set up rules with player reference
    rules.set_player(player)
    
    # Move player onto portal 1
    world.move_object(player, 5, 5)
    
    # Update rules (should transport player)
    rules.update(1.0)
    
    # Check that player was transported
    assert player.grid_x == 15, "Player should be at portal 2"
    assert player.grid_y == 5, "Player should maintain same height"
    
    print("✓ Portal system tests passed!")


def test_level_progression():
    """Test level unlocking progression"""
    print("\nTesting Level Progression...")
    
    world = GameWorld(15, 10)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    rules = GameRulesSystem(world, physics, ice_system)
    level_manager = LevelManager(world, rules, physics, ice_system)
    
    # Load tutorial level
    level_manager.load_level("tutorial_1")
    
    # Complete level
    level_manager.complete_level()
    
    # Check that basic levels are unlocked
    available_levels = level_manager.get_available_levels()
    basic_levels = [l for l in available_levels if l['level_id'].startswith('basic_')]
    
    # Should unlock first 2 basic levels after tutorial
    assert len(basic_levels) >= 2, "Should unlock some basic levels"
    
    # Check that completed level is marked
    tutorial_level = level_manager.get_level_info("tutorial_1")
    assert tutorial_level['is_completed'], "Tutorial level should be marked completed"
    
    print("✓ Level progression tests passed!")


def test_complete_scenario():
    """Test a complete game scenario"""
    print("\nTesting Complete Game Scenario...")
    
    world = GameWorld(20, 12)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    rules = GameRulesSystem(world, physics, ice_system)
    level_manager = LevelManager(world, rules, physics, ice_system)
    
    # Load medium level with complex puzzle
    level_manager.load_level("medium_1")
    
    # Get initial status
    status = rules.get_level_status()
    initial_moves = status['moves_taken']
    initial_flames = status['flames_remaining']
    
    # Solve puzzle by extinguishing all flames
    for x, y, obj in world.grid:
        if obj and obj.get_type() == "flame":
            # Place ice block on flame
            ice = IceBlock(x, y + 1)
            world.add_object(ice, x, y + 1)
            rules._extinguish_flame_with_ice(obj, ice)
            break
    
    # Update physics
    physics._apply_gravity(1.0)
    rules.update(1.0)
    
    # Check puzzle solved
    final_status = rules.get_level_status()
    assert final_status['moves_taken'] > initial_moves, "Moves should have increased"
    assert final_status['flames_remaining'] < initial_flames, "Flames should have decreased"
    assert len(final_status['puzzles_list']) > 0, "Puzzles should have been solved"
    
    print("✓ Complete scenario tests passed!")


def test_save_load_system():
    """Test save/load functionality"""
    print("\nTesting Save/Load System...")
    
    world = GameWorld(15, 10)
    physics = PhysicsEngine(world)
    ice_system = IceBlockSystem()
    level_manager = LevelManager(world, GameRulesSystem(world, physics, ice_system), physics, ice_system)
    
    # Complete a level
    level_manager.load_level("tutorial_1")
    level_manager.complete_level()
    
    # Save progress
    save_success = level_manager.save_progress("test_save.json")
    assert save_success, "Should save progress successfully"
    
    # Load progress
    load_success = level_manager.load_progress("test_save.json")
    assert load_success, "Should load progress successfully"
    
    # Verify data persistence
    assert level_manager.current_level_id == "tutorial_1", "Level should be loaded"
    assert "tutorial_1" in level_manager.completed_levels, "Level should be marked completed"
    
    print("✓ Save/Load system tests passed!")


def main():
    """Run all game rules and level system tests"""
    print("=== ICER Game Rules & Level System Tests ===\n")
    
    try:
        test_level_system()
        test_game_rules()
        test_pot_ignition()
        test_portal_system()
        test_level_progression()
        test_complete_scenario()
        test_save_load_system()
        
        print("\n🎉 All game rules and level system tests passed!")
        print("\nGame systems are fully integrated and ready!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()