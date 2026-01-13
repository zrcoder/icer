# Test script for grid and world systems

from src.world.grid import Grid
from src.world.game_world import GameWorld
from src.entities.base import GameObject


class TestObject(GameObject):
    """Test object for grid/world testing"""
    
    def __init__(self, x: int = 0, y: int = 0, obj_type: str = "test", color: tuple = (255, 0, 0)):
        super().__init__(x, y)
        self._type = obj_type
        self._color = color
        self.set_property('solid', True)
        self.set_property('affected_by_gravity', True)
    
    def get_type(self) -> str:
        return self._type
    
    def get_color(self) -> tuple:
        return self._color


def test_grid_system():
    """Test grid system functionality"""
    print("Testing Grid System...")
    
    # Create grid
    grid = Grid(10, 8)
    print(f"Created grid: {grid}")
    
    # Test position validation
    assert grid.is_valid_position(0, 0), "Origin should be valid"
    assert grid.is_valid_position(9, 7), "Max corner should be valid"
    assert not grid.is_valid_position(10, 0), "X out of bounds"
    assert not grid.is_valid_position(0, 8), "Y out of bounds"
    
    # Test object placement
    obj = TestObject(5, 3)
    assert grid.add_object(5, 3, obj), "Should add object successfully"
    assert not grid.add_object(5, 3, TestObject()), "Should not add to occupied cell"
    
    # Test retrieval
    retrieved_obj = grid.get_cell(5, 3)
    assert retrieved_obj == obj, "Should retrieve same object"
    assert grid.is_empty(4, 3), "Empty cell should be empty"
    assert not grid.is_empty(5, 3), "Occupied cell should not be empty"
    
    # Test movement
    assert grid.move_object(5, 3, 6, 3), "Should move to empty cell"
    assert grid.is_empty(5, 3), "Old position should be empty"
    assert grid.get_cell(6, 3) == obj, "Object should be at new position"
    
    # Test neighbors
    neighbors = grid.get_neighbors(6, 3)
    assert len(neighbors) == 4, "Should have 4 neighbors"
    
    print("✓ Grid system tests passed!")


def test_game_world():
    """Test game world functionality"""
    print("\nTesting Game World...")
    
    # Create world
    world = GameWorld(8, 6)
    print(f"Created world: {world}")
    
    # Test object addition
    obj1 = TestObject(2, 2, "wall", (100, 100, 100))
    obj2 = TestObject(3, 3, "ice", (0, 200, 255))
    
    assert world.add_object(obj1, 2, 2), "Should add object 1"
    assert world.add_object(obj2, 3, 3), "Should add object 2"
    assert world.count_objects_of_type(TestObject) == 2, "Should have 2 test objects"
    
    # Test object retrieval
    retrieved = world.get_object_at(2, 2)
    assert retrieved == obj1, "Should retrieve correct object"
    
    # Test object movement
    assert world.move_object(obj1, 2, 4), "Should move object"
    assert world.is_empty(2, 2), "Old position should be empty"
    assert world.get_object_at(2, 4) == obj1, "Object should be at new position"
    
    # Test object removal
    success = world.remove_object(obj2)
    assert success == True, "Should return True for successful removal"
    assert world.is_empty(3, 3), "Position should be empty after removal"
    assert world.count_objects_of_type(TestObject) == 1, "Should have 1 object remaining"
    
    # Test gravity (object with no support)
    obj3 = TestObject(1, 4, "falling", (255, 0, 255))
    world.add_object(obj3, 1, 4)
    
    print(f"Before gravity: obj at {obj3.get_grid_position()}")
    world.apply_gravity()
    print(f"After gravity: obj at {obj3.get_grid_position()}")
    
    print("✓ Game world tests passed!")


def test_object_properties():
    """Test object property system"""
    print("\nTesting Object Properties...")
    
    obj = TestObject(0, 0, "special", (255, 255, 0))
    
    # Test basic properties
    obj.set_property('pushable', True)
    obj.set_property('fragile', False)
    obj.set_property('custom_value', 42)
    
    assert obj.is_pushable(), "Object should be pushable"
    assert not obj.is_fragile(), "Object should not be fragile"
    assert obj.get_property('custom_value') == 42, "Should get custom value"
    
    # Test property existence
    assert obj.has_property('pushable'), "Should have pushable property"
    assert not obj.has_property('nonexistent'), "Should not have nonexistent property"
    
    print("✓ Object property tests passed!")


def main():
    """Run all tests"""
    print("=== ICER Grid & World System Tests ===\n")
    
    try:
        test_grid_system()
        test_game_world()
        test_object_properties()
        
        print("\n🎉 All tests passed successfully!")
        print("\nGrid and world systems are ready for player implementation!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()