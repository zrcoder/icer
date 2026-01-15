package rules

import (
	"github.com/zrcoder/icer/internal/sprites"
)

// GameRulesSystem handles game logic and win/lose conditions
type GameRulesSystem struct {
	objects []sprites.Sprite
	flames  int
	ices    int
}

// NewGameRulesSystem creates a new game rules system
func NewGameRulesSystem(objects []sprites.Sprite) *GameRulesSystem {
	g := &GameRulesSystem{}
	g.SetObjects(objects)
	return g
}

// SetObjects sets the objects to manage
func (g *GameRulesSystem) SetObjects(objects []sprites.Sprite) {
	g.objects = objects
	g.flames = 0
	g.ices = 0
	for _, obj := range g.objects {
		switch obj.Type() {
		case "flame":
			g.flames++
		case "ice_block":
			g.ices++
		}
	}
}

// CheckWin checks if the player has won
func (g *GameRulesSystem) CheckWin() bool {
	return g.flames == 0
}

// ProcessIceFlameCollision handles ice and flame collision
func (g *GameRulesSystem) ProcessIceFlameCollision(ice, flame sprites.Sprite) {
}

// ProcessPortalTeleportation handles portal teleportation
func (g *GameRulesSystem) ProcessPortalTeleportation(obj sprites.Sprite, portal *sprites.Portal) {
	linkedPortal := portal.GetLinkedPortal()
	if linkedPortal != nil && linkedPortal.IsActive() {
		// Get linked portal position
		newX, newY := linkedPortal.GetGridPosition()
		obj.SetPosition(newX, newY)
	}
}

// Update game rules
func (g *GameRulesSystem) Update() {
	// Re-categorize objects in case their states changed
	g.categorizeObjects()
}
