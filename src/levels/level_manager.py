# Level System - Level loading and management

from typing import List, Dict, Any, Optional, Tuple
import json
from src.levels.toml_loader import load_toml_level, discover_custom_levels
from src.world.game_world import GameWorld
from src.entities.base import GameObject
from src.entities.player import Player
from src.entities.objects.wall import Wall
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.flame import Flame
from src.entities.objects.stone import Stone
from src.entities.objects.pot import Pot
from src.entities.objects.portal import Portal
from src.rules.game_rules import GameRulesSystem
from src.physics.physics_engine import PhysicsEngine
from src.physics.ice_system import IceBlockSystem


class Level:
    """Single level data"""
    
    def __init__(self, level_id: str, name: str, width: int, height: int):
        self.level_id = level_id
        self.name = name
        self.width = width
        self.height = height
        
        # Level data
        self.player_start: Tuple[int, int] = (0, 0)
        self.objects: List[Dict[str, Any]] = []
        
        # Level requirements
        self.requirements: Dict[str, Any] = {}
        
        # Level metadata
        self.description: str = ""
        self.difficulty: str = "medium"
        self.author: str = ""
        self.hints: List[str] = []
        
        # Solution tracking
        self.optimal_moves: Optional[int] = None
        self.optimal_time: Optional[float] = None
    
    def add_object(self, obj_type: str, x: int, y: int, **properties):
        """Add object to level"""
        obj_data = {
            'type': obj_type,
            'x': x,
            'y': y,
            'properties': properties
        }
        self.objects.append(obj_data)
    
    def add_player_start(self, x: int, y: int):
        """Set player start position"""
        self.player_start = (x, y)
    
    def set_requirement(self, requirement: str, value: Any):
        """Set level requirement"""
        self.requirements[requirement] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert level to dictionary"""
        return {
            'level_id': self.level_id,
            'name': self.name,
            'width': self.width,
            'height': self.height,
            'player_start': self.player_start,
            'objects': self.objects,
            'requirements': self.requirements,
            'description': self.description,
            'difficulty': self.difficulty,
            'author': self.author,
            'hints': self.hints,
            'optimal_moves': self.optimal_moves,
            'optimal_time': self.optimal_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Level':
        """Create level from dictionary"""
        level = cls(
            data['level_id'],
            data['name'],
            data['width'],
            data['height']
        )
        
        level.player_start = tuple(data['player_start'])
        level.objects = data.get('objects', [])
        level.requirements = data.get('requirements', {})
        level.description = data.get('description', '')
        level.difficulty = data.get('difficulty', 'medium')
        level.author = data.get('author', '')
        level.hints = data.get('hints', [])
        level.optimal_moves = data.get('optimal_moves')
        level.optimal_time = data.get('optimal_time')
        
        return level


class LevelManager:
    """Level loading and management system"""
    
    def __init__(self, game_world: GameWorld, rules: GameRulesSystem, physics: PhysicsEngine, ice_system: IceBlockSystem):
        self.game_world = game_world
        self.rules = rules
        self.physics = physics
        self.ice_system = ice_system
        
        # Level data
        self.levels: Dict[str, Level] = {}
        self.current_level: Optional[Level] = None
        self.current_level_id: str = ""
        
        # Progress tracking
        self.unlocked_levels: List[str] = []
        self.completed_levels: List[str] = []
        self.level_scores: Dict[str, Dict[str, Any]] = {}
        
        # Load built-in levels
        self._load_built_in_levels()
        
        # Load custom levels
        self._load_custom_levels()
    
    def _load_built_in_levels(self):
        """Load built-in tutorial and basic levels"""
        # Tutorial Level 1: Basic movement
        tutorial1 = Level("tutorial_1", "Movement Basics", 10, 8)
        tutorial1.description = "Learn basic movement and jumping"
        tutorial1.difficulty = "tutorial"
        tutorial1.add_player_start(5, 1)
        tutorial1.add_object("wall", 0, 0)  # Floor
        
        # Tutorial walls for jumping
        tutorial1.add_object("wall", 3, 1)
        tutorial1.add_object("wall", 4, 1)
        
        # Single flame to extinguish
        tutorial1.add_object("flame", 7, 1)
        tutorial1.set_requirement("require_all_flames_extinguished", True)
        tutorial1.optimal_moves = 8
        tutorial1.optimal_time = 15.0
        
        # Tutorial Level 2: Ice block creation
        tutorial2 = Level("tutorial_2", "Ice Creation", 12, 8)
        tutorial2.description = "Learn to create and remove ice blocks"
        tutorial2.difficulty = "tutorial"
        tutorial2.add_player_start(6, 1)
        tutorial2.add_object("wall", 0, 0)  # Floor
        
        # Higher platform with flame
        for x in range(2, 6):
            tutorial2.add_object("wall", x, 2)
        
        tutorial2.add_object("flame", 3, 1)  # Flame on floor
        tutorial2.set_requirement("require_all_flames_extinguished", True)
        tutorial2.optimal_moves = 6
        tutorial2.optimal_time = 12.0
        
        # Basic Level 1: Simple puzzle
        basic1 = Level("basic_1", "Ice Bridge", 15, 10)
        basic1.description = "Create an ice bridge to reach the flame"
        basic1.difficulty = "easy"
        basic1.add_player_start(2, 1)
        basic1.add_object("wall", 0, 0)  # Floor
        
        # Left platform
        for x in range(0, 5):
            basic1.add_object("wall", x, 3)
        
        # Right platform with flame
        for x in range(10, 15):
            basic1.add_object("wall", x, 1)
        
        basic1.add_object("flame", 13, 1)
        basic1.set_requirement("require_all_flames_extinguished", True)
        basic1.optimal_moves = 10
        basic1.optimal_time = 25.0
        
        # Basic Level 2: Pushing puzzle
        basic2 = Level("basic_2", "Stone Pusher", 15, 10)
        basic2.description = "Use stone to help reach higher platforms"
        basic2.difficulty = "easy"
        basic2.add_player_start(2, 1)
        basic2.add_object("wall", 0, 0)  # Floor
        
        # Left platforms
        for x in range(0, 4):
            basic2.add_object("wall", x, 3)
        
        for x in range(8, 11):
            basic2.add_object("wall", x, 4)
        
        # Stone to push
        basic2.add_object("stone", 6, 1)
        
        # Right platform with flames
        for x in range(12, 15):
            basic2.add_object("wall", x, 2)
        
        basic2.add_object("flame", 12, 2)
        basic2.add_object("flame", 14, 2)
        basic2.set_requirement("require_all_flames_extinguished", True)
        basic2.optimal_moves = 15
        basic2.optimal_time = 35.0
        
        # Medium Level 1: Portal puzzle
        medium1 = Level("medium_1", "Portal Maze", 20, 12)
        medium1.description = "Use portals to navigate and extinguish all flames"
        medium1.difficulty = "medium"
        medium1.add_player_start(2, 1)
        medium1.add_object("wall", 0, 0)  # Floor
        
        # Complex platform structure
        for x in range(0, 3):
            medium1.add_object("wall", x, 4)
        
        for x in range(7, 10):
            medium1.add_object("wall", x, 6)
        
        for x in range(13, 17):
            medium1.add_object("wall", x, 8)
        
        # Flames in different areas
        medium1.add_object("flame", 2, 5)
        medium1.add_object("flame", 8, 2)
        medium1.add_object("flame", 15, 9)
        
        # Portals connecting areas
        from src.entities.objects.portal import Portal
        portal1, portal2 = Portal.create_portal_pair(4, 1, 9, 10, "portal_1")
        portal3, portal4 = Portal.create_portal_pair(11, 1, 16, 9, "portal_2")
        
        medium1.add_object("wall", 4, 1)  # Portal covers
        medium1.add_object("wall", 9, 10)  # Portal covers
        medium1.add_object("wall", 11, 1)  # Portal covers
        medium1.add_object("wall", 16, 9)  # Portal covers
        
        medium1.set_requirement("require_all_flames_extinguished", True)
        medium1.optimal_moves = 20
        medium1.optimal_time = 60.0
        
        # Add all levels
        self.levels[tutorial1.level_id] = tutorial1
        self.levels[tutorial2.level_id] = tutorial2
        self.levels[basic1.level_id] = basic1
        self.levels[basic2.level_id] = basic2
        self.levels[medium1.level_id] = medium1
        
        # Initialize unlocked levels
        self.unlocked_levels = list(self.levels.keys())
    
    def _load_custom_levels(self):
        """Load custom levels from TOML files"""
        custom_files = discover_custom_levels("levels")
        
        for filepath in custom_files:
            level_data = load_toml_level(filepath)
            if level_data:
                # Create Level object from loaded data
                level = Level.from_dict(level_data)
                self.levels[level.level_id] = level
                self.unlocked_levels.append(level.level_id)
                print(f"Loaded custom level: {level.name} from {filepath}")
    
    def load_level(self, level_id: str) -> bool:
        """Load a level by ID"""
        if level_id not in self.levels:
            print(f"Level {level_id} not found!")
            return False
        
        if level_id not in self.unlocked_levels:
            print(f"Level {level_id} is locked!")
            return False
        
        # Clear current world
        self.game_world.clear()
        self.ice_system.reset()
        self.rules.reset_level()
        
        # Set current level
        self.current_level = self.levels[level_id]
        self.current_level_id = level_id
        
        # Load level data
        level_data = self.current_level
        self._create_level_objects(level_data)
        self._create_player(level_data)
        self._set_level_requirements(level_data)
        
        print(f"Loaded level: {level_data.name}")
        return True
    
    def _create_level_objects(self, level: Level):
        """Create objects for level"""
        # Create floor if not specified
        has_floor = any(obj['y'] == 0 for obj in level.objects)
        if not has_floor:
            for x in range(level.width):
                wall = Wall(x, 0)
                self.game_world.add_object(wall, x, 0)
        
        # Create level objects
        for obj_data in level.objects:
            obj = self._create_object_from_data(obj_data)
            if obj:
                self.game_world.add_object(obj, obj.grid_x, obj.grid_y)
    
    def _create_object_from_data(self, obj_data: Dict[str, Any]) -> Optional[GameObject]:
        """Create object from data"""
        obj_type = obj_data['type']
        x = obj_data['x']
        y = obj_data['y']
        properties = obj_data.get('properties', {})
        
        if obj_type == "wall":
            return Wall(x, y)
        elif obj_type == "flame":
            return Flame(x, y)
        elif obj_type == "stone":
            return Stone(x, y)
        elif obj_type == "ice_pot":
            is_hot = properties.get('is_hot', False)
            return Pot(x, y, is_hot)
        elif obj_type == "ice_block":
            return IceBlock(x, y)
        elif obj_type == "portal":
            portal_id = properties.get('portal_id', 'default')
            return Portal(x, y, portal_id)
        
        return None
    
    def _create_player(self, level: Level):
        """Create player for level"""
        player = Player(level.player_start[0], level.player_start[1])
        self.game_world.add_object(player, player.grid_x, player.grid_y)
        
        # Set player reference in rules system
        # Note: Player reference is passed to rules system during level loading
        # (GameRulesSystem gets player reference via level objects)
        pass
    
    def _set_level_requirements(self, level: Level):
        """Set level requirements in rules system"""
        self.rules.set_level_requirements(**level.requirements)
    
    def get_available_levels(self) -> List[Dict[str, Any]]:
        """Get list of available levels"""
        levels = []
        
        for level_id, level in self.levels.items():
            is_unlocked = level_id in self.unlocked_levels
            is_completed = level_id in self.completed_levels
            score = self.level_scores.get(level_id, {})
            
            levels.append({
                'level_id': level_id,
                'name': level.name,
                'description': level.description,
                'difficulty': level.difficulty,
                'is_unlocked': is_unlocked,
                'is_completed': is_completed,
                'best_moves': score.get('moves', 0),
                'best_time': score.get('time', 0),
                'optimal_moves': level.optimal_moves,
                'optimal_time': level.optimal_time
            })
        
        return sorted(levels, key=lambda x: (x['level_id']))
    
    def complete_level(self):
        """Mark current level as completed"""
        if self.current_level_id:
            if self.current_level_id not in self.completed_levels:
                self.completed_levels.append(self.current_level_id)
            
            # Save score
            status = self.rules.get_level_status()
            score = {
                'moves': status['moves_taken'],
                'time': status['time_elapsed'],
                'puzzles_solved': len(status['puzzles_solved']),
                'completion_date': self._get_current_timestamp()
            }
            
            self.level_scores[self.current_level_id] = score
            
            # Unlock next levels
            self._unlock_next_levels()
            
            print(f"Level {self.current_level.name} completed!")
    
    def _unlock_next_levels(self):
        """Unlock next levels based on progression"""
        if not self.current_level_id:
            return
        
        # Tutorial unlocks basic levels
        if self.current_level_id.startswith('tutorial_'):
            basic_levels = [k for k in self.levels.keys() if k.startswith('basic_')]
            for level_id in basic_levels[:2]:  # Unlock first 2 basic levels
                if level_id not in self.unlocked_levels:
                    self.unlocked_levels.append(level_id)
                    print(f"Unlocked level: {level_id}")
        
        # Basic levels unlock medium levels
        elif self.current_level_id.startswith('basic_'):
            medium_levels = [k for k in self.levels.keys() if k.startswith('medium_')]
            for level_id in medium_levels:
                if level_id not in self.unlocked_levels:
                    self.unlocked_levels.append(level_id)
                    print(f"Unlocked level: {level_id}")
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def restart_current_level(self):
        """Restart current level"""
        if self.current_level_id:
            self.load_level(self.current_level_id)
    
    def get_level_info(self, level_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific level"""
        if level_id not in self.levels:
            return None
        
        level = self.levels[level_id]
        is_unlocked = level_id in self.unlocked_levels
        is_completed = level_id in self.completed_levels
        score = self.level_scores.get(level_id, {})
        
        return {
            'level': level.to_dict(),
            'is_unlocked': is_unlocked,
            'is_completed': is_completed,
            'score': score
        }
    
    def save_progress(self, filename: str = "icer_save.json"):
        """Save game progress to file"""
        save_data = {
            'unlocked_levels': self.unlocked_levels,
            'completed_levels': self.completed_levels,
            'level_scores': self.level_scores,
            'last_played_level': self.current_level_id,
            'save_date': self._get_current_timestamp()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            print(f"Progress saved to {filename}")
        except Exception as e:
            print(f"Failed to save progress: {e}")
    
    def load_progress(self, filename: str = "icer_save.json"):
        """Load game progress from file"""
        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
                
            self.unlocked_levels = save_data.get('unlocked_levels', [])
            self.completed_levels = save_data.get('completed_levels', [])
            self.level_scores = save_data.get('level_scores', {})
            
            print(f"Progress loaded from {filename}")
            return True
        except FileNotFoundError:
            print("No save file found, starting fresh")
            return True
        except Exception as e:
            print(f"Failed to load progress: {e}")
            return False
    
    def export_levels(self, filename: str = "icer_levels.json"):
        """Export all levels to JSON file"""
        levels_data = {
            'levels': [level.to_dict() for level in self.levels.values()],
            'export_date': self._get_current_timestamp(),
            'version': '1.0'
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(levels_data, f, indent=2)
            print(f"Levels exported to {filename}")
        except Exception as e:
            print(f"Failed to export levels: {e}")