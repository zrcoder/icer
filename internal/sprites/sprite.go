package sprites

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/zrcoder/icer/internal/utils"
)

// Sprite interface defines the basic contract for all game objects
type Sprite interface {
	Type() string
	Draw(parent *ebiten.Image)
	Position() utils.Position
}

// Base provides common functionality for game objects
type Base struct {
	position utils.Position
}

// NewBase creates a new base object
func NewBase(x, y int) *Base {
	return &Base{
		position: utils.Position{X: x, Y: y},
	}
}

func (b *Base) Position() utils.Position {
	return b.position
}
