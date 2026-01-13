# ICER Level Editor

import sys
import pygame
import toml
import os
from typing import List, Tuple, Optional, Dict
from datetime import datetime

# Add current directory to path
sys.path.insert(0, '.')

from src.game.constants import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT
from src.game.constants import COLOR_PLAYER, COLOR_WALL, COLOR_ICE_BLOCK, COLOR_FLAME, COLOR_STONE, COLOR_ICE_POT, COLOR_HOT_POT, COLOR_PORTAL

# Object character mappings
OBJECT_CHARS = {
    '.': 'empty',
    'P': 'player', 
    'W': 'wall',
    'S': 'stone',
    'F': 'flame',
    'I': 'ice_block',
    'C': 'cold_pot',
    'H': 'hot_pot',
    '1': 'portal_1',
    '2': 'portal_2',
    '3': 'portal_3'
}

CHAR_COLORS = {
    '.': (50, 50, 50),
    'P': COLOR_PLAYER,
    'W': COLOR_WALL,
    'S': COLOR_STONE,
    'F': COLOR_FLAME,
    'I': COLOR_ICE_BLOCK,
    'C': COLOR_ICE_POT,
    'H': COLOR_HOT_POT,
    '1': COLOR_PORTAL,
    '2': COLOR_PORTAL,
    '3': COLOR_PORTAL
}


class LevelEditor:
    """Simple text-based level editor for ICER"""
    
    def __init__(self):
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH + 300, WINDOW_HEIGHT))
        pygame.display.set_caption("ICER Level Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 36)
        
        # Editor state
        self.running = True
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.current_char = 'W'  # Current object to place
        self.grid = [['.' for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Metadata
        self.level_id = f"custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.level_name = "Custom Level"
        self.author = "Level Editor"
        self.description = "A custom created level"
        self.difficulty = "medium"
        self.optimal_moves = 20
        self.optimal_time = 60.0
        
        # UI state
        self.show_help = True
        self.message = "Welcome to ICER Level Editor!"
        self.message_timer = 0
        
        # Editing state
        self.player_placed = False
        
    def save_level(self, filename: Optional[str] = None) -> bool:
        """Save level to TOML file"""
        if not filename:
            filename = f"levels/{self.level_id}.toml"
        
        # Validate level has player
        has_player = any('P' in row for row in self.grid)
        if not has_player:
            self.show_message("ERROR: Must place player (P) somewhere!")
            return False
        
        # Create level data
        level_data = {
            'level_metadata': {
                'id': self.level_id,
                'name': self.level_name,
                'difficulty': self.difficulty,
                'author': self.author,
                'description': self.description,
                'optimal_moves': self.optimal_moves,
                'optimal_time': self.optimal_time
            },
            'level_layout': {
                'grid': [''.join(row) for row in self.grid]
            }
        }
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                toml.dump(level_data, f)
            self.show_message(f"Level saved to {filename}")
            return True
        except Exception as e:
            self.show_message(f"ERROR: Failed to save: {e}")
            return False
    
    def load_level(self, filename: str) -> bool:
        """Load level from TOML file"""
        try:
            with open(filename, 'r') as f:
                level_data = toml.load(f)
            
            # Load metadata
            metadata = level_data.get('level_metadata', {})
            self.level_id = metadata.get('id', 'custom_level')
            self.level_name = metadata.get('name', 'Custom Level')
            self.difficulty = metadata.get('difficulty', 'medium')
            self.author = metadata.get('author', 'Level Editor')
            self.description = metadata.get('description', 'A custom created level')
            self.optimal_moves = metadata.get('optimal_moves', 20)
            self.optimal_time = metadata.get('optimal_time', 60.0)
            
            # Load grid
            layout = level_data.get('level_layout', {})
            grid_strings = layout.get('grid', [])
            
            self.grid = []
            for row_str in grid_strings[:self.grid_height]:
                row = list(row_str[:self.grid_width])
                # Pad row if needed
                while len(row) < self.grid_width:
                    row.append('.')
                self.grid.append(row)
            
            # Fill remaining rows with empty cells
            while len(self.grid) < self.grid_height:
                self.grid.append(['.' for _ in range(self.grid_width)])
            
            self.player_placed = any('P' in row for row in self.grid)
            self.show_message(f"Level loaded from {filename}")
            return True
            
        except Exception as e:
            self.show_message(f"ERROR: Failed to load: {e}")
            return False
    
    def show_message(self, message: str):
        """Show a temporary message"""
        self.message = message
        self.message_timer = 3.0
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos, event.button)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button held
                    self.handle_mouse_click(event.pos, 1)  # Simulate left click
    
    def handle_keydown(self, key):
        """Handle keyboard input"""
        # Object selection
        if key == pygame.K_1:
            self.current_char = 'W'
            self.show_message("Wall (W)")
        elif key == pygame.K_2:
            self.current_char = 'S'
            self.show_message("Stone (S)")
        elif key == pygame.K_3:
            self.current_char = 'I'
            self.show_message("Ice Block (I)")
        elif key == pygame.K_4:
            self.current_char = 'F'
            self.show_message("Flame (F)")
        elif key == pygame.K_5:
            self.current_char = 'C'
            self.show_message("Cold Pot (C)")
        elif key == pygame.K_6:
            self.current_char = 'H'
            self.show_message("Hot Pot (H)")
        elif key == pygame.K_7:
            self.current_char = '1'
            self.show_message("Portal 1")
        elif key == pygame.K_8:
            self.current_char = '2'
            self.show_message("Portal 2")
        elif key == pygame.K_9:
            self.current_char = '3'
            self.show_message("Portal 3")
        elif key == pygame.K_0:
            self.current_char = 'P'
            self.show_message("Player (P)")
        elif key == pygame.K_SPACE:
            self.current_char = '.'
            self.show_message("Eraser")
        
        # File operations
        elif key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_level()
        elif key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.open_file_dialog()
        elif key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.clear_grid()
        
        # Toggle help
        elif key == pygame.K_F1:
            self.show_help = not self.show_help
        
        # Clear grid
        elif key == pygame.K_DELETE:
            self.clear_grid()
    
    def handle_mouse_click(self, pos, button):
        """Handle mouse clicks on grid"""
        x, y = pos
        
        # Check if click is on grid
        if x < WINDOW_WIDTH and y < WINDOW_HEIGHT:
            grid_x = x // CELL_SIZE
            grid_y = y // CELL_SIZE
            
            if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
                if button == 1:  # Left click - place
                    self.place_object(grid_x, grid_y)
                elif button == 3:  # Right click - erase
                    self.place_object(grid_x, grid_y, erase=True)
    
    def place_object(self, x: int, y: int, erase: bool = False):
        """Place or erase object at grid position"""
        if erase:
            char = '.'
        else:
            char = self.current_char
        
        # Handle player placement
        if char == 'P':
            # Remove existing player
            for gy in range(self.grid_height):
                for gx in range(self.grid_width):
                    if self.grid[gy][gx] == 'P':
                        self.grid[gy][gx] = '.'
        
        # Place the object
        self.grid[y][x] = char
    
    def clear_grid(self):
        """Clear the entire grid"""
        self.grid = [['.' for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        self.player_placed = False
        self.show_message("Grid cleared")
    
    def open_file_dialog(self):
        """Simple file dialog - loads from levels/ directory"""
        levels_dir = "levels"
        if os.path.exists(levels_dir):
            toml_files = [f for f in os.listdir(levels_dir) if f.endswith('.toml')]
            if toml_files:
                # Load the first TOML file for now
                filename = os.path.join(levels_dir, toml_files[0])
                self.load_level(filename)
            else:
                self.show_message("No level files found in levels/ directory")
        else:
            self.show_message("levels/ directory not found")
    
    def update(self, dt: float):
        """Update editor state"""
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
    
    def render(self):
        """Render the editor"""
        self.screen.fill((30, 30, 40))
        
        # Render grid
        self.render_grid()
        
        # Render UI panel
        self.render_ui_panel()
        
        # Render message
        if self.message_timer > 0:
            self.render_message()
        
        pygame.display.flip()
    
    def render_grid(self):
        """Render the level grid"""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                char = self.grid[y][x]
                color = CHAR_COLORS.get(char, (100, 100, 100))
                
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                # Fill cell
                pygame.draw.rect(self.screen, color, rect)
                
                # Draw border
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
                
                # Draw character in center
                if char != '.':
                    text = self.small_font.render(char, True, (255, 255, 255))
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)
    
    def render_ui_panel(self):
        """Render the UI panel on the right side"""
        panel_x = WINDOW_WIDTH
        panel_width = 300
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x, 0, panel_width, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, (40, 40, 50), panel_rect)
        
        # Title
        title_text = self.title_font.render("LEVEL EDITOR", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, 30))
        self.screen.blit(title_text, title_rect)
        
        # Current object
        y_offset = 70
        current_text = self.font.render(f"Current: {self.current_char}", True, (255, 255, 255))
        self.screen.blit(current_text, (panel_x + 10, y_offset))
        
        # Draw current object preview
        preview_rect = pygame.Rect(panel_x + 200, y_offset - 5, 30, 30)
        pygame.draw.rect(self.screen, CHAR_COLORS.get(self.current_char, (100, 100, 100)), preview_rect)
        
        # Object shortcuts
        y_offset += 50
        shortcuts_text = self.small_font.render("SHORTCUTS:", True, (200, 200, 200))
        self.screen.blit(shortcuts_text, (panel_x + 10, y_offset))
        
        shortcuts = [
            "1-9: Objects", "0: Player", "Space: Eraser",
            "Click: Place", "Right Click: Erase",
            "Ctrl+S: Save", "Ctrl+O: Open", "Del: Clear",
            "F1: Toggle Help"
        ]
        
        y_offset += 25
        for shortcut in shortcuts:
            text = self.small_font.render(shortcut, True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 10, y_offset))
            y_offset += 20
        
        # Object legend
        y_offset += 20
        legend_text = self.small_font.render("OBJECTS:", True, (200, 200, 200))
        self.screen.blit(legend_text, (panel_x + 10, y_offset))
        
        y_offset += 25
        for char, description in [
            ('.', 'Empty'), ('P', 'Player'), ('W', 'Wall'),
            ('S', 'Stone'), ('I', 'Ice Block'), ('F', 'Flame'),
            ('C', 'Cold Pot'), ('H', 'Hot Pot'),
            ('1-3', 'Portal Pairs')
        ]:
            # Draw color box
            color_rect = pygame.Rect(panel_x + 10, y_offset - 2, 15, 15)
            pygame.draw.rect(self.screen, CHAR_COLORS.get(char, (100, 100, 100)), color_rect)
            
            # Draw text
            text = self.small_font.render(f"{char}: {description}", True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 35, y_offset))
            
            y_offset += 18
        
        # Level metadata
        y_offset += 20
        metadata_text = self.small_font.render("METADATA:", True, (200, 200, 200))
        self.screen.blit(metadata_text, (panel_x + 10, y_offset))
        
        y_offset += 25
        metadata = [
            f"ID: {self.level_id[:15]}...",
            f"Name: {self.level_name[:15]}...",
            f"Author: {self.author[:15]}..."
        ]
        
        for meta in metadata:
            text = self.small_font.render(meta, True, (180, 180, 180))
            self.screen.blit(text, (panel_x + 10, y_offset))
            y_offset += 18
    
    def render_message(self):
        """Render temporary message"""
        if self.message_timer > 0:
            text = self.font.render(self.message, True, (255, 255, 100))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            
            # Draw background
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (60, 60, 40), bg_rect)
            pygame.draw.rect(self.screen, (100, 100, 80), bg_rect, 2)
            
            # Draw text
            self.screen.blit(text, text_rect)
    
    def run(self):
        """Main editor loop"""
        print("=== ICER Level Editor ===")
        print("Use number keys 1-9 to select objects")
        print("0 for player, SPACE for eraser")
        print("Click to place, right-click to erase")
        print("Ctrl+S to save, Ctrl+O to load")
        print("===========================")
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()


def main():
    """Main entry point"""
    editor = LevelEditor()
    editor.run()


if __name__ == "__main__":
    main()