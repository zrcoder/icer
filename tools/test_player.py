# Test script for player and basic game mechanics

from src.world.game_world import GameWorld
from src.entities.player import Player
from src.entities.objects.wall import Wall
from src.entities.objects.ice_block import IceBlock
from src.game.constants import GRID_WIDTH, GRID_HEIGHT


def test_player_movement():
    """Test player movement capabilities"""
    print("Testing Player Movement...")
    
    world = GameWorld(10, 8)
    player = Player(5, 1)
    world.add_object(player, 5, 1)
    
    # Test basic movement
    assert world.get_object_at(5, 1) == player, "Player should start at position"
    
# Try to move right (should succeed) - use time > cooldown
    success = player.try_move(1, 0, world, 1.0)
    assert success, "Should move right to empty space"
    assert world.get_object_at(6, 1) == player, "Player should be at new position"
    assert world.is_empty(5, 1), "Old position should be empty"
    
    # Try to move left (should succeed) - wait for cooldown
    success = player.try_move(-1, 0, world, 2.0)  # Use 2.0 to ensure cooldown is passed
    assert success, "Should move left to empty space"
    assert world.get_object_at(5, 1) == player, "Player should be back at start"
    
    # Add wall and test collision
    wall = Wall(6, 1)
    world.add_object(wall, 6, 1)
    
    success = player.try_move(1, 0, world, 2.0)  # Use 2.0 to ensure cooldown
    assert not success, "Should not move into wall"
    assert world.get_object_at(5, 1) == player, "Player should stay at position"
    
    print("✓ Player movement tests passed!")


def test_player_jumping():
    """Test player jumping over obstacles"""
    print("\nTesting Player Jumping...")
    
    world = GameWorld(10, 8)
    player = Player(3, 1)
    world.add_object(player, 3, 1)
    
    # Add floor
    for x in range(10):
        world.add_object(Wall(x, 0), x, 0)
    
    # Add a 1-high wall to jump over
    wall = Wall(4, 1)
    world.add_object(wall, 4, 1)
    
    # Try to jump over the wall
    print(f"Player jumping from ({player.grid_x},{player.grid_y})")
    success = player.try_move(1, 0, world, 1.0)
    print(f"Jump result: {success}, position: ({player.grid_x},{player.grid_y})")
    assert success, "Should jump over 1-high wall"
    assert world.get_object_at(4, 2) == player, "Player should land on top of wall"
    
    # Check jump animation state
    assert player.is_jumping_animation(), "Player should be in jump animation"
    
    print("✓ Player jumping tests passed!")


def test_ice_block_creation():
    """Test ice block creation and removal"""
    print("\nTesting Ice Block Creation...")
    
    world = GameWorld(10, 8)
    player = Player(5, 3)
    world.add_object(player, 5, 3)
    
    # Add floor
    for x in range(10):
        world.add_object(Wall(x, 0), x, 0)
    
    # Test ice creation to the right
    can_create, reason, (ice_x, ice_y) = player.can_create_ice_right(world, 1.0)
    assert can_create, "Should be able to create ice to the right"
    assert (ice_x, ice_y) == (6, 2), "Should create at right-below position"
    
    # Create ice block
    success = player.create_ice_block(ice_x, ice_y, world, 1.0)
    assert success, "Should successfully create ice block"
    
    ice_obj = world.get_object_at(6, 2)
    assert ice_obj is not None, "Ice block should exist at position"
    assert ice_obj.get_type() == "ice_block", "Should be ice block type"
    
    # Test ice removal
    can_create, reason, (ice_x, ice_y) = player.can_create_ice_right(world, 1.1)
    assert can_create, "Should detect existing ice block"
    assert reason == "remove_existing", "Should identify removal scenario"
    
    success = player.create_ice_block(ice_x, ice_y, world, 1.1)
    assert success, "Should successfully remove ice block"
    assert world.is_empty(6, 2), "Ice block should be removed"
    
    print("✓ Ice block creation tests passed!")


def test_ice_block_properties():
    """Test ice block properties and behavior"""
    print("\nTesting Ice Block Properties...")
    
    world = GameWorld(10, 8)
    
    # Test ice block basic properties
    ice = IceBlock(5, 2)
    assert ice.get_type() == "ice_block", "Should have correct type"
    assert ice.is_solid(), "Ice block should be solid"
    assert ice.is_pushable(), "Ice block should be pushable"
    assert ice.is_fragile(), "Ice block should be fragile"
    
    # Test firm status with attachments
    world.add_object(ice, 5, 2)
    
    # Add wall next to ice (should make it firm)
    wall = Wall(4, 2)
    world.add_object(wall, 4, 2)
    
    ice.check_firm_status(world)
    assert ice.is_firm(), "Ice should be firm when attached to wall"
    
    # Remove wall and check status
    world.remove_object(wall)
    ice.check_firm_status(world)
    assert not ice.is_firm(), "Ice should not be firm when not attached"
    
    print("✓ Ice block property tests passed!")


def test_level_setup():
    """Test basic level setup"""
    print("\nTesting Level Setup...")
    
    world = GameWorld(GRID_WIDTH, GRID_HEIGHT)
    player = Player(GRID_WIDTH // 2, 1)
    
    # Create basic level
    world.add_object(player, player.grid_x, player.grid_y)
    
    # Create floor
    for x in range(GRID_WIDTH):
        world.add_object(Wall(x, 0), x, 0)
    
    # Add some obstacles
    world.add_object(Wall(5, 2), 5, 2)
    world.add_object(Wall(6, 2), 6, 2)
    world.add_object(Wall(7, 2), 7, 2)
    
    # Verify setup
    assert world.get_object_at(player.grid_x, player.grid_y) == player, "Player should be placed"
    assert world.count_objects_of_type(Wall) >= GRID_WIDTH + 3, "Should have floor and obstacles"
    
    print("✓ Level setup tests passed!")


def main():
    """Run all player and mechanics tests"""
    print("=== ICER Player & Game Mechanics Tests ===\n")
    
    try:
        test_player_movement()
        test_player_jumping()
        test_ice_block_creation()
        test_ice_block_properties()
        test_level_setup()
        
        print("\n🎉 All player tests passed successfully!")
        print("\nPlayer system is ready for full game integration!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()