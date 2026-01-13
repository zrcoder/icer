# Physics Engine for ICER Game

from typing import List, Tuple, Optional, Dict, Any
from src.world.game_world import GameWorld
from src.entities.base import GameObject
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.stone import Stone
from src.utils.vector2 import Vector2


class PhysicsEngine:
    """Main physics engine for object movement and interactions"""
    
    def __init__(self, game_world: GameWorld):
        self.game_world = game_world
        self.gravity_enabled = True
        self.physics_enabled = True
        self.gravity_strength = 9.8  # m/s^2
        self.dt_accumulator = 0.0
        self.fixed_dt = 1.0 / 60.0  # 60 FPS physics timestep
        
        # Movement tracking
        self.pending_moves: List[Dict[str, Any]] = []
        self.sliding_objects: List[GameObject] = []
        
    def update(self, dt: float):
        """Update physics simulation"""
        if not self.physics_enabled:
            return
        
        # Accumulate time for fixed timestep
        self.dt_accumulator += dt
        
        # Process physics at fixed timestep
        while self.dt_accumulator >= self.fixed_dt:
            self._fixed_update(self.fixed_dt)
            self.dt_accumulator -= self.fixed_dt
        
        # Process pending moves
        self._process_pending_moves()
        
        # Update object physics properties
        # self._update_object_physics(dt)  # Commented out - method doesn't exist yet
    
    def _fixed_update(self, dt: float):
        """Fixed timestep physics update"""
        # Apply gravity
        if self.gravity_enabled:
            self._apply_gravity(dt)
        
        # Update sliding objects
        self._update_sliding_objects(dt)
        
        # Process collisions
        self._process_collisions()
    
    def _apply_gravity(self, dt: float):
        """Apply gravity to affected objects"""
        # Get all objects that need gravity
        for x, y, obj in self.game_world.grid:
            if obj is None or not obj.is_active:
                continue
            
            if not obj.get_property('affected_by_gravity', True):
                continue
            
            # Check if object should fall
            if self._should_fall(obj, x, y):
                self._make_object_fall(obj, x, y)
    
    def _should_fall(self, obj: GameObject, x: int, y: int) -> bool:
        """Check if object should fall"""
        # Check if there's support below
        if y > 0:
            below_obj = self.game_world.get_object_at(x, y - 1)
            if below_obj and below_obj.can_support_weight():
                return False
        else:
            # At bottom level
            return False
        
        return True
    
    def _make_object_fall(self, obj: GameObject, x: int, y: int):
        """Make object fall down"""
        fall_distance = 0
        
        # Calculate maximum fall distance
        for check_y in range(y - 1, -1, -1):
            if check_y < 0:
                break  # Reached bottom
            
            if self.game_world.is_empty(x, check_y):
                fall_distance += 1
            else:
                below_obj = self.game_world.get_object_at(x, check_y)
                if below_obj and below_obj.can_support_weight():
                    break
                else:
                    # Can't fall through this object
                    break
        
        # Apply fall
        if fall_distance > 0:
            new_y = y - fall_distance
            self.game_world.move_object(obj, x, new_y)
            
            # Trigger fall event
            obj.set_property('falling', True)
            obj.set_property('fall_distance', fall_distance)
            obj.set_property('last_fall_time', self._get_current_time())
    
    def _get_current_time(self) -> float:
        """Get current time from game state"""
        # TODO: Get from game state
        return 0.0
    
    def _update_sliding_objects(self, dt: float):
        """Update objects that are sliding"""
        objects_to_remove = []
        
        for obj in self.sliding_objects:
            if not obj.is_active:
                objects_to_remove.append(obj)
                continue
            
            # Update sliding physics
            slide_success = self._update_slide_physics(obj, dt)
            
            if not slide_success:
                # Object stopped sliding
                objects_to_remove.append(obj)
                if hasattr(obj, 'stop_sliding'):
                    obj.stop_sliding()
        
        # Remove stopped objects
        for obj in objects_to_remove:
            if obj in self.sliding_objects:
                self.sliding_objects.remove(obj)
    
    def _update_slide_physics(self, obj: GameObject, dt: float) -> bool:
        """Update sliding physics for a single object"""
        if not obj.get_property('sliding', False):
            return False
        
        x, y = obj.grid_x, obj.grid_y
        slide_direction = obj.get_property('slide_direction', None)
        
        if not slide_direction:
            return False
        
        # Parse slide direction
        dx, dy = 0, 0
        if slide_direction.startswith('slide_'):
            direction = slide_direction[6:]  # Remove 'slide_' prefix
            if direction == '1_0':
                dx, dy = 1, 0
            elif direction == '-1_0':
                dx, dy = -1, 0
            elif direction == '0_1':
                dx, dy = 0, 1
            elif direction == '0_-1':
                dx, dy = 0, -1
        
        new_x, new_y = x + dx, y + dy
        
        # Check if can slide to new position
        if self._can_slide_to(obj, new_x, new_y):
            # Move object
            if self.game_world.move_object(obj, new_x, new_y):
                return True
        
        # Cannot slide further
        return False
    
    def _can_slide_to(self, obj: GameObject, x: int, y: int) -> bool:
        """Check if object can slide to position"""
        if not self.game_world.is_valid_position(x, y):
            return False
        
        if not self.game_world.is_empty(x, y):
            return False
        
        # Check if landing position has support
        if y > 0:
            below_obj = self.game_world.get_object_at(x, y - 1)
            if below_obj is None:
                return False  # Would fall
        
        return True
    
    def _process_collisions(self):
        """Process object collisions and interactions"""
        interactions = []
        
        # Find all potential interactions
        for x, y, obj in self.game_world.grid:
            if obj is None or not obj.is_active:
                continue
            
            # Check adjacent objects
            neighbors = self.game_world.get_neighbors(x, y)
            for nx, ny, neighbor in neighbors:
                if neighbor:
                    interaction = self._check_interaction(obj, neighbor)
                    if interaction:
                        interactions.append(interaction)
        
        # Process interactions
        for interaction in interactions:
            self._process_interaction(interaction)
    
    def _check_interaction(self, obj1: GameObject, obj2: GameObject) -> Optional[Dict[str, Any]]:
        """Check if two objects should interact"""
        # Flame + Ice = Extinguish
        if (obj1.get_type() == "flame" and obj2.get_type() == "ice_block") or \
           (obj1.get_type() == "ice_block" and obj2.get_type() == "flame"):
            return {
                'type': 'extinguish',
                'objects': [obj1, obj2],
                'flame': obj1 if obj1.get_type() == "flame" else obj2,
                'ice': obj1 if obj1.get_type() == "ice_block" else obj2
            }
        
        # Ice Pot + Flame = Ignite
        if (obj1.get_type() == "ice_pot" and obj2.get_type() == "flame") or \
           (obj1.get_type() == "flame" and obj2.get_type() == "ice_pot"):
            ice_pot = obj1 if obj1.get_type() == "ice_pot" else obj2
            if hasattr(ice_pot, 'can_ignite') and ice_pot.can_ignite():
                return {
                    'type': 'ignite',
                    'objects': [obj1, obj2],
                    'pot': ice_pot,
                    'flame': obj1 if obj1.get_type() == "flame" else obj2
                }
        
        # Hot Pot + Ice = Melt
        if (obj1.get_type() == "hot_pot" and obj2.get_type() == "ice_block") or \
           (obj1.get_type() == "ice_block" and obj2.get_type() == "hot_pot"):
            hot_pot = obj1 if obj1.get_type() == "hot_pot" else obj2
            ice_block = obj1 if obj1.get_type() == "ice_block" else obj2
            if hasattr(ice_block, 'can_be_placed_on_hot_pot') and ice_block.can_be_placed_on_hot_pot(hot_pot.grid_y):
                return {
                    'type': 'melt',
                    'objects': [obj1, obj2],
                    'pot': hot_pot,
                    'ice': ice_block
                }
        
        return None
    
    def _process_interaction(self, interaction: Dict[str, Any]):
        """Process a specific interaction"""
        interaction_type = interaction['type']
        
        if interaction_type == 'extinguish':
            flame = interaction['flame']
            ice = interaction['ice']
            
            # Both are destroyed
            flame.destroy()
            ice.destroy()
            
            # Remove from world
            self.game_world.remove_object(flame)
            self.game_world.remove_object(ice)
            
        elif interaction_type == 'ignite':
            pot = interaction['pot']
            
            # Ignite the pot
            pot.ignite()
            
        elif interaction_type == 'melt':
            ice = interaction['ice']
            
            # Ice melts
            ice.destroy()
            self.game_world.remove_object(ice)
    
    def _process_pending_moves(self):
        """Process pending movement requests"""
        moves_to_process = self.pending_moves.copy()
        self.pending_moves.clear()
        
        for move in moves_to_process:
            self._execute_move(move)
    
    def _execute_move(self, move: Dict[str, Any]):
        """Execute a movement request"""
        obj = move['object']
        from_x = move['from_x']
        from_y = move['from_y']
        to_x = move['to_x']
        to_y = move['to_y']
        move_type = move.get('type', 'push')
        
        if move_type == 'push':
            self._execute_push(obj, from_x, from_y, to_x, to_y)
        elif move_type == 'slide':
            self._execute_slide(obj, to_x, to_y)
    
    def _execute_push(self, obj: GameObject, from_x: int, from_y: int, to_x: int, to_y: int):
        """Execute a push movement"""
        # Check if object can be pushed
        if not obj.is_pushable():
            return
        
        # Check if object is firm
        if hasattr(obj, 'is_firm') and obj.is_firm():
            return
        
        # Check push distance limits
        max_distance = 1  # Default push distance
        if hasattr(obj, 'get_push_distance'):
            max_distance = obj.get_push_distance()
        
        distance = abs(to_x - from_x) + abs(to_y - from_y)
        if distance > max_distance:
            return
        
        # Execute push
        if self.game_world.move_object_to(obj, from_x, from_y, to_x, to_y):
            # Check if object should slide after push
            if obj.get_type() == "ice_block":
                self._check_and_start_sliding(obj)
            
            return True
        
        return False
    
    def _execute_slide(self, obj: GameObject, to_x: int, to_y: int):
        """Execute a sliding movement"""
        if self.game_world.move_object(obj, to_x, to_y):
            return True
        return False
    
    def _check_and_start_sliding(self, obj):
        """Check if ice block should start sliding"""
        if obj.get_type() != "ice_block":
            return
        
        if not obj.can_slide():
            return
        
        x, y = obj.grid_x, obj.grid_y
        
        # Check if on slippery surface
        if y > 0:
            below_obj = self.game_world.get_object_at(x, y - 1)
            if below_obj and below_obj.get_type() == "ice_block":
                # Start sliding in available direction
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    slide_x, slide_y = x + dx, y + dy
                    
                    if self._can_slide_to(obj, slide_x, slide_y):
                        direction = f"slide_{dx}_{dy}"
                        obj.start_sliding(direction)
                        if obj not in self.sliding_objects:
                            self.sliding_objects.append(obj)
                        break
    
    def request_push(self, obj: GameObject, to_x: int, to_y: int):
        """Request to push an object"""
        from_x, from_y = obj.grid_x, obj.grid_y
        
        self.pending_moves.append({
            'object': obj,
            'from_x': from_x,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y,
            'type': 'push'
        })
    
    def request_slide(self, obj: GameObject, to_x: int, to_y: int):
        """Request to slide an object"""
        from_x, from_y = obj.grid_x, obj.grid_y
        
        self.pending_moves.append({
            'object': obj,
            'from_x': from_x,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y,
            'type': 'slide'
        })
    
    def update_object_physics(self, dt: float):
        """Update physics properties for all objects"""
        for x, y, obj in self.game_world.grid:
            if obj is None or not obj.is_active:
                continue
            
            # Update firm status for ice blocks and stones
            if hasattr(obj, 'check_firm_status'):
                obj.check_firm_status(self.game_world)
            
            # Update falling animation state
            if obj.get_property('falling', False):
                # Reset falling state after animation
                last_fall_time = obj.get_property('last_fall_time', 0.0)
                current_time = self._get_current_time()
                if current_time - last_fall_time > 0.3:  # 300ms fall animation
                    obj.set_property('falling', False)
    
    def get_physics_status(self) -> Dict[str, Any]:
        """Get physics engine status for debugging"""
        return {
            'physics_enabled': self.physics_enabled,
            'gravity_enabled': self.gravity_enabled,
            'pending_moves': len(self.pending_moves),
            'sliding_objects': len(self.sliding_objects),
            'dt_accumulator': self.dt_accumulator
        }