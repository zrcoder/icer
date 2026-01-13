# Ice Block System - Enhanced ice block creation and management

from typing import Optional, List, Tuple
from src.entities.objects.ice_block import IceBlock
from src.game.constants import COLOR_ICE_BLOCK


class IceBlockSystem:
    """System for managing ice block creation, removal, and interactions"""
    
    def __init__(self):
        self.ice_blocks: List[IceBlock] = []
        self.max_ice_blocks = 20  # Maximum ice blocks per level
        
    def create_ice_block(self, x: int, y: int, game_world) -> Optional[IceBlock]:
        """Create ice block at specified position"""
        # Check if position is valid
        if not game_world.is_valid_position(x, y):
            return None
        
        # Check if position is empty
        if not game_world.is_empty(x, y):
            return None
        
        # Check if we're at max ice blocks
        if len(self.ice_blocks) >= self.max_ice_blocks:
            return None
        
        # Check if ice can be placed here (not on hot pot)
        if self._is_blocked_by_hot_pot(x, y, game_world):
            return None
        
        # Create ice block
        ice_block = IceBlock(x, y)
        
        if game_world.add_object(ice_block, x, y):
            self.ice_blocks.append(ice_block)
            return ice_block
        
        return None
    
    def remove_ice_block(self, ice_block: IceBlock, game_world) -> bool:
        """Remove ice block from world"""
        if ice_block not in self.ice_blocks:
            return False
        
        if game_world.remove_object(ice_block):
            self.ice_blocks.remove(ice_block)
            return True
        
        return False
    
    def remove_ice_block_at(self, x: int, y: int, game_world) -> bool:
        """Remove ice block at specific position"""
        obj = game_world.get_object_at(x, y)
        if obj and isinstance(obj, IceBlock):
            return self.remove_ice_block(obj, game_world)
        return False
    
    def _is_blocked_by_hot_pot(self, x: int, y: int, game_world) -> bool:
        """Check if ice placement is blocked by hot pot below"""
        # Check if there's a hot pot directly below
        if y > 0:
            below_obj = game_world.get_object_at(x, y - 1)
            if below_obj and below_obj.get_type() == "hot_pot":
                # Ice cannot be placed directly on hot pot
                return True
        
        return False
    
    def get_ice_block_at(self, x: int, y: int, game_world) -> Optional[IceBlock]:
        """Get ice block at specific position"""
        obj = game_world.get_object_at(x, y)
        if obj and isinstance(obj, IceBlock):
            return obj
        return None
    
    def find_all_ice_blocks(self, game_world) -> List[Tuple[int, int, IceBlock]]:
        """Find all ice blocks in the world"""
        return game_world.find_objects_of_type(IceBlock)
    
    def count_ice_blocks(self, game_world) -> int:
        """Count all ice blocks in the world"""
        return game_world.count_objects_of_type(IceBlock)
    
    def update_all_ice_blocks(self, dt: float, game_world):
        """Update all ice blocks in the system"""
        # Update firm status for all ice blocks
        for x, y, ice_block in self.find_all_ice_blocks(game_world):
            ice_block.check_firm_status(game_world)
        
        # Update physics for all ice blocks
        self._update_ice_physics(dt, game_world)
        
        # Handle interactions
        self._handle_ice_interactions(game_world)
    
    def _update_ice_physics(self, dt: float, game_world):
        """Update physics for all ice blocks"""
        ice_blocks_to_process = []
        
        for x, y, ice_block in self.find_all_ice_blocks(game_world):
            if ice_block.is_firm():
                continue  # Firm ice blocks don't move
            
            ice_blocks_to_process.append((x, y, ice_block))
        
        # Process sliding ice blocks
        for x, y, ice_block in ice_blocks_to_process:
            self._process_ice_sliding(ice_block, game_world)
    
    def _process_ice_sliding(self, ice_block: IceBlock, game_world):
        """Process sliding physics for ice block"""
        if not ice_block.can_slide():
            return
        
        x, y = ice_block.grid_x, ice_block.grid_y
        
        # Check if ice should slide (not firm and no support below)
        if y > 0:
            below_obj = game_world.get_object_at(x, y - 1)
            if below_obj is None:
                # Ice should fall (handled by gravity)
                return
            elif below_obj and below_obj.is_solid():
                # Check if on a slippery surface (another ice block)
                if below_obj.get_type() == "ice_block":
                    # Try to slide in available directions
                    self._try_ice_slide(ice_block, game_world)
    
    def _try_ice_slide(self, ice_block: IceBlock, game_world):
        """Try to slide ice block in available directions"""
        x, y = ice_block.grid_x, ice_block.grid_y
        
        # Try sliding in all four directions
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, up, down
        
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            
            # Check if can slide to this position
            if self._can_slide_to(ice_block, new_x, new_y, game_world):
                # Start sliding
                ice_block.start_sliding(f"slide_{dx}_{dy}")
                break
    
    def _can_slide_to(self, ice_block: IceBlock, x: int, y: int, game_world) -> bool:
        """Check if ice block can slide to position"""
        if not game_world.is_valid_position(x, y):
            return False
        
        if not game_world.is_empty(x, y):
            return False
        
        # Check if landing position has support
        if y > 0:
            below_obj = game_world.get_object_at(x, y - 1)
            if below_obj is None:
                return False  # Would fall
        
        return True
    
    def _handle_ice_interactions(self, game_world):
        """Handle interactions between ice blocks and other objects"""
        interactions_to_process = []
        
        for x, y, ice_block in self.find_all_ice_blocks(game_world):
            # Check adjacent objects for interactions
            neighbors = game_world.get_adjacent_objects(x, y)
            
            for neighbor_obj in neighbors:
                if neighbor_obj.get_type() == "flame":
                    interactions_to_process.append((ice_block, neighbor_obj, "extinguish"))
                elif neighbor_obj.get_type() == "hot_pot":
                    interactions_to_process.append((ice_block, neighbor_obj, "melt"))
        
        # Process interactions
        for ice_block, other_obj, interaction_type in interactions_to_process:
            self._process_interaction(ice_block, other_obj, interaction_type, game_world)
    
    def _process_interaction(self, ice_block: IceBlock, other_obj, interaction_type: str, game_world):
        """Process specific interaction"""
        if interaction_type == "extinguish":
            # Ice extinguishes flame, both are destroyed
            ice_block.on_collision(other_obj)
            if ice_block.is_active == False:  # Ice was destroyed
                game_world.remove_object(ice_block)
                if ice_block in self.ice_blocks:
                    self.ice_blocks.remove(ice_block)
            
            # Remove flame
            if other_obj.is_fragile():
                game_world.remove_object(other_obj)
        
        elif interaction_type == "melt":
            # Ice melts when touching hot pot
            if ice_block.can_be_placed_on_hot_pot(other_obj.grid_y):
                ice_block.on_collision(other_obj)
                if ice_block.is_active == False:  # Ice was destroyed
                    game_world.remove_object(ice_block)
                    if ice_block in self.ice_blocks:
                        self.ice_blocks.remove(ice_block)
    
    def clear_all_ice_blocks(self, game_world):
        """Remove all ice blocks from the world"""
        for ice_block in self.ice_blocks.copy():
            game_world.remove_object(ice_block)
        
        self.ice_blocks.clear()
    
    def get_ice_chain_reactions(self, game_world) -> List[List[IceBlock]]:
        """Find potential ice chain reactions"""
        chain_reactions = []
        
        # Look for ice blocks that, when removed, could cause others to fall
        for x, y, ice_block in self.find_all_ice_blocks(game_world):
            if ice_block.is_firm():
                continue  # Firm ice blocks won't fall
            
            # Check what's above this ice block
            above_obj = game_world.get_object_at(x, y + 1)
            if above_obj and above_obj.get_type() == "ice_block":
                # This could cause a chain reaction
                chain = self._find_falling_chain(above_obj, game_world)
                if len(chain) > 1:
                    chain_reactions.append(chain)
        
        return chain_reactions
    
    def _find_falling_chain(self, start_obj, game_world, visited=None) -> List[IceBlock]:
        """Recursively find chain of falling ice blocks"""
        if visited is None:
            visited = set()
        
        if start_obj in visited or start_obj.get_type() != "ice_block":
            return []
        
        visited.add(start_obj)
        chain = [start_obj]
        
        x, y = start_obj.grid_x, start_obj.grid_y
        
        # Check what's above
        above_obj = game_world.get_object_at(x, y + 1)
        if above_obj and above_obj.get_type() == "ice_block":
            above_ice = above_obj
            above_ice.check_firm_status(game_world)
            if not above_ice.is_firm():
                chain.extend(self._find_falling_chain(above_ice, game_world, visited))
        
        return chain
    
    def reset(self):
        """Reset the ice block system"""
        self.ice_blocks.clear()
    
    def get_status(self) -> dict:
        """Get system status for debugging"""
        return {
            'ice_block_count': len(self.ice_blocks),
            'max_ice_blocks': self.max_ice_blocks,
            'ice_blocks': [(ib.grid_x, ib.grid_y) for ib in self.ice_blocks]
        }