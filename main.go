package main

import (
	"github.com/charmbracelet/log"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/zrcoder/icer/internal/game"
)

func init() {
	log.SetReportCaller(true)
	log.SetLevel(log.DebugLevel)
}
func main() {
	g := game.NewGame()
	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}
