package game

import (
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/zrcoder/icer/internal/levels"
	"github.com/zrcoder/icer/internal/sprites"
)

// Game represents the main game state and implements ebiten.Game
type Game struct {
	state         State
	player        *sprites.Player
	objects       []sprites.Sprite
	levelsManager *levels.Manager
}

// State represents the current state of the game
type State int

const (
	StateSelect State = iota
	StatePlaying
	StateWin
	StateLose

	FPS = 60
)

const (
	// Window settings
	WindowWidth  = 800
	WindowHeight = 600

	// Grid settings
	GridWidth  = 20
	GridHeight = 15
	CellSize   = 40
)

// NewGame creates a new game instance
func NewGame() *Game {
	ebiten.SetWindowSize(WindowWidth, WindowHeight)
	ebiten.SetWindowTitle("ICER - Ice Block Puzzle Game")

	return &Game{
		state:         StateSelect,
		levelsManager: levels.NewManager(),
	}
}

// Update updates the game logic
func (g *Game) Update() error {
	switch g.state {
	case StateSelect:
		g.updateMenu()
	case StatePlaying:
		g.updateGame()
	case StateWin, StateLose:
		g.updateGameOver()
	}
	return nil
}

// Draw renders the game
func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(color.RGBA{20, 20, 40, 255}) // Dark blue background
	switch g.state {
	case StateSelect:
		g.drawSelect(screen)
	case StatePlaying:
		g.drawGame(screen)
	case StateWin:
		g.drawGame(screen)
		g.drawWin(screen)
	case StateLose:
		g.drawGame(screen)
		g.drawLose(screen)
	}
}

// Layout returns the screen dimensions
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return WindowWidth, WindowHeight
}

// updateMenu handles menu state updates
func (g *Game) updateMenu() {
	// TODO
	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.state = StatePlaying
		log.Println("Starting game...")
	}
}

// updateGame handles main game state updates
func (g *Game) updateGame() {
	x := g.player.Position().X
	if ebiten.IsKeyPressed(ebiten.KeyLeft) || ebiten.IsKeyPressed(ebiten.KeyJ) {
		if x > 0 {
			g.player.MoveLeft()
		}
	}
	if ebiten.IsKeyPressed(ebiten.KeyRight) || ebiten.IsKeyPressed(ebiten.KeyL) {
		if x < GridWidth-1 {
			g.player.MoveRight()
		}
	}
}

// updateGameOver handles game over state updates
func (g *Game) updateGameOver() {
	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.state = StateSelect
		// Reset game state here
	}
}

// drawGame draws the main game
func (g *Game) drawGame(screen *ebiten.Image) {
	// TODO
}

// drawPaused draws the paused overlay
func (g *Game) drawPaused(screen *ebiten.Image) {
	ebitenutil.DebugPrint(screen, "PAUSED\nPress ESC to continue")
}

// drawWin draws the win screen
func (g *Game) drawWin(screen *ebiten.Image) {
	ebitenutil.DebugPrint(screen, "YOU WIN!\nPress SPACE to continue")
}

// drawLose draws the lose screen
func (g *Game) drawLose(screen *ebiten.Image) {
	ebitenutil.DebugPrint(screen, "GAME OVER\nPress SPACE to continue")
}
