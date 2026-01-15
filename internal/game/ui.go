package game

import (
	"fmt"

	"github.com/ebitenui/ebitenui/widget"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/zrcoder/icer/internal/levels/sections"
)

func (g *Game) drawSelect(screen *ebiten.Image) {
	root := widget.NewContainer(
		widget.ContainerOpts.Layout(widget.NewRowLayout(
			widget.RowLayoutOpts.Direction(widget.DirectionVertical),
			widget.RowLayoutOpts.Spacing(10),
		)),
	)

	titleLabel := widget.NewLabel(
		widget.LabelOpts.LabelText("ICER - Level Selection"),
	)
	root.AddChild(titleLabel)

	sectionContainer := widget.NewContainer(
		widget.ContainerOpts.Layout(widget.NewGridLayout(
			widget.GridLayoutOpts.Columns(sections.Count),
			widget.GridLayoutOpts.Spacing(5, 5),
		)),
	)
	for i := range sections.Count {
		btn := widget.NewButton(
			widget.ButtonOpts.TextLabel(fmt.Sprintf("Section %d", i+1)),
			widget.ButtonOpts.WidgetOpts(
				widget.WidgetOpts.MinSize(60, 60),
			),
			widget.ButtonOpts.ClickedHandler(func(args *widget.ButtonClickedEventArgs) {
				g.levelsManager.SetCurrentSection(i)
			}),
		)
		sectionContainer.AddChild(btn)
	}
	root.AddChild(sectionContainer)

	// Create back button
	backButton := widget.NewButton(
		widget.ButtonOpts.TextLabel("Back to Menu"),
		widget.ButtonOpts.WidgetOpts(
			widget.WidgetOpts.MinSize(120, 40),
		),
		widget.ButtonOpts.ClickedHandler(func(args *widget.ButtonClickedEventArgs) {
			fmt.Println("Back to menu")
		}),
	)
	root.AddChild(backButton)

	root.Render(screen)
}
