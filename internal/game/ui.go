package game

import (
	"bytes"
	"fmt"
	"image/color"
	"strconv"

	"github.com/charmbracelet/log"
	"github.com/ebitenui/ebitenui/image"
	"github.com/ebitenui/ebitenui/widget"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/text/v2"
	"github.com/zrcoder/icer/internal/levels/sections"
	"golang.org/x/image/colornames"
	"golang.org/x/image/font/gofont/goregular"
)

var defaultFace = DefaultFont()

func (g *Game) initUI() {
	g.titleContainer = widget.NewContainer()
	g.createSelectUI()
	g.createScenUI()
}

func (g *Game) createSelectUI() {
	root := widget.NewContainer(
		widget.ContainerOpts.Layout(
			widget.NewRowLayout(
				widget.RowLayoutOpts.Direction(widget.DirectionVertical),
				widget.RowLayoutOpts.Padding(widget.NewInsetsSimple(30)),
				widget.RowLayoutOpts.Spacing(15),
			),
		),
	)

	// root.AddChild()
	root.AddChild(g.createSectionContainer())
	root.AddChild(g.createLevelContainer())
	g.selectUI.Container = root
}

func (g *Game) createSectionContainer() *widget.Container {
	return g.createSectionLevelContainer("Section", sections.Count, func(i int) {
		g.levelsManager.SetCurrentSection(i)
	})
}

func (g *Game) createLevelContainer() *widget.Container {
	return g.createSectionLevelContainer("Level", g.levelsManager.CurrentSection().LevelCount, func(i int) {
		g.levelsManager.SetCurrentLevel(i)
		g.state = StatePlaying
	})
}

func (g *Game) createSectionLevelContainer(title string, count int, buttonClickHander func(int)) *widget.Container {
	container := widget.NewContainer(
		widget.ContainerOpts.Layout(widget.NewRowLayout(
			widget.RowLayoutOpts.Direction(widget.DirectionVertical),
		)),
	)
	label := widget.NewLabel(
		widget.LabelOpts.Text(
			title,
			&defaultFace,
			&widget.LabelColor{
				Idle: colornames.White,
			}),
	)
	container.AddChild(label)
	body := widget.NewContainer(
		widget.ContainerOpts.Layout(widget.NewGridLayout(
			widget.GridLayoutOpts.Columns(count),
			widget.GridLayoutOpts.Spacing(18, 0),
		)),
	)
	for i := range count {
		button := createButton(
			strconv.Itoa(i+1),
			func(args *widget.ButtonClickedEventArgs) {
				log.Debug("button clicked", "title", title, "id", i)
				buttonClickHander(i)
			},
		)
		if title == "Section" && i == g.levelsManager.CurrentSection().ID {
			button.Focus(true)
		}
		body.AddChild(button)
	}
	container.AddChild(body)
	return container
}

func createButton(name string, handler func(args *widget.ButtonClickedEventArgs)) *widget.Button {
	return widget.NewButton(
		widget.ButtonOpts.WidgetOpts(
			widget.WidgetOpts.LayoutData(widget.AnchorLayoutData{
				HorizontalPosition: widget.AnchorLayoutPositionCenter,
				VerticalPosition:   widget.AnchorLayoutPositionCenter,
			}),
			widget.WidgetOpts.MinSize(80, 80),
		),
		widget.ButtonOpts.Image(&widget.ButtonImage{
			Idle:    image.NewBorderedNineSliceColor(colornames.Black, colornames.Gainsboro, 3),
			Hover:   image.NewBorderedNineSliceColor(color.NRGBA{R: 130, G: 130, B: 150, A: 255}, color.NRGBA{70, 70, 70, 255}, 3),
			Pressed: image.NewAdvancedNineSliceColor(color.NRGBA{R: 130, G: 130, B: 150, A: 255}, image.NewBorder(3, 2, 2, 2, color.NRGBA{70, 70, 70, 255})),
		}),
		widget.ButtonOpts.Text(
			name,
			&defaultFace,
			&widget.ButtonTextColor{
				Idle: colornames.Gainsboro,
			},
		),
		widget.ButtonOpts.TextProcessBBCode(false),
		widget.ButtonOpts.ClickedHandler(handler),
	)
}

func (g *Game) createScenUI() {
	root := widget.NewContainer(
		widget.ContainerOpts.BackgroundImage(image.NewNineSliceColor(colornames.Green)),
	)
	g.sceneUI.Container = root
}

// Draw renders the game
func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(colornames.Black)
	switch g.state {
	case StateSelect:
		g.selectUI.Draw(screen)
	case StatePlaying:
		g.updateTitle()
		g.sceneUI.Draw(screen)
	case StateWin:
		g.drawGame(screen)
		g.drawWin(screen)
	case StateLose:
		g.drawGame(screen)
		g.drawLose(screen)
	}
}

func (g *Game) updateTitle() {
	g.sceneUI.Container.RemoveChild(g.titleContainer)
	g.titleContainer.RemoveChildren()
	label := widget.NewLabel(
		widget.LabelOpts.Text(
			fmt.Sprintf(
				"ICE %d-%d",
				g.levelsManager.CurrentSection().ID+1, g.levelsManager.CurrentLevel().ID+1,
			),
			&defaultFace,
			&widget.LabelColor{
				Idle:     colornames.Orange,
				Disabled: colornames.Orange,
			},
		),
	)
	g.titleContainer.AddChild(label)
	g.sceneUI.Container.AddChild(g.titleContainer)
}

func DefaultFont() text.Face {
	s, err := text.NewGoTextFaceSource(bytes.NewReader(goregular.TTF))
	if err != nil {
		panic(err)
	}
	return &text.GoTextFace{
		Source: s,
		Size:   20,
	}
}
