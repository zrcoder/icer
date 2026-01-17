package game

import (
	"github.com/ebitenui/ebitenui"
	"github.com/ebitenui/ebitenui/widget"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/zrcoder/icer/internal/levels"
	"github.com/zrcoder/icer/internal/sprites"
)

// Game represents the main game state and implements ebiten.Game
type Game struct {
	state          State
	player         *sprites.Player
	objects        []sprites.Sprite
	levelsManager  *levels.Manager
	selectUI       ebitenui.UI
	sceneUI        ebitenui.UI
	titleContainer *widget.Container
}

// State represents the current state of the game
type State int

const (
	StateSelect State = iota
	StatePlaying
	StateWin
	StateLose
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

	g := &Game{
		state:         StateSelect,
		levelsManager: levels.NewManager(),
	}
	g.initUI()
	return g
}

// Update updates the game logic
func (g *Game) Update() error {
	switch g.state {
	case StateSelect:
		g.updateSelect()
	case StatePlaying:
		g.updateGame()
	case StateWin, StateLose:
		g.updateGameOver()
	}
	return nil
}

// Layout returns the screen dimensions
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return WindowWidth, WindowHeight
}

// updateSelect handles menu state updates
func (g *Game) updateSelect() {
	g.selectUI.Update()
}

// updateGame handles main game state updates
func (g *Game) updateGame() {
	g.sceneUI.Update()
	if ebiten.IsKeyPressed(ebiten.KeySpace) {
		g.state = StateSelect
	}
	// x := g.player.Position().X
	// if ebiten.IsKeyPressed(ebiten.KeyLeft) || ebiten.IsKeyPressed(ebiten.KeyJ) {
	// 	if x > 0 {
	// 		g.player.MoveLeft()
	// 	}
	// }
	// if ebiten.IsKeyPressed(ebiten.KeyRight) || ebiten.IsKeyPressed(ebiten.KeyL) {
	// 	if x < GridWidth-1 {
	// 		g.player.MoveRight()
	// 	}
	// }
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

// drawWin draws the win screen
func (g *Game) drawWin(screen *ebiten.Image) {
	ebitenutil.DebugPrint(screen, "YOU WIN!\nPress SPACE to continue")
}

// drawLose draws the lose screen
func (g *Game) drawLose(screen *ebiten.Image) {
	ebitenutil.DebugPrint(screen, "GAME OVER\nPress SPACE to continue")
}
