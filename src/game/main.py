# Main Game Class

import sys
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, '.')

try:
    import pygame
    PYGAME_AVAILABLE = True
    print("Pygame available, version:", pygame.version.ver)
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: Pygame not installed. Install with: pip install pygame")

from src.game.constants import *
from src.game.game_state import GameStateManager, GameState
from src.input.input_handler import InputHandler
from src.utils.vector2 import Vector2
from src.world.game_world import GameWorld
from src.entities.player import Player
from src.entities.objects.wall import Wall
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.flame import Flame
from src.entities.objects.stone import Stone
from src.entities.objects.pot import Pot
from src.entities.objects.portal import Portal
from src.physics.ice_system import IceBlockSystem
from src.physics.physics_engine import PhysicsEngine
from src.physics.push_system import PushSystem
from src.rules.game_rules import GameRulesSystem
from src.levels.level_manager import LevelManager
from src.rendering.ui_effects import UIEffects


class Game:
    """Main game class that manages the game loop"""
    
    def __init__(self):
        # Check pygame availability
        if not PYGAME_AVAILABLE:
            print("Error: Pygame is required to run this game.")
            print("Please install it with: pip install pygame")
            sys.exit(1)
        
        # Initialize Pygame
        pygame.init()
        
        # Setup display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ICER - Ice Block Puzzle Game")
        
        # Setup timing
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0  # Delta time in seconds
        
        # Initialize subsystems
        self.state_manager = GameStateManager()
        self.input_handler = InputHandler()
        self.game_world = GameWorld()
        self.player: Optional[Player] = None
        self.ice_system = IceBlockSystem()
        self.physics_engine = PhysicsEngine(self.game_world)
        self.push_system = PushSystem(self.game_world, self.physics_engine)
        self.game_rules = GameRulesSystem(self.game_world, self.physics_engine, self.ice_system)
        self.level_manager = LevelManager(self.game_world, self.game_rules, self.physics_engine, self.ice_system)
        
        # Initialize UI effects (after screen is created)
        self.ui_effects: Optional[UIEffects] = None
        
        # Setup input callbacks
        self._setup_input_callbacks()
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize UI effects after screen is ready
        self.ui_effects = UIEffects(self.screen)
    
    def _setup_input_callbacks(self):
        """Setup input callback functions"""
        self.input_handler.bind_action_callback('pause', self._toggle_pause)
        self.input_handler.bind_action_callback('menu', self._toggle_menu)
        self.input_handler.bind_action_callback('restart', self._restart_level)
    
    def _toggle_pause(self):
        """Toggle pause state"""
        if self.state_manager.is_state(GameState.PLAYING):
            self.state_manager.change_state(GameState.PAUSED)
        elif self.state_manager.is_state(GameState.PAUSED):
            self.state_manager.change_state(GameState.PLAYING)
    
    def _toggle_menu(self):
        """Toggle menu state"""
        if self.state_manager.is_state(GameState.PLAYING):
            self.state_manager.change_state(GameState.MENU)
        elif self.state_manager.is_state(GameState.MENU):
            self.state_manager.change_state(GameState.PLAYING)
    
    def _restart_level(self):
        """Restart current level"""
        if self.state_manager.is_state(GameState.PLAYING):
            self.state_manager.game_data.reset_level_data()
            self._initialize_level()
            print("Level restarted!")
    
    def _initialize_level(self):
        """Initialize test level"""
        # Clear world and systems
        self.game_world.clear()
        self.ice_system.reset()
        
        # Create player
        self.player = Player(GRID_WIDTH // 2, 1)
        self.game_world.add_object(self.player, self.player.grid_x, self.player.grid_y)
        
        # Initialize level with tutorial 1
        self.level_manager.load_level("tutorial_1")
    
    def _create_test_level(self):
        """Create a simple test level"""
        # Create floor
        for x in range(15):
            self.game_world.add_object(Wall(x, 0), x, 0)
        
        # Add some platforms
        for x in range(3, 7):
            self.game_world.add_object(Wall(x, 2), x, 2)
        
        # Add a single flame to extinguish
        self.game_world.add_object(Flame(6, 3), 6, 3)
        
        # Add some walls for jumping practice
        self.game_world.add_object(Wall(8, 1), 8, 1)
        self.game_world.add_object(Wall(9, 1), 9, 1)
        
        # Add flames to extinguish (main objective)
        self.game_world.add_object(Flame(3, 1), 3, 1)
        self.game_world.add_object(Flame(15, 2), 15, 2)
        self.game_world.add_object(Flame(10, 3), 10, 3)
        
        # Add ice pot (can be ignited)
        self.game_world.add_object(Pot(5, 1, False), 5, 1)
        
        # Add hot pot (already burning)
        self.game_world.add_object(Pot(12, 1, True), 12, 1)
        
        # Add stones for physics puzzles
        self.game_world.add_object(Stone(2, 2), 2, 2)
        self.game_world.add_object(Stone(14, 1), 14, 1)
        
        # Add some platforms
        for x in range(6, 11):
            self.game_world.add_object(Wall(x, 2), x, 2)
        
        # Add portals for transportation
        portal1, portal2 = Portal.create_portal_pair(2, 5, 17, 4, "test_portal")
        self.game_world.add_object(portal1, portal1.grid_x, portal1.grid_y)
        self.game_world.add_object(portal2, portal2.grid_x, portal2.grid_y)
        
        # Add higher platforms
        for x in range(15, 19):
            self.game_world.add_object(Wall(x, 4), x, 4)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.running = False  # Alt+F4 to quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
    
    def _handle_mouse_click(self, pos):
        """Handle mouse click events"""
        # TODO: Implement mouse interaction
        pass
    
    def update(self, dt: float):
        """Update game logic"""
        # Update input handler
        self.input_handler.update()
        
        # Update based on current state
        if self.state_manager.is_state(GameState.PLAYING):
            self._update_gameplay(dt)
        elif self.state_manager.is_state(GameState.MENU):
            self._update_menu(dt)
        elif self.state_manager.is_state(GameState.PAUSED):
            self._update_paused(dt)
        elif self.state_manager.is_state(GameState.WIN):
            self._update_win(dt)
        elif self.state_manager.is_state(GameState.LOSE):
            self._update_lose(dt)
    
    def _update_menu(self, dt: float):
        """Update menu logic"""
        # Handle input for level selection
        keys = pygame.key.get_pressed()
        
        # Get available levels
        available_levels = self.level_manager.get_available_levels()
        
        # Start first available level with SPACE
        if keys[pygame.K_SPACE]:
            first_unlocked = next((l for l in available_levels if l['is_unlocked']), None)
            if first_unlocked:
                self.level_manager.load_level(first_unlocked['level_id'])
                self.state_manager.game_data.reset_level_data()
                self.state_manager.change_state(GameState.PLAYING)
        
        # Quick level selection with number keys
        for i in range(6):
            if i < len(available_levels) and available_levels[i]['is_unlocked']:
                if keys[pygame.K_1 + i]:
                    self.level_manager.load_level(available_levels[i]['level_id'])
                    self.state_manager.game_data.reset_level_data()
                    self.state_manager.change_state(GameState.PLAYING)
    
    def _update_paused(self, dt: float):
        """Update paused logic"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state_manager.change_state(GameState.PLAYING)
    
    def _update_win(self, dt: float):
        """Update win screen logic"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Mark level as completed
            self.level_manager.complete_level()
            self.state_manager.change_state(GameState.MENU)
        elif keys[pygame.K_r]:
            # Restart level
            self._initialize_level()
            self.state_manager.change_state(GameState.PLAYING)
        
        # Quick level selection
        available_levels = self.level_manager.get_available_levels()
        for i in range(6):
            if i < len(available_levels) and available_levels[i]['is_unlocked']:
                if keys[pygame.K_1 + i]:
                    self.level_manager.load_level(available_levels[i]['level_id'])
                    self.state_manager.game_data.reset_level_data()
                    self.state_manager.change_state(GameState.PLAYING)
    
    def _update_lose(self, dt: float):
        """Update lose screen logic"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self._initialize_level()
            self.state_manager.change_state(GameState.PLAYING)
        elif keys[pygame.K_ESCAPE]:
            self.state_manager.change_state(GameState.MENU)
    
    def _update_gameplay(self, dt: float):
        """Update gameplay logic"""
        # Update game time
        self.state_manager.game_data.time_elapsed += dt
        
        # Set current time for objects
        if self.player:
            self.player.set_property('current_time', self.state_manager.game_data.time_elapsed)
        
        # Update game world and all objects
        self.game_world.update(dt)
        
        # Update physics systems
        self.physics_engine.update(dt)
        self.ice_system.update_all_ice_blocks(dt, self.game_world)
        self.push_system.process_push_requests()
        
        # Update game rules
        self.game_rules.update(dt)
        
        # Handle player input
        self._handle_player_input(dt)
        
        # Update game rules
        self.game_rules.update(dt)
        
        # Handle player input
        self._handle_player_input(dt)
        self._check_win_conditions()
    
    def render(self):
        """Main render method"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Render based on current state
        if self.state_manager.is_state(GameState.PLAYING):
            self._render_gameplay()
        elif self.state_manager.is_state(GameState.MENU):
            self._render_menu()
        elif self.state_manager.is_state(GameState.PAUSED):
            self._render_gameplay()
            self._render_paused_overlay()
        elif self.state_manager.is_state(GameState.WIN):
            self._render_win()
        elif self.state_manager.is_state(GameState.LOSE):
            self._render_lose()
        
        # Update display
        pygame.display.flip()
    
    def _render_gameplay(self):
        """Render gameplay screen"""
        # Render grid
        self._render_grid()
        
        # Render game objects
        self._render_game_objects()
        
        # Render UI
        self._render_ui()
    
    def _render_grid(self):
        """Render grid lines"""
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (x * CELL_SIZE, 0), 
                           (x * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(self.screen, GRAY, 
                           (0, y * CELL_SIZE), 
                           (GRID_WIDTH * CELL_SIZE, y * CELL_SIZE))
    
    def _render_game_objects(self):
        """Render all game objects"""
        for x, y, obj in self.game_world.grid:
            if obj is not None:
                self._render_object(obj, x, y)
    
    def _render_object(self, obj, x: int, y: int):
        """Render a single object"""
        color = obj.get_color()
        screen_x = x * CELL_SIZE + 5
        screen_y = (GRID_HEIGHT - y - 1) * CELL_SIZE + 5
        
        # Apply animation offset for player
        offset_x, offset_y = 0, 0
        if obj.get_type() == "player":
            current_time = self.state_manager.game_data.time_elapsed
            obj.set_property('current_time', current_time)
            offset_x, offset_y = obj.get_render_offset(current_time)
        
        pygame.draw.rect(self.screen, color,
                        (screen_x + offset_x, screen_y + offset_y, 
                         CELL_SIZE - 10, CELL_SIZE - 10))
        
        # Render UI effects after objects
        if self.ui_effects:
            self.ui_effects.update(self.dt)
    
    def _render_ui(self):
        """Render UI elements"""
        # Draw UI panel background
        ui_panel = pygame.Surface((250, 100))
        ui_panel.set_alpha(200)
        ui_panel.fill((40, 40, 40))
        self.screen.blit(ui_panel, (10, 10))
        
        # Draw level info
        level_name = "Tutorial 1" if self.level_manager.current_level else "Unknown"
        level_text = self.small_font.render(f"Level: {level_name}", True, WHITE)
        self.screen.blit(level_text, (20, 20))
        
        # Draw moves counter
        moves_text = self.small_font.render(f"Moves: {self.state_manager.game_data.moves}", 
                                           True, WHITE)
        self.screen.blit(moves_text, (20, 45))
        
        # Draw timer
        time_text = self.small_font.render(f"Time: {self.state_manager.game_data.time_elapsed:.1f}s", 
                                          True, WHITE)
        self.screen.blit(time_text, (20, 70))
        
        # Draw flame counter
        from src.entities.objects.flame import Flame
        flame_count = self.game_world.count_objects_of_type(Flame)
        flame_text = self.small_font.render(f"Flames: {flame_count}", True, COLOR_FLAME)
        self.screen.blit(flame_text, (150, 45))
        
        # Draw objectives hint
        if flame_count > 0:
            hint_text = self.small_font.render("Extinguish all flames!", True, (200, 200, 200))
            self.screen.blit(hint_text, (150, 70))
    
    def _render_menu(self):
        """Render menu"""
        # Draw background gradient
        for i in range(WINDOW_HEIGHT):
            color_value = int(20 + (40 * i / WINDOW_HEIGHT))
            pygame.draw.line(self.screen, (color_value, color_value, color_value + 10), 
                           (0, i), (WINDOW_WIDTH, i))
        
        # Draw title with shadow
        shadow_text = self.font.render("ICER", True, (20, 20, 20))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 153))
        self.screen.blit(shadow_text, shadow_rect)
        
        title_text = self.font.render("ICER", True, COLOR_PLAYER)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.small_font.render("Ice Block Puzzle Game", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Draw level selection
        available_levels = self.level_manager.get_available_levels()
        y_offset = 280
        
        # Section header
        header_text = self.small_font.render("SELECT LEVEL:", True, (200, 200, 200))
        header_rect = header_text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
        self.screen.blit(header_text, header_rect)
        y_offset += 40
        
        # Draw level options (show first 6 levels)
        for i, level in enumerate(available_levels[:6]):
            if not level['is_unlocked']:
                continue
                
            # Determine color based on completion
            if level['is_completed']:
                color = GREEN
                status = "✓ "
            else:
                color = WHITE
                status = "→ "
            
            level_text = f"{status}{level['name']} ({level['difficulty']})"
            if level['best_moves'] > 0:
                level_text += f" - Best: {level['best_moves']} moves"
            
            text = self.small_font.render(level_text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            
            # Highlight if this is the current level
            if level['level_id'] == self.level_manager.current_level_id:
                pygame.draw.rect(self.screen, color, text_rect.inflate(20, 10), 2)
            
            self.screen.blit(text, text_rect)
            y_offset += 35
        
        # Draw controls
        y_offset = WINDOW_HEIGHT - 180
        controls = [
            "SPACE: Start selected level",
            "1-6: Quick select level", 
            "J/L or Arrows: Move",
            "A/D: Create/Remove ice",
            "ESC: Pause  |  R: Restart"
        ]
        
        for control in controls:
            text = self.small_font.render(control, True, (180, 180, 180))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def _render_paused_overlay(self):
        """Render pause overlay"""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Draw instruction
        resume_text = self.small_font.render("Press ESC to resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(resume_text, resume_rect)
    
    def _render_win(self):
        """Render win screen"""
        # Draw celebration background
        for i in range(0, WINDOW_HEIGHT, 20):
            r = min(255, int(20 + 10 * (i % 40)))
            g = min(255, int(40 + 5 * (i % 20)))
            b = min(255, int(20 + 15 * (i % 30)))
            color = (r, g, b)
            pygame.draw.rect(self.screen, color, (0, i, WINDOW_WIDTH, 20))
        
        # Draw celebration text with animation effect
        pulse = abs(int(self.state_manager.game_data.time_elapsed * 3) % 2)
        scale = 1.0 + pulse * 0.1
        
        # Create bigger font for celebration
        big_font = pygame.font.Font(None, int(72 * scale))
        
        win_text = big_font.render("🎉 LEVEL COMPLETE! 🎉", True, GREEN)
        win_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        self.screen.blit(win_text, win_rect)
        
        # Draw level name if available
        if self.level_manager.current_level:
            level_name_text = self.font.render(self.level_manager.current_level.name, True, WHITE)
            level_name_rect = level_name_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(level_name_text, level_name_rect)
        
        # Draw stats in panels
        stats_y = WINDOW_HEIGHT // 2 + 40
        
        # Stats panel
        stats_panel = pygame.Surface((400, 120))
        stats_panel.set_alpha(180)
        stats_panel.fill((30, 30, 40))
        self.screen.blit(stats_panel, (WINDOW_WIDTH // 2 - 200, stats_y))
        
        # Performance stats
        stats = [
            (f"Moves: {self.state_manager.game_data.moves}", WHITE),
            (f"Time: {self.state_manager.game_data.time_elapsed:.1f}s", WHITE),
            (f"Efficiency: {self._calculate_score():.0f}%", (100, 255, 100) if self._calculate_score() >= 80 else (255, 255, 100))
        ]
        
        for i, (stat_text, color) in enumerate(stats):
            text = self.small_font.render(stat_text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, stats_y + 25 + i * 30))
            self.screen.blit(text, text_rect)
        
        # Draw options
        options_y = stats_y + 140
        options = [
            ("SPACE: Continue to menu", WHITE),
            ("R: Replay level", (200, 200, 200)),
            ("1-6: Select another level", (200, 200, 200))
        ]
        
        for i, (option_text, color) in enumerate(options):
            text = self.small_font.render(option_text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, options_y + i * 25))
            self.screen.blit(text, text_rect)
    
    def _calculate_score(self) -> float:
        """Calculate efficiency score based on optimal performance"""
        if not self.level_manager.current_level:
            return 100.0
        
        current_moves = self.state_manager.game_data.moves
        current_time = self.state_manager.game_data.time_elapsed
        
        optimal_moves = self.level_manager.current_level.optimal_moves
        optimal_time = self.level_manager.current_level.optimal_time
        
        if not optimal_moves or not optimal_time:
            return 100.0
        
        # Calculate score based on both moves and time
        move_score = max(0, 100 - (current_moves - optimal_moves) * 5)
        time_score = max(0, 100 - (current_time - optimal_time) * 2)
        
        return (move_score + time_score) / 2
    
    def _render_lose(self):
        """Render lose screen"""
        # Draw lose text
        lose_text = self.font.render("GAME OVER", True, RED)
        lose_rect = lose_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(lose_text, lose_rect)
        
        # Draw instruction
        retry_text = self.small_font.render("Press R to retry or ESC for menu", True, WHITE)
        retry_rect = retry_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(retry_text, retry_rect)
    
    def _handle_player_input(self, dt: float):
        """Handle player input during gameplay"""
        keys = pygame.key.get_pressed()
        
        if not self.player:
            return
        
        # Handle movement
        if keys[pygame.K_j] or keys[pygame.K_LEFT]:
            self.player.move_left(self.game_world)
        elif keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            self.player.move_right(self.game_world)
        
        # Handle ice creation/removal
        if keys[pygame.K_a]:
            self.player.create_ice_left(self.game_world, self.ice_system)
        elif keys[pygame.K_d]:
            self.player.create_ice_right(self.game_world, self.ice_system)
    
    def _check_win_conditions(self):
        """Check if win conditions are met"""
        from src.entities.objects.flame import Flame
        
        # Count remaining flames
        flame_count = self.game_world.count_objects_of_type(Flame)
        
        # Win condition: no flames remaining
        if flame_count == 0:
            self.state_manager.change_state(GameState.WIN)
    
    def run(self):
        """Main game loop"""
        print("Starting ICER game...")
        print("Controls:")
        print("  J/L or Arrow Keys: Move left/right")
        print("  A/D: Create/remove ice blocks")
        print("  ESC: Pause game")
        print("  R: Restart level")
        print("  TAB: Toggle menu")
        print("  ALT+F4: Quit game")
        
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0
            
            # Game loop
            self.handle_events()
            self.update(self.dt)
            self.render()
        
        # Cleanup
        pygame.quit()
        sys.exit()
    
    def quit(self):
        """Quit the game"""
        self.running = False


def main():
    """Main entry point"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()