# Game Rules System - Core game mechanics and interactions

from typing import List, Dict, Any, Optional, Tuple
from src.world.game_world import GameWorld
from src.entities.base import GameObject
from src.entities.objects.flame import Flame
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.stone import Stone
from src.entities.objects.pot import Pot
from src.physics.physics_engine import PhysicsEngine
from src.physics.ice_system import IceBlockSystem


class GameRulesSystem:
    """System for managing core game rules and win conditions"""
    
    def __init__(self, game_world: GameWorld, physics_engine: PhysicsEngine, ice_system: IceBlockSystem):
        self.game_world = game_world
        self.physics_engine = physics_engine
        self.ice_system = ice_system
        
        # Game state
        self.is_level_complete = False
        self.game_won = False
        self.moves_taken = 0
        self.time_elapsed = 0.0
        self.puzzles_solved = []
        self.player = None
        self.player = None
        
        # Rule configuration
        self.max_moves = 50  # Maximum moves before level fails (optional)
        self.time_limit = 300  # 5 minutes time limit (optional)
        
        # Win conditions
        self.require_all_flames_extinguished = True
        self.require_player_at_exit = False  # For specific levels
        self.require_min_objects_collected = 0  # Optional collectible requirement
        
        # Lose conditions
        self.lose_on_player_death = True
        self.lose_on_time_limit = False
        self.lose_on_move_limit = False
    
    def update(self, dt: float):
        """Update game rules"""
        self.time_elapsed += dt
        
        # Check win conditions
        self._check_win_conditions()
        
        # Check lose conditions
        self._check_lose_conditions()
        
        # Update game-specific rules
        self._update_game_specific_rules(dt)
    
    def _check_win_conditions(self):
        """Check if level is won"""
        if self.is_level_complete:
            return
        
        # Primary win condition: All flames extinguished
        if self.require_all_flames_extinguished:
            flame_count = self.game_world.count_objects_of_type(Flame)
            if flame_count == 0:
                self._trigger_level_complete()
                return
        
        # Secondary conditions
        if self.require_player_at_exit:
            if self._check_player_at_exit():
                self._trigger_level_complete()
                return
        
        if self.require_min_objects_collected > 0:
            collected = len(self.puzzles_solved)
            if collected >= self.require_min_objects_collected:
                self._trigger_level_complete()
                return
    
    def _check_lose_conditions(self):
        """Check if level is lost"""
        # Check time limit
        if self.lose_on_time_limit and self.time_elapsed > self.time_limit:
            self._trigger_level_failed("Time limit exceeded")
            return
        
        # Check move limit
        if self.lose_on_move_limit and self.moves_taken > self.max_moves:
            self._trigger_level_failed("Move limit exceeded")
            return
        
        # Check player death
        if self.lose_on_player_death:
            if self._check_player_death():
                self._trigger_level_failed("Player died")
                return
    
    def _update_game_specific_rules(self, dt: float):
        """Update game-specific rules"""
        # Flame extinguishing by ice
        self._process_flame_ice_interactions()
        
        # Ice pot ignition by flame
        self._process_pot_flame_interactions()
        
        # Ice block melting by hot pot
        self._process_ice_hotpot_interactions()
        
        # Stone heat resistance
        self._process_stone_heat_interactions()
        
        # Portal transportation
        self._process_portal_interactions()
        
        # Ice chain reactions
        self._process_ice_chain_reactions()
    
    def _process_flame_ice_interactions(self):
        """Process flame and ice block interactions"""
        flames = self.game_world.find_objects_of_type(Flame)
        ice_blocks = self.game_world.find_objects_of_type(IceBlock)
        
        for fx, fy, flame in flames:
            for ix, iy, ice in ice_blocks:
                # Check if flame and ice are adjacent
                if abs(fx - ix) <= 1 and abs(fy - iy) <= 1:
                    # Check if ice can extinguish flame
                    if self._can_ice_extinguish_flame(ice, flame):
                        self._extinguish_flame_with_ice(flame, ice)
    
    def _can_ice_extinguish_flame(self, ice, flame) -> bool:
        """Check if ice can extinguish flame"""
        # Ice can extinguish flame if they're in contact
        # Note: Ice above flame doesn't melt (per rules)
        return True
    
    def _extinguish_flame_with_ice(self, flame: Flame, ice: IceBlock):
        """Handle flame extinguishing by ice"""
        if flame.is_burning():
            flame.extinguish()
            self.game_world.remove_object(flame)
            self.ice_system.remove_ice_block(ice, self.game_world)
            
            # Add to solved puzzles
            self.puzzles_solved.append(f"Extinguished flame at ({flame.grid_x},{flame.grid_y})")
    
    def _process_pot_flame_interactions(self):
        """Process pot and flame interactions"""
        pots = self.game_world.find_objects_of_type(Pot)
        flames = self.game_world.find_objects_of_type(Flame)
        
        for px, py, pot in pots:
            if pot.is_ice():
                for fx, fy, flame in flames:
                    # Check if flame is adjacent to ice pot
                    if abs(px - fx) <= 1 and abs(py - fy) <= 1:
                        # Check if pot can be ignited
                        if self._can_flame_ignite_pot(pot, flame):
                            pot.check_for_ignition(self.game_world)
                            if pot.is_hot():
                                self.puzzles_solved.append(f"Ignited pot at ({pot.grid_x},{pot.grid_y})")
    
    def _can_flame_ignite_pot(self, pot: Pot, flame: Flame) -> bool:
        """Check if flame can ignite pot"""
        return pot.is_ice() and pot.can_ignite() and flame.is_burning()
    
    def _process_ice_hotpot_interactions(self):
        """Process ice block and hot pot interactions"""
        ice_blocks = self.game_world.find_objects_of_type(IceBlock)
        pots = self.game_world.find_objects_of_type(Pot)
        
        for ix, iy, ice in ice_blocks:
            for px, py, pot in pots:
                if pot.is_hot():
                    # Check if ice is directly above hot pot
                    if ix == px and iy == py + 1:
                        # Check if ice can be melted
                        if self._can_hotpot_melt_ice(pot, ice):
                            self._melt_ice_with_hotpot(ice, pot)
    
    def _can_hotpot_melt_ice(self, pot: Pot, ice: IceBlock) -> bool:
        """Check if hot pot can melt ice"""
        return pot.is_hot() and ice.can_be_placed_on_hot_pot(pot.grid_y)
    
    def _melt_ice_with_hotpot(self, ice: IceBlock, pot: Pot):
        """Handle ice melting by hot pot"""
        if ice.is_active:
            self.ice_system.remove_ice_block(ice, self.game_world)
            self.puzzles_solved.append(f"Melted ice at ({ice.grid_x},{ice.grid_y}) with hot pot")
    
    def _process_stone_heat_interactions(self):
        """Process stone heat resistance"""
        stones = self.game_world.find_objects_of_type(Stone)
        flames = self.game_world.find_objects_of_type(Flame)
        pots = self.game_world.find_objects_of_type(Pot)
        
        # Stones are heat resistant, so they don't get destroyed by flames or hot pots
        # This is more about protecting stones from being removed by interactions
        pass
    
    def _process_portal_interactions(self):
        """Process portal transportation rules"""
        from src.entities.objects.portal import Portal
        
        portals = self.game_world.find_objects_of_type(Portal)
        player = self._get_player()
        
        if not player:
            return
        
        # Check if player is at portal position
        for x, y, portal in portals:
            if x == player.grid_x and y == player.grid_y:
                # Check if player can use portal
                if portal.can_player_enter(player.grid_x, player.grid_y):
                    # Check portal height difference
                    height_diff = portal.grid_y - player.grid_y
                    max_diff = portal.get_property('height_difference', 1)
                    
                    if height_diff <= max_diff:
                        # Transport player
                        linked_portal = portal.get_linked_portal()
                        if linked_portal and linked_portal.can_player_accept_player(player, self.game_world):
                            portal.transport_player(player, self.game_world)
                            self.puzzles_solved.append(f"Used portal from ({portal.grid_x},{portal.grid_y})")
    
    def _process_ice_chain_reactions(self):
        """Process ice chain reactions"""
        chains = self.ice_system.get_ice_chain_reactions(self.game_world)
        
        for chain in chains:
            if len(chain) > 1:
                # Record chain reaction as solved puzzle
                start_pos = f"({chain[0].grid_x},{chain[0].grid_y})"
                self.puzzles_solved.append(f"Triggered chain reaction starting at {start_pos}")
    
    def _check_player_at_exit(self) -> bool:
        """Check if player is at exit position"""
        player = self._get_player()
        if not player:
            return False
        
        # TODO: Implement exit position checking
        return False
    
    def _check_player_death(self) -> bool:
        """Check if player is dead"""
        player = self._get_player()
        if not player:
            return False
        
        # TODO: Implement player death checking
        return False
    
    def _get_player(self) -> Optional[GameObject]:
        """Get player object"""
        # Find player in world
        for x, y, obj in self.game_world.grid:
            if obj and obj.get_type() == "player":
                return obj
        return None
    
    def _trigger_level_complete(self):
        """Trigger level completion"""
        self.is_level_complete = True
        self.game_won = True
        print(f"🎉 Level Complete! Time: {self.time_elapsed:.1f}s, Moves: {self.moves_taken}")
        print(f"Puzzles solved: {len(self.puzzles_solved)}")
        for puzzle in self.puzzles_solved:
            print(f"  • {puzzle}")
    
    def _trigger_level_failed(self, reason: str):
        """Trigger level failure"""
        self.game_won = False
        print(f"❌ Level Failed: {reason}")
        print(f"Time: {self.time_elapsed:.1f}s, Moves: {self.moves_taken}")
    
    def reset_level(self):
        """Reset level state"""
        self.is_level_complete = False
        self.game_won = False
        self.moves_taken = 0
        self.time_elapsed = 0.0
        self.puzzles_solved.clear()
    
    def increment_moves(self):
        """Increment move counter"""
        self.moves_taken += 1
    
    def get_level_status(self) -> Dict[str, Any]:
        """Get current level status"""
        return {
            'is_complete': self.is_level_complete,
            'game_won': self.game_won,
            'moves_taken': self.moves_taken,
            'time_elapsed': self.time_elapsed,
            'flames_remaining': self.game_world.count_objects_of_type(Flame),
            'ice_blocks_count': self.game_world.count_objects_of_type(IceBlock),
            'puzzles_solved': len(self.puzzles_solved),
            'puzzles_list': self.puzzles_solved.copy()
        }
    
    def set_level_requirements(self, **requirements):
        """Set level requirements"""
        if 'require_all_flames_extinguished' in requirements:
            self.require_all_flames_extinguished = requirements['require_all_flames_extinguished']
        
        if 'require_player_at_exit' in requirements:
            self.require_player_at_exit = requirements['require_player_at_exit']
        
        if 'require_min_objects_collected' in requirements:
            self.require_min_objects_collected = requirements['require_min_objects_collected']
        
        if 'time_limit' in requirements:
            self.time_limit = requirements['time_limit']
            self.lose_on_time_limit = True
        
        if 'move_limit' in requirements:
            self.max_moves = requirements['move_limit']
            self.lose_on_move_limit = True
    
    def add_puzzle_solved(self, puzzle: str):
        """Add a solved puzzle"""
        if puzzle not in self.puzzles_solved:
            self.puzzles_solved.append(puzzle)
    
    def is_game_over(self) -> bool:
        """Check if game is over (won or lost)"""
        return self.is_level_complete