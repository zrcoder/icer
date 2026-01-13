# Object Pushing System

from typing import List, Tuple, Optional, Dict, Any
from src.entities.base import GameObject
from src.world.game_world import GameWorld
from src.entities.objects.ice_block import IceBlock
from src.entities.objects.stone import Stone
from src.physics.physics_engine import PhysicsEngine


class PushSystem:
    """System for handling object pushing mechanics"""
    
    def __init__(self, game_world: GameWorld, physics_engine: PhysicsEngine):
        self.game_world = game_world
        self.physics_engine = physics_engine
        self.push_requests: List[Dict[str, Any]] = []
        
    def try_push_object(self, obj: GameObject, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        """Try to push an object in a direction"""
        if not obj.is_pushable():
            return False
        
        # Check if object is firm (attached)
        if hasattr(obj, 'is_firm') and obj.is_firm():
            return False
        
        # Check push distance limits
        max_distance = self._get_max_push_distance(obj)
        distance = abs(to_x - from_x) + abs(to_y - from_y)
        if distance > max_distance:
            return False
        
        # Check if destination is empty
        if not self.game_world.is_empty(to_x, to_y):
            return False
        
        # Check if there's something to push at source position
        source_obj = self.game_world.get_object_at(from_x, from_y)
        if source_obj != obj:
            return False
        
        # Perform the push
        if self.game_world.move_object_to(obj, from_x, from_y, to_x, to_y):
            # Handle post-push physics
            self._handle_post_push_physics(obj, to_x, to_y)
            return True
        
        return False
    
    def _get_max_push_distance(self, obj: GameObject) -> int:
        """Get maximum push distance for object"""
        if hasattr(obj, 'get_push_distance'):
            return obj.get_push_distance()
        return 1  # Default
    
    def _handle_post_push_physics(self, obj: GameObject, x: int, y: int):
        """Handle physics after an object is pushed"""
        # Check if ice block should start sliding
        if obj.get_type() == "ice_block":
            self._check_ice_sliding(obj, x, y)
        
        # Check for chain reactions
        self._check_chain_reactions(obj, x, y)
    
    def _check_ice_sliding(self, ice_block: IceBlock, x: int, y: int):
        """Check if ice block should start sliding after push"""
        if not ice_block.can_slide():
            return
        
        # Check if on slippery surface (another ice block)
        if y > 0:
            below_obj = self.game_world.get_object_at(x, y - 1)
            if below_obj and below_obj.get_type() == "ice_block":
                # Try to slide in available directions
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                
                for dx, dy in directions:
                    slide_x, slide_y = x + dx, y + dy
                    
                    if self._can_slide_to(ice_block, slide_x, slide_y):
                        direction = f"slide_{dx}_{dy}"
                        ice_block.start_sliding(direction)
                        return
    
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
    
    def _check_chain_reactions(self, obj: GameObject, x: int, y: int):
        """Check for chain reactions after push"""
        # Check if pushing this object caused others to fall
        chain_reactions = self._find_falling_objects(x, y)
        
        for falling_obj, fall_distance in chain_reactions:
            # Request physics to handle falling
            if hasattr(falling_obj, 'set_property'):
                falling_obj.set_property('falling', True)
                falling_obj.set_property('fall_distance', fall_distance)
    
    def _find_falling_objects(self, push_x: int, push_y: int) -> List[Tuple[GameObject, int]]:
        """Find objects that will fall due to a push"""
        falling_objects = []
        
        # Check positions above where push originated
        check_x, check_y = push_x, push_y + 1
        above_obj = self.game_world.get_object_at(check_x, check_y)
        
        if above_obj and above_obj.get_property('affected_by_gravity', True):
            # Check if this object now has no support
            if self._object_has_no_support(above_obj, check_x, check_y):
                fall_distance = self._calculate_fall_distance(above_obj, check_x, check_y)
                if fall_distance > 0:
                    falling_objects.append((above_obj, fall_distance))
        
        return falling_objects
    
    def _object_has_no_support(self, obj: GameObject, x: int, y: int) -> bool:
        """Check if object has no support below"""
        if y <= 0:
            return False  # At bottom
        
        below_obj = self.game_world.get_object_at(x, y - 1)
        if below_obj is None:
            return True  # No support
        
        if below_obj.can_support_weight():
            return False  # Has support
        
        return True  # Support cannot hold this object
    
    def _calculate_fall_distance(self, obj: GameObject, x: int, y: int) -> int:
        """Calculate how far an object will fall"""
        fall_distance = 0
        
        for check_y in range(y - 1, -1, -1):
            if check_y < 0:
                break  # Reached bottom
            
            if self.game_world.is_empty(x, check_y):
                fall_distance += 1
            else:
                below_obj = self.game_world.get_object_at(x, check_y)
                if below_obj and below_obj.can_support_weight():
                    break  # Found support
                else:
                    break  # Cannot fall through this object
        
        return fall_distance
    
    def can_push_from_position(self, pusher_x: int, pusher_y: int, target_x: int, target_y: int, pusher_obj: GameObject) -> bool:
        """Check if pusher can push object at target position"""
        # Check if target is adjacent to pusher
        distance = abs(pusher_x - target_x) + abs(pusher_y - target_y)
        if distance != 1:
            return False
        
        # Get object at target position
        target_obj = self.game_world.get_object_at(target_x, target_y)
        if not target_obj:
            return False
        
        # Check if object can be pushed
        if not target_obj.is_pushable():
            return False
        
        # Check if object is firm
        if hasattr(target_obj, 'is_firm') and target_obj.is_firm():
            return False
        
        # Check if there's empty space beyond target
        push_dx = target_x - pusher_x
        push_dy = target_y - pusher_y
        new_x = target_x + push_dx
        new_y = target_y + push_dy
        
        if not self.game_world.is_valid_position(new_x, new_y):
            return False
        
        if not self.game_world.is_empty(new_x, new_y):
            return False
        
        return True
    
    def execute_push_from_position(self, pusher_x: int, pusher_y: int, target_x: int, target_y: int, pusher_obj: GameObject) -> bool:
        """Execute push from pusher position to target"""
        if not self.can_push_from_position(pusher_x, pusher_y, target_x, target_y, pusher_obj):
            return False
        
        target_obj = self.game_world.get_object_at(target_x, target_y)
        if not target_obj:
            return False
        
        # Calculate new position
        push_dx = target_x - pusher_x
        push_dy = target_y - pusher_y
        new_x = target_x + push_dx
        new_y = target_y + push_dy
        
        # Move the object
        if self.game_world.move_object_to(target_obj, target_x, target_y, new_x, new_y):
            self._handle_post_push_physics(target_obj, new_x, new_y)
            return True
        
        return False
    
    def get_pushable_objects(self) -> List[Tuple[int, int, GameObject]]:
        """Get all pushable objects in the world"""
        pushable_objects = []
        
        for x, y, obj in self.game_world.grid:
            if obj and obj.is_pushable():
                # Check if object is not firm
                if not hasattr(obj, 'is_firm') or not obj.is_firm():
                    pushable_objects.append((x, y, obj))
        
        return pushable_objects
    
    def get_push_preview(self, obj: GameObject, direction: str) -> Optional[Tuple[int, int]]:
        """Get preview of where object would be pushed"""
        if not obj.is_pushable():
            return None
        
        x, y = obj.grid_x, obj.grid_y
        
        # Calculate direction
        dx, dy = 0, 0
        if direction == "up":
            dy = 1
        elif direction == "down":
            dy = -1
        elif direction == "left":
            dx = -1
        elif direction == "right":
            dx = 1
        else:
            return None
        
        new_x, new_y = x + dx, y + dy
        
        # Check if valid
        if not self.game_world.is_valid_position(new_x, new_y):
            return None
        
        if not self.game_world.is_empty(new_x, new_y):
            return None
        
        return (new_x, new_y)
    
    def process_push_requests(self):
        """Process all pending push requests"""
        requests_to_process = self.push_requests.copy()
        self.push_requests.clear()
        
        for request in requests_to_process:
            self._execute_push_request(request)
    
    def _execute_push_request(self, request: Dict[str, Any]):
        """Execute a specific push request"""
        obj = request['object']
        from_x = request['from_x']
        from_y = request['from_y']
        to_x = request['to_x']
        to_y = request['to_y']
        
        self.try_push_object(obj, from_x, from_y, to_x, to_y)
    
    def add_push_request(self, obj: GameObject, from_x: int, from_y: int, to_x: int, to_y: int):
        """Add a push request to the queue"""
        self.push_requests.append({
            'object': obj,
            'from_x': from_x,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y,
            'timestamp': self._get_current_time()
        })
    
    def _get_current_time(self) -> float:
        """Get current time"""
        # TODO: Get from game state
        return 0.0
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get push system status for debugging"""
        return {
            'pushable_objects': len(self.get_pushable_objects()),
            'pending_requests': len(self.push_requests),
            'push_requests': self.push_requests.copy()
        }