#!/bin/bash

# ICER Game Launcher
# Launch options for the ICER ice block puzzle game

echo "=== ICER Ice Block Puzzle Game ==="
echo ""
echo "Select launch option:"
echo "1) Play ICER Game"
echo "2) Level Editor"
echo "3) Test Custom Levels"
echo "4) Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo "Starting ICER Game..."
        /usr/bin/python3 src/game/main.py
        ;;
    2)
        echo "Starting Level Editor..."
        echo "Controls: 1-9 for objects, 0 for player, SPACE for eraser"
        echo "Click to place, Right-click to erase"
        echo "Ctrl+S to save, Ctrl+O to load"
        /usr/bin/python3 tools/level_editor.py
        ;;
    3)
        echo "Testing custom level loading..."
        /usr/bin/python3 -c "
from src.levels.toml_loader import load_toml_level, discover_custom_levels
import os

# Discover custom levels
custom_levels = discover_custom_levels()
print(f'Found {len(custom_levels)} custom levels:')
for level_file in custom_levels:
    print(f'  - {level_file}')

# Test loading each level
for level_file in custom_levels:
    level_data = load_toml_level(level_file)
    if level_data:
        print(f'✓ Loaded: {level_data[\"name\"]} ({level_data[\"difficulty\"]})')
    else:
        print(f'✗ Failed to load: {level_file}')
"
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please select 1-4."
        ;;
esac