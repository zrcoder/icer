package physics

import (
	"github.com/zrcoder/icer/internal/sprites"
)

// PhysicsEngine handles all physics calculations and collisions
type PhysicsEngine struct {
	objects []sprites.Sprite
}

// NewPhysicsEngine creates a new physics engine
func NewPhysicsEngine() *PhysicsEngine {
	return &PhysicsEngine{
		objects: make([]sprites.Sprite, 0),
	}
}

// AddObject adds an object to the physics world
func (p *PhysicsEngine) AddObject(obj sprites.Sprite) {
	p.objects = append(p.objects, obj)
}

// RemoveObject removes an object from the physics world
func (p *PhysicsEngine) RemoveObject(obj sprites.Sprite) {
	for i, o := range p.objects {
		if o == obj {
			p.objects = append(p.objects[:i], p.objects[i+1:]...)
			break
		}
	}
}

// Update updates all physics calculations
func (p *PhysicsEngine) Update(dt float64) {
	// Simple physics update - in a real implementation
	// you'd want to handle gravity, collisions, etc.
	p.updateCollisions()
}

// updateCollisions handles collision detection and response
func (p *PhysicsEngine) updateCollisions() {
	for i, obj1 := range p.objects {
		if !obj1.IsActive() {
			continue
		}

		for j, obj2 := range p.objects {
			if i >= j || !obj2.IsActive() {
				continue
			}

			if p.checkCollision(obj1, obj2) {
				obj1.OnCollision(obj2)
				obj2.OnCollision(obj1)
			}
		}
	}
}

// checkCollision checks if two objects are colliding
func (p *PhysicsEngine) checkCollision(obj1, obj2 sprites.Sprite) bool {
	x1, y1 := obj1.GetGridPosition()
	x2, y2 := obj2.GetGridPosition()

	// Simple grid-based collision
	return x1 == x2 && y1 == y2
}

// MoveObject attempts to move an object to a new position
func (p *PhysicsEngine) MoveObject(obj sprites.Sprite, newX, newY int) bool {
	if !obj.IsPushable() {
		return false
	}

	// Check if the new position is valid
	if p.isPositionValid(obj, newX, newY) {
		obj.SetPosition(newX, newY)
		return true
	}

	return false
}

// isPositionValid checks if a position is valid for an object
func (p *PhysicsEngine) isPositionValid(obj sprites.Sprite, x, y int) bool {
	// Check boundaries
	if x < 0 || x >= 20 || y < 0 || y >= 15 { // Use grid constants
		return false
	}

	// Check collision with other objects
	for _, other := range p.objects {
		if other == obj || !other.IsActive() || !other.IsSolid() {
			continue
		}

		otherX, otherY := other.GetGridPosition()
		if x == otherX && y == otherY {
			return false
		}
	}

	return true
}
