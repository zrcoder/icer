# ICER Project Structure

## 📁 **Directory Organization**

```
ICER/
├── src/                           # Source code
│   ├── game/                      # Main game loop and state management
│   ├── world/                     # Grid system and game world
│   ├── entities/                  # All game objects
│   │   └── objects/               # Specific object implementations
│   ├── physics/                   # Physics and systems
│   ├── rules/                     # Game rules and level management
│   ├── levels/                    # Level loading and management
│   ├── rendering/                 # UI effects and visual feedback
│   ├── input/                     # Input handling
│   └── utils/                     # Utility classes
├── levels/                        # Custom level files (.toml)
├── tools/                         # Development and testing tools
│   ├── level_editor.py            # Level editor tool
│   └── test_*.py                 # Test files
├── docs/                          # Documentation
│   ├── README.md                  # Documentation index
│   ├── requirements.md            # Game requirements and specifications
│   ├── tech_stack.md              # Technical architecture and choices
│   ├── LEVEL_EDITOR_GUIDE.md      # Level editor user guide
│   └── LEVEL_EDITOR_COMPLETE.md   # Level editor development summary
├── assets/                        # Game assets (images, sounds, fonts)
├── run.sh                         # Launcher script
└── README.md                      # Main project README
```

## 📚 **Documentation Organization**

### **Core Documentation** (`docs/`)
- **[README.md](docs/README.md)** - Documentation index and overview
- **[requirements.md](docs/requirements.md)** - Complete game specifications
- **[tech_stack.md](docs/tech_stack.md)** - Technical implementation details

### **Level Editor Documentation** (`docs/`)
- **[LEVEL_EDITOR_GUIDE.md](docs/LEVEL_EDITOR_GUIDE.md)** - Comprehensive editor guide
- **[LEVEL_EDITOR_COMPLETE.md](docs/LEVEL_EDITOR_COMPLETE.md)** - Development completion summary

## 🛠️ **Tools** (`tools/`)

### **Development Tools**
- **level_editor.py** - Visual level editor with TOML export
- **test_*.py** - Unit and integration tests for various systems

### **Launcher**
- **run.sh** - Main launcher script for game and tools

## 🎮 **Game Files**

### **Source Code** (`src/`)
- **game/** - Main game loop, state management, constants
- **world/** - Grid system, game world management
- **entities/** - GameObject base class and all object types
- **physics/** - Physics engine, ice system, push system
- **rules/** - Game rules enforcement, level management
- **levels/** - Level loading, custom level support
- **rendering/** - UI effects, visual feedback systems
- **input/** - Input handling and action mapping
- **utils/** - Vector2 math, helper utilities

### **Content** (`levels/`)
- **example_level.toml** - Example custom level
- **custom_level_template.toml** - Level template file
- ***.toml** - User-created custom levels

---

**📋 This structure provides clear separation of concerns and organized documentation for the ICER project.**