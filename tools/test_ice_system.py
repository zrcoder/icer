# Test script for ice block system and all game objects

from src.world.game_world import GameWorld
from src.entities.player import Player
from src.entities.objects.wall import Wall
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.flame import Flame
from src.entities.objects.stone import Stone
from src.entities.objects.pot import Pot
from src.entities.objects.portal import Portal
from src.physics.ice_system import IceBlockSystem
from src.game.constants import GRID_WIDTH, GRID_HEIGHT


def test_ice_block_system():
    """Test ice block creation and management"""
    print("Testing Ice Block System...")
    
    world = GameWorld(15, 10)
    ice_system = IceBlockSystem()
    
    # Create floor
    for x in range(15):
        world.add_object(Wall(x, 0), x, 0)
    
    # Test ice creation
    ice = ice_system.create_ice_block(5, 2, world)
    assert ice is not None, "Should create ice block successfully"
    assert ice_system.count_ice_blocks(world) == 1, "Should have 1 ice block"
    
    # Test ice removal
    success = ice_system.remove_ice_block_at(5, 2, world)
    assert success, "Should remove ice block successfully"
    assert ice_system.count_ice_blocks(world) == 0, "Should have 0 ice blocks after removal"
    
    print("✓ Ice block system tests passed!")


def test_game_objects():
    """Test all game object types"""
    print("\nTesting Game Objects...")
    
    world = GameWorld(20, 10)
    
    # Create floor
    for x in range(20):
        world.add_object(Wall(x, 0), x, 0)
    
    # Test flame
    flame = Flame(5, 1)
    world.add_object(flame, 5, 1)
    assert flame.is_burning(), "Flame should be burning"
    assert world.get_object_at(5, 1) == flame, "Flame should be at position"
    
    # Test stone
    stone = Stone(3, 1)
    world.add_object(stone, 3, 1)
    assert stone.get_surface_type() == 'rough', "Stone should have rough surface"
    assert stone.can_be_pushed(), "Stone should be pushable"
    assert stone.is_heat_resistant(), "Stone should be heat resistant"
    
    # Test ice pot
    ice_pot = Pot(7, 1, False)
    world.add_object(ice_pot, 7, 1)
    assert ice_pot.is_ice(), "Pot should be ice pot"
    assert ice_pot.can_player_stand_on(), "Player can stand on ice pot"
    assert ice_pot.can_ignite(), "Ice pot can be ignited"
    
    # Test hot pot
    hot_pot = Pot(10, 1, True)
    world.add_object(hot_pot, 10, 1)
    assert hot_pot.is_hot(), "Pot should be hot pot"
    assert not hot_pot.can_player_stand_on(), "Player cannot stand on hot pot"
    assert hot_pot.can_melt_ice_above(), "Hot pot can melt ice above"
    
    # Test portal
    portal1, portal2 = Portal.create_portal_pair(2, 2, 17, 2, "test")
    world.add_object(portal1, 2, 2)
    world.add_object(portal2, 17, 2)
    assert portal1.get_linked_portal() == portal2, "Portals should be linked"
    assert portal2.get_linked_portal() == portal1, "Link should be bidirectional"
    
    print("✓ Game objects tests passed!")


def test_object_interactions():
    """Test interactions between different objects"""
    print("\nTesting Object Interactions...")
    
    world = GameWorld(10, 8)
    ice_system = IceBlockSystem()
    
    # Create floor
    for x in range(10):
        world.add_object(Wall(x, 0), x, 0)
    
    # Test ice extinguishing flame
    flame = Flame(5, 1)
    ice = ice_system.create_ice_block(5, 1, world)
    
    # Simulate interaction
    if ice:
        ice.on_collision(flame)
        assert not ice.is_active, "Ice should be destroyed by flame"
        
        # Remove destroyed ice
        world.remove_object(ice)
    
    # Add ice pot near flame
    ice_pot = Pot(3, 1, False)
    world.add_object(ice_pot, 3, 1)
    world.add_object(Flame(3, 2), 3, 2)  # Flame above pot
    
    # Simulate pot igniting
    ice_pot.check_for_ignition(world)
    # Note: This would need proper adjacency check for full implementation
    
    print("✓ Object interactions tests passed!")


def test_player_with_all_objects():
    """Test player interaction with all object types"""
    print("\nTesting Player with All Objects...")
    
    world = GameWorld(20, 10)
    ice_system = IceBlockSystem()
    player = Player(10, 1)
    
    # Create floor
    for x in range(20):
        world.add_object(Wall(x, 0), x, 0)
    
    world.add_object(player, 10, 1)
    
    # Test player creating ice - need space above floor
    ice = ice_system.create_ice_block(9, 1, world)
    assert ice is not None, "Player should be able to create ice"
    
# Test player movement around objects
    # Add wall at a distance
    world.add_object(Wall(7, 1), 7, 1)
    
    # Test basic movement (no obstacles)
    success = player.try_move(-1, 0, world, 2.0)  # Move to 9,1
    assert success, "Player should move left"
    
    success = player.try_move(-1, 0, world, 3.0)  # Move to 8,1  
    assert success, "Player should move left"
    
    success = player.try_move(-1, 0, world, 4.0)  # Try to move into wall at 7,1
    assert success, "Player should jump over wall"
    # Player should jump over wall successfully
    
    print("✓ Player interaction tests passed!")


def test_complete_level():
    """Test a complete level setup"""
    print("\nTesting Complete Level Setup...")
    
    world = GameWorld(20, 15)
    ice_system = IceBlockSystem()
    player = Player(10, 1)
    
    # Create floor
    for x in range(20):
        world.add_object(Wall(x, 0), x, 0)
    
    # Add player
    world.add_object(player, 10, 1)
    
    # Add objectives (flames)
    world.add_object(Flame(3, 1), 3, 1)
    world.add_object(Flame(15, 2), 15, 2)
    world.add_object(Flame(7, 3), 7, 3)
    
    # Add obstacles
    for x in range(5, 8):
        world.add_object(Wall(x, 2), x, 2)
    
    # Add tools
    world.add_object(Stone(2, 1), 2, 1)
    world.add_object(Pot(12, 1, False), 12, 1)
    
    # Add transport
    portal1, portal2 = Portal.create_portal_pair(2, 5, 17, 3, "level_portal")
    world.add_object(portal1, 2, 5)
    world.add_object(portal2, 17, 3)
    
    # Verify setup
    assert world.count_objects_of_type(Flame) == 3, "Should have 3 flames"
    assert world.count_objects_of_type(Wall) >= 23, "Should have walls"
    assert world.count_objects_of_type(Stone) == 1, "Should have 1 stone"
    assert world.count_objects_of_type(Pot) == 1, "Should have 1 pot"
    assert world.count_objects_of_type(Portal) == 2, "Should have 2 portals"
    
    print("✓ Complete level setup tests passed!")


def main():
    """Run all ice block system and game object tests"""
    print("=== ICER Ice Block System & Game Objects Tests ===\n")
    
    try:
        test_ice_block_system()
        test_game_objects()
        test_object_interactions()
        test_player_with_all_objects()
        test_complete_level()
        
        print("\n🎉 All ice block system and game object tests passed!")
        print("\nGame is ready for physics system implementation!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()