package sprites

import (
	"image/color"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/vector"
	"github.com/zrcoder/icer/internal/utils"
)

const (
	SpriteWidth  = 10
	SpriteHeight = 10

	step = 10
)

var (
	darkGray  = color.RGBA{64, 64, 64, 255}
	lightBlue = color.RGBA{173, 216, 230, 255}
	gray      = color.RGBA{128, 128, 128, 255}
	red       = color.RGBA{255, 0, 0, 255}
	green     = color.RGBA{0, 255, 0, 255}
	blue      = color.RGBA{0, 100, 255, 255}
	orange    = color.RGBA{255, 165, 0, 255}
	white     = color.RGBA{255, 255, 255, 255}
)

type Wall struct {
	*Base
}

func NewWall(x, y int) *Wall {
	wall := &Wall{
		Base: NewBase(x, y),
	}

	return wall
}

func (w *Wall) Type() string {
	return "wall"
}

func (w *Wall) Draw(parent *ebiten.Image) {
	drawReact(parent, w.position, darkGray)
}

type Ice struct {
	*Base
}

func NewIce(x, y int) *Ice {
	ice := &Ice{
		Base: NewBase(x, y),
	}
	return ice
}

func (i *Ice) Type() string {
	return "ice"
}

func (i *Ice) Draw(parent *ebiten.Image) {
	drawReact(parent, i.position, lightBlue)
}

type Stone struct {
	*Base
}

func NewStone(x, y int) *Stone {
	stone := &Stone{
		Base: NewBase(x, y),
	}

	return stone
}

func (s *Stone) Type() string {
	return "stone"
}

func (s *Stone) Draw(parent *ebiten.Image) {
	drawReact(parent, s.position, gray)
}

type Flame struct {
	*Base
}

func NewFlame(x, y int) *Flame {
	flame := &Flame{
		Base: NewBase(x, y),
	}

	return flame
}

func (f *Flame) Type() string {
	return "flame"
}

func (f *Flame) Draw(parent *ebiten.Image) {
	drawCircle(parent, f.position, red)
}

type Portal struct {
	*Base
	ID byte
}

func NewPortal(id byte, x, y int) *Portal {
	portal := &Portal{
		Base: NewBase(x, y),
		ID:   id,
	}

	return portal
}

func (p *Portal) Type() string {
	return "portal"
}

func (p *Portal) Draw(parent *ebiten.Image) {
	drawCircle(parent, p.position, green)
}

type Player struct {
	*Base
}

func NewPlayer(x, y int) *Player {
	player := &Player{
		Base: NewBase(x, y),
	}

	return player
}

func (p *Player) Type() string {
	return "player"
}

func (p *Player) Draw(parant *ebiten.Image) {
	drawCircle(parant, p.position, blue)
}

func (p *Player) MoveLeft() {
	p.position.X -= step
}

func (p *Player) MoveRight() {
	p.position.X += step
}

type Pot struct {
	*Base
	Hot bool
}

func NewPot(x, y int) *Pot {
	pot := &Pot{
		Base: NewBase(x, y),
	}
	return pot
}

func (p *Pot) Type() string {
	return "pot"
}

func (p *Pot) Draw(parent *ebiten.Image) {
	if p.Hot {
		drawCircle(parent, p.position, orange)
	} else {
		drawCircle(parent, p.position, white)
	}
}

func drawReact(parent *ebiten.Image, pos utils.Position, c color.Color) {
	vector.DrawFilledRect(
		parent,
		float32(pos.X),
		float32(pos.Y),
		SpriteWidth,
		SpriteHeight,
		c,
		false,
	)
}

func drawCircle(parent *ebiten.Image, pos utils.Position, c color.Color) {
	vector.DrawFilledCircle(
		parent,
		float32(pos.X),
		float32(pos.Y),
		SpriteWidth/2,
		c,
		false,
	)
}
