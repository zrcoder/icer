# Vector2D Class for 2D Vector Operations

import math
from typing import Tuple


class Vector2:
    """2D Vector class for position and movement calculations"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Vector2):
            return abs(self.x - other.x) < 1e-9 and abs(self.y - other.y) < 1e-9
        return False
    
    def __add__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            raise TypeError("Can only add Vector2 to Vector2 or tuple/list of length 2")
    
    def __sub__(self, other) -> 'Vector2':
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (tuple, list)) and len(other) == 2:
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            raise TypeError("Can only subtract Vector2 from Vector2 or tuple/list of length 2")
    
    def __mul__(self, scalar) -> 'Vector2':
        if isinstance(scalar, (int, float)):
            return Vector2(self.x * scalar, self.y * scalar)
        else:
            raise TypeError("Can only multiply Vector2 by scalar")
    
    def __rmul__(self, scalar) -> 'Vector2':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar) -> 'Vector2':
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Vector2(self.x / scalar, self.y / scalar)
        else:
            raise TypeError("Can only divide Vector2 by non-zero scalar")
    
    def __neg__(self) -> 'Vector2':
        return Vector2(-self.x, -self.y)
    
    def __getitem__(self, index) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Vector2 index out of range")
    
    def magnitude(self) -> float:
        """Get the length of the vector"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def magnitude_squared(self) -> float:
        """Get the squared length of the vector (faster than magnitude)"""
        return self.x * self.x + self.y * self.y
    
    def normalize(self) -> 'Vector2':
        """Get a normalized copy of the vector"""
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)
    
    def normalized(self) -> 'Vector2':
        """Alias for normalize()"""
        return self.normalize()
    
    def distance_to(self, other) -> float:
        """Get distance to another vector"""
        if isinstance(other, Vector2):
            return (self - other).magnitude()
        else:
            raise TypeError("Can only calculate distance to Vector2")
    
    def distance_squared_to(self, other) -> float:
        """Get squared distance to another vector (faster)"""
        if isinstance(other, Vector2):
            return (self - other).magnitude_squared()
        else:
            raise TypeError("Can only calculate distance to Vector2")
    
    def dot(self, other) -> float:
        """Calculate dot product with another vector"""
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("Can only calculate dot product with Vector2")
    
    def cross(self, other) -> float:
        """Calculate 2D cross product (returns scalar)"""
        if isinstance(other, Vector2):
            return self.x * other.y - self.y * other.x
        else:
            raise TypeError("Can only calculate cross product with Vector2")
    
    def lerp(self, other, t: float) -> 'Vector2':
        """Linear interpolation between this vector and another"""
        if isinstance(other, Vector2):
            t = max(0, min(1, t))  # Clamp t between 0 and 1
            return self + (other - self) * t
        else:
            raise TypeError("Can only lerp with Vector2")
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple"""
        return (self.x, self.y)
    
    def to_int_tuple(self) -> Tuple[int, int]:
        """Convert to integer tuple"""
        return (int(self.x), int(self.y))
    
    def copy(self) -> 'Vector2':
        """Create a copy of this vector"""
        return Vector2(self.x, self.y)
    
    @classmethod
    def zero(cls) -> 'Vector2':
        """Create a zero vector"""
        return cls(0, 0)
    
    @classmethod
    def one(cls) -> 'Vector2':
        """Create a vector with all components as 1"""
        return cls(1, 1)
    
    @classmethod
    def up(cls) -> 'Vector2':
        """Create a vector pointing up"""
        return cls(0, 1)
    
    @classmethod
    def down(cls) -> 'Vector2':
        """Create a vector pointing down"""
        return cls(0, -1)
    
    @classmethod
    def left(cls) -> 'Vector2':
        """Create a vector pointing left"""
        return cls(-1, 0)
    
    @classmethod
    def right(cls) -> 'Vector2':
        """Create a vector pointing right"""
        return cls(1, 0)
    
    @classmethod
    def from_tuple(cls, t: Tuple[float, float]) -> 'Vector2':
        """Create vector from tuple"""
        return cls(t[0], t[1])