# TOML Level Loader for ICER
# Adds support for loading custom TOML levels in the main game

import toml
import os
from typing import Dict, Any, List, Optional

def load_toml_level(filename: str) -> Optional[Dict[str, Any]]:
    """Load a level from TOML file and return level data compatible with LevelManager"""
    
    try:
        with open(filename, 'r') as f:
            level_data = toml.load(f)
        
        # Parse metadata
        metadata = level_data.get('level_metadata', {})
        level_id = metadata.get('id', 'custom_level')
        level_name = metadata.get('name', 'Custom Level')
        difficulty = metadata.get('difficulty', 'medium')
        author = metadata.get('author', 'Custom')
        description = metadata.get('description', 'A custom level')
        optimal_moves = metadata.get('optimal_moves')
        optimal_time = metadata.get('optimal_time')
        
        # Parse grid layout
        layout = level_data.get('level_layout', {})
        grid_strings = layout.get('grid', [])
        
        # Convert grid to objects
        objects = []
        player_start = (0, 1)  # Default position
        
        for y, row_str in enumerate(grid_strings):
            for x, char in enumerate(row_str):
                if char == '.':
                    continue
                elif char == 'P':
                    player_start = (x, y)
                elif char == 'W':
                    objects.append({'type': 'wall', 'x': x, 'y': y})
                elif char == 'S':
                    objects.append({'type': 'stone', 'x': x, 'y': y})
                elif char == 'I':
                    objects.append({'type': 'ice_block', 'x': x, 'y': y})
                elif char == 'F':
                    objects.append({'type': 'flame', 'x': x, 'y': y})
                elif char == 'C':
                    objects.append({'type': 'ice_pot', 'x': x, 'y': y, 'properties': {'is_hot': False}})
                elif char == 'H':
                    objects.append({'type': 'ice_pot', 'x': x, 'y': y, 'properties': {'is_hot': True}})
                elif char in ['1', '2', '3']:
                    objects.append({'type': 'portal', 'x': x, 'y': y, 'properties': {'portal_id': f'portal_{char}'}})
        
        # Create level data structure
        converted_level = {
            'level_id': level_id,
            'name': level_name,
            'width': len(grid_strings[0]) if grid_strings else 20,
            'height': len(grid_strings),
            'player_start': player_start,
            'objects': objects,
            'requirements': {'require_all_flames_extinguished': True},
            'description': description,
            'difficulty': difficulty,
            'author': author,
            'hints': [],
            'optimal_moves': optimal_moves,
            'optimal_time': optimal_time
        }
        
        return converted_level
        
    except Exception as e:
        print(f"Error loading TOML level {filename}: {e}")
        return None


def discover_custom_levels(levels_dir: str = "levels") -> List[str]:
    """Discover all custom level files in the levels directory"""
    
    custom_levels = []
    
    if os.path.exists(levels_dir):
        for filename in os.listdir(levels_dir):
            if filename.endswith('.toml'):
                filepath = os.path.join(levels_dir, filename)
                custom_levels.append(filepath)
    
    return custom_levels