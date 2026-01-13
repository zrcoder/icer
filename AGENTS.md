# ICER Game Development Guide

This document contains development guidelines and commands for working on the ICER ice block puzzle game.

## Development Commands

### Running the Game
```bash
# Main game entry point
python3 src/game/main.py

# Using the launcher script (recommended)
./run.sh

# Level editor
python3 tools/level_editor.py
```

### Testing Commands
```bash
# Run individual test files
python3 tools/test_basic.py
python3 tools/test_player.py
python3 tools/test_game.py
python3 tools/test_grid_world.py
python3 tools/test_physics.py
python3 tools/test_ice_system.py
python3 tools/test_game_system.py

# No pytest configuration found - run tests individually
```

### Code Quality Tools
```bash
# Format code (if available)
black src/ tools/ --line-length 100

# Lint code (if available)  
flake8 src/ tools/ --max-line-length=100

# Type checking (if available)
mypy src/ tools/
```

## Project Structure & Architecture

### Core Architecture
- **Component-based entity system** with `GameObject` base class
- **Fixed-timestep physics engine** for consistent gameplay
- **Grid-based world system** (20x15 grid by default)
- **State management** through `GameStateManager`
- **Level loading** via TOML configuration files

### Module Organization
```
src/
├── game/          # Main game loop, state, constants
├── entities/      # Game objects (player, walls, items)
├── physics/       # Physics engine and systems
├── world/         # Grid system and game world
├── levels/        # Level loading and management
├── rendering/     # UI effects and visual feedback
├── input/         # Input handling system
├── utils/         # Helper classes (Vector2, etc.)
└── rules/         # Game rules and interactions
```

## Code Style Guidelines

### Import Organization
```python
# Standard library imports first
import sys
import os
from typing import Optional, Dict, Any

# Third-party imports
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

# Local imports - use absolute paths from project root
from src.game.constants import *
from src.utils.vector2 import Vector2
from src.entities.base import GameObject
```

### Class Naming & Structure
- Use **PascalCase** for class names (`GameObject`, `PhysicsEngine`)
- Use **snake_case** for methods and variables (`update()`, `grid_x`)
- Abstract base classes should end with `ABC` import and `@abstractmethod`
- Include comprehensive docstrings for all public methods

### Type Hints
```python
def __init__(self, x: int = 0, y: int = 0):
    self.grid_x: int = x
    self.grid_y: int = y
    self.position: Vector2 = Vector2(x, y)
    self.properties: Dict[str, Any] = {}

def update(self, dt: float) -> None:
    """Update object logic (called each frame)"""
    pass

def get_position(self) -> Vector2:
    """Get object position"""
    return self.position
```

### Constants & Configuration
- Define all game constants in `src/game/constants.py`
- Use **UPPER_SNAKE_CASE** for constants (`WINDOW_WIDTH`, `COLOR_PLAYER`)
- Group related constants together (colors, keys, states)

### Error Handling
```python
# Graceful handling of optional dependencies
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: Pygame not installed")

# Type checking with proper error messages
def __add__(self, other) -> 'Vector2':
    if isinstance(other, Vector2):
        return Vector2(self.x + other.x, self.y + other.y)
    else:
        raise TypeError("Can only add Vector2 to Vector2")
```

### Game Object Patterns
```python
class CustomObject(GameObject):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)
        # Set object properties
        self.set_property('solid', True)
        self.set_property('pushable', False)
        self.set_property('weight', 1)
    
    def get_type(self) -> str:
        return "custom_object"
    
    def get_color(self) -> tuple:
        return COLOR_CUSTOM
    
    def update(self, dt: float):
        # Update logic here
        pass
```

## Testing Guidelines

### Test File Structure
- Place tests in `tools/` directory with `test_*.py` naming
- Use simple assertion-based testing without complex test frameworks
- Focus on testing core mechanics without pygame dependency when possible

### Test Example
```python
def test_player_movement():
    """Test player movement capabilities"""
    world = GameWorld(10, 8)
    player = Player(5, 1)
    world.add_object(player, 5, 1)
    
    # Test basic movement
    assert world.get_object_at(5, 1) == player, "Player should start at position"
```

## Development Workflow

### Adding New Game Objects
1. Create new class inheriting from `GameObject` in `src/entities/objects/`
2. Implement required methods: `get_type()`, `get_color()`
3. Set appropriate properties (`solid`, `pushable`, `weight`, etc.)
4. Add object color constant to `src/game/constants.py`
5. Update level editor to support new object type

### Adding New Levels
1. Create TOML file in `levels/` directory
2. Follow existing level structure and naming convention
3. Test loading with custom level tester in `run.sh`

### Physics Integration
- All physics calculations should use the `PhysicsEngine` class
- Object interactions should be handled through `GameRulesSystem`
- Ice system has its own specialized update cycle

## Code Quality Standards

### Performance Considerations
- Use `magnitude_squared()` instead of `magnitude()` when comparing distances
- Cache frequently accessed object references
- Minimize object creation in update loops
- Use fixed timestep for physics consistency

### Documentation
- All public methods must have docstrings
- Complex algorithms should have inline comments
- Constants should be documented where usage isn't obvious
- Update README.md when adding major features

## Dependencies
- **pygame 2.1.0** - Core game engine and rendering
- **pytest 6.2.0** - Testing framework (installed but not configured)
- **black 21.0.0** - Code formatting (installed but not configured)
- **flake8 3.9.0** - Linting (installed but not configured)
- **mypy 0.910** - Type checking (installed but not configured)

Note: Quality tools are installed but not integrated into workflow - consider setting up pre-commit hooks or CI configuration.