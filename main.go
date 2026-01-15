package main

import (
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/zrcoder/icer/internal/game"
)

func main() {
	g := game.NewGame()

	if err := ebiten.RunGame(g); err != nil {
		log.Fatal("Failed to run game:", err)
	}
}
