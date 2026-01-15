package rendering

import (
	"fmt"
	"image/color"
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/zrcoder/icer/internal/game"
	"github.com/zrcoder/icer/internal/sprites"
)

// GameRenderer handles all rendering for the game
type GameRenderer struct {
	cameraX float64
	cameraY float64
}

// NewGameRenderer creates a new game renderer
func NewGameRenderer() *GameRenderer {
	return &GameRenderer{
		cameraX: 0,
		cameraY: 0,
	}
}

// DrawWorld draws the game world including grid and objects
func (r *GameRenderer) DrawWorld(screen *ebiten.Image, objects []sprites.Sprite) {
	// Draw background
	screen.Fill(color.RGBA{20, 20, 40, 255}) // Dark blue

	// Draw grid
	r.drawGrid(screen)

	// Draw objects
	r.drawObjects(screen, objects)

	// Draw UI overlay
	r.drawUI(screen, objects)
}

// drawGrid draws the game grid
func (r *GameRenderer) drawGrid(screen *ebiten.Image) {
	for x := 0; x < game.GridWidth; x++ {
		for y := 0; y < game.GridHeight; y++ {
			cellX := float64(x * game.CellSize)
			cellY := float64(y * game.CellSize)

			// Draw grid cell
			ebitenutil.DrawRect(screen, cellX, cellY, game.CellSize, game.CellSize, color.RGBA{50, 50, 50, 255})
		}
	}
}

// drawObjects draws all game objects
func (r *GameRenderer) drawObjects(screen *ebiten.Image, objects []sprites.Sprite) {
	for _, obj := range objects {
		if !obj.IsActive() {
			continue
		}

		x, y := obj.GetGridPosition()
		centerX := float64(x*game.CellSize + game.CellSize/2)
		centerY := float64(y*game.CellSize + game.CellSize/2)

		// Apply camera transform
		drawX := centerX + r.cameraX
		drawY := centerY + r.cameraY

		// Draw object based on type
		r.drawGameObject(screen, obj, drawX, drawY)
	}
}

// drawGameObject draws a single game object
func (r *GameRenderer) drawGameObject(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	switch obj.Type() {
	case "player":
		r.drawPlayer(screen, obj, x, y)
	case "wall":
		r.drawWall(screen, obj, x, y)
	case "ice_block":
		r.drawIceBlock(screen, obj, x, y)
	case "stone":
		r.drawStone(screen, obj, x, y)
	case "flame":
		r.drawFlame(screen, obj, x, y)
	case "pot":
		r.drawPot(screen, obj, x, y)
	case "portal":
		r.drawPortal(screen, obj, x, y)
	default:
		// Default: draw colored rectangle
		r.drawColoredRect(screen, x-15, y-15, 30, 30, obj.Color())
	}
}

// drawPlayer draws the player
func (r *GameRenderer) drawPlayer(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw player as blue circle
	r.drawColoredCircle(screen, x, y, 15, obj.Color())
}

// drawWall draws a wall
func (r *GameRenderer) drawWall(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw wall as gray rectangle
	r.drawColoredRect(screen, x-20, y-20, 40, 40, obj.Color())
}

// drawIceBlock draws an ice block
func (r *GameRenderer) drawIceBlock(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw ice block as light blue rectangle with some transparency
	r.drawColoredRect(screen, x-18, y-18, 36, 36, obj.Color())

	// Add ice crystals effect
	r.drawIceCrystals(screen, x, y)
}

// drawStone draws a stone
func (r *GameRenderer) drawStone(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw stone as gray circle
	r.drawColoredCircle(screen, x, y, 18, obj.Color())
}

// drawFlame draws a flame
func (r *GameRenderer) drawFlame(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw flame as animated red/orange triangle
	r.drawColoredTriangle(screen, x, y-10, 12, obj.Color())

	// Add flame flicker effect
	flicker := math.Sin(r.getAnimTimer()*5)*0.2 + 1.0
	r.drawColoredCircle(screen, x, y, 8, color.RGBA{255, 165, 0, uint8(255 * flicker)})
}

// drawPot draws a pot
func (r *GameRenderer) drawPot(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw pot as rectangle
	r.drawColoredRect(screen, x-12, y-10, 24, 20, obj.Color())

	// Add pot rim
	r.drawColoredRect(screen, x-14, y-12, 28, 4, color.RGBA{100, 100, 100, 255})
}

// drawPortal draws a portal
func (r *GameRenderer) drawPortal(screen *ebiten.Image, obj sprites.Sprite, x, y float64) {
	// Draw portal as rotating green circle
	r.drawColoredCircle(screen, x, y, 16, obj.Color())

	// Add portal swirl effect
	swirl := math.Cos(r.getAnimTimer()*3)*0.3 + 1.0
	r.drawColoredCircle(screen, x, y, 16.0*swirl, color.RGBA{0, 255, 0, 100})
}

// drawUI draws UI overlay
func (r *GameRenderer) drawUI(screen *ebiten.Image, objects []sprites.Sprite) {
	// Draw move counter
	moves := r.countPlayerMoves(objects)
	ebitenutil.DebugPrint(screen, "Moves: "+fmt.Sprintf("%d", moves))

	// Draw flame counter
	flames := r.countFlames(objects)
	ebitenutil.DebugPrint(screen, "Flames: "+fmt.Sprintf("%d", flames))

	// Draw timer
	// timer := r.getFormattedTime()
	// ebitenutil.DebugPrintAt(screen, 10, 50, "Time: "+timer)
}

// Helper drawing functions
func (r *GameRenderer) drawColoredRect(screen *ebiten.Image, x, y, width, height float64, color color.Color) {
	ebitenutil.DrawRect(screen, x, y, width, height, color)
}

func (r *GameRenderer) drawColoredCircle(screen *ebiten.Image, x, y, radius float64, color color.Color) {
	// Simple circle approximation using multiple lines
	for angle := 0.0; angle < 2*math.Pi; angle += math.Pi / 8 {
		x1 := x + math.Cos(angle)*radius
		y1 := y + math.Sin(angle)*radius
		x2 := x + math.Cos(angle+math.Pi/8)*radius
		y2 := y + math.Sin(angle+math.Pi/8)*radius

		// Draw line from center to edge
		ebitenutil.DrawLine(screen, x, y, x1, y1, color)
		ebitenutil.DrawLine(screen, x1, y1, x2, y2, color)
	}
}

func (r *GameRenderer) drawColoredTriangle(screen *ebiten.Image, x, y, size float64, color color.Color) {
	// Draw triangle pointing up
	x1 := x
	y1 := y - size/2
	x2 := x - size/2
	y2 := y + size/2
	x3 := x + size/2
	y3 := y + size/2

	ebitenutil.DrawLine(screen, x1, y1, x2, y2, color)
	ebitenutil.DrawLine(screen, x2, y2, x3, y3, color)
	ebitenutil.DrawLine(screen, x3, y3, x1, y1, color)
}

func (r *GameRenderer) drawIceCrystals(screen *ebiten.Image, x, y float64) {
	// Draw some ice crystal effects
	for i := 0; i < 4; i++ {
		offsetX := math.Sin(float64(i)*math.Pi/2) * 8
		offsetY := math.Cos(float64(i)*math.Pi/2) * 8
		ebitenutil.DrawRect(screen, x+offsetX-2, y+offsetY-2, 4, 4, color.RGBA{200, 230, 255, 128})
	}
}

// Utility functions
func (r *GameRenderer) countPlayerMoves(objects []sprites.Sprite) int {
	// In a real implementation, you'd track this properly
	return 42 // Placeholder
}

func (r *GameRenderer) countFlames(objects []sprites.Sprite) int {
	count := 0
	for _, obj := range objects {
		if obj.Type() == "flame" && obj.IsActive() {
			count++
		}
	}
	return count
}

func (r *GameRenderer) getAnimTimer() float64 {
	// Return animation timer based on current time
	// In a real implementation, you'd track this properly
	return float64(12345) / 60.0 // Placeholder for animation
}

// MoveCamera moves the camera
func (r *GameRenderer) MoveCamera(dx, dy float64) {
	r.cameraX += dx
	r.cameraY += dy
}

// SetCameraPosition sets the camera position
func (r *GameRenderer) SetCameraPosition(x, y float64) {
	r.cameraX = x
	r.cameraY = y
}
