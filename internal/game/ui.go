package game

import (
	"bytes"
	"image/color"
	"math"
	"strconv"

	"github.com/ebitenui/ebitenui/image"
	"github.com/ebitenui/ebitenui/widget"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/text/v2"
	"github.com/hajimehoshi/ebiten/v2/vector"
	"github.com/zrcoder/icer/internal/levels/sections"
	"golang.org/x/image/colornames"
	"golang.org/x/image/font/gofont/goregular"
)

var defaultFace = DefaultFont()

func (g *Game) initUI() {
	g.initSelectUI()
}

func (g *Game) initSelectUI() {
	root := widget.NewContainer(
		widget.ContainerOpts.Layout(widget.NewRowLayout(
			widget.RowLayoutOpts.Direction(widget.DirectionVertical),
			widget.RowLayoutOpts.Spacing(10),
		)),
	)
	titleLabel := widget.NewLabel(
		widget.LabelOpts.Text(
			"ICER - Level Selection",
			&defaultFace,
			&widget.LabelColor{
				Idle: colornames.White,
			}),
	)
	root.AddChild(titleLabel)
	root.AddChild(g.createSectionContainer())
	root.AddChild(g.createLevelContainer())
	g.selectUI.Container = root
}

func (g *Game) createSectionContainer() *widget.Container {
	return createSectionLevelContainer("Section", sections.Count, func(i int) {
		g.levelsManager.SetCurrentSection(i)
	})
}

func (g *Game) createLevelContainer() *widget.Container {
	return createSectionLevelContainer("Level", len(g.levelsManager.CurrentSection().Levels), func(i int) {
		g.levelsManager.SetCurrentLevel(i)
	})
}

func createSectionLevelContainer(title string, count int, buttonClickHander func(int)) *widget.Container {
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
		)),
	)
	for i := range sections.Count {
		body.AddChild(createButton(i+1, func(args *widget.ButtonClickedEventArgs) {
			buttonClickHander(i)
		}))
	}
	container.AddChild(body)
	return container
}

func createButton(i int, handler func(args *widget.ButtonClickedEventArgs)) *widget.Button {
	return widget.NewButton(
		widget.ButtonOpts.Image(&widget.ButtonImage{
			Idle:         DefaultNineSlice(colornames.Darkslategray),
			Hover:        DefaultNineSlice(Mix(colornames.Darkslategray, colornames.Mediumseagreen, 0.4)),
			Disabled:     DefaultNineSlice(Mix(colornames.Darkslategray, colornames.Gainsboro, 0.8)),
			Pressed:      PressedNineSlice(Mix(colornames.Darkslategray, colornames.Black, 0.4)),
			PressedHover: PressedNineSlice(Mix(colornames.Darkslategray, colornames.Black, 0.4)),
		}),
		widget.ButtonOpts.TextLabel(strconv.Itoa(i+1)),
		widget.ButtonOpts.TextFace(&defaultFace),
		widget.ButtonOpts.WidgetOpts(
			widget.WidgetOpts.MinSize(60, 60),
		),
		widget.ButtonOpts.TextColor(&widget.ButtonTextColor{
			Idle:    colornames.Gainsboro,
			Hover:   colornames.Gainsboro,
			Pressed: Mix(colornames.Gainsboro, colornames.Black, 0.4),
		}),
		widget.ButtonOpts.ClickedHandler(handler),
	)
}

// Draw renders the game
func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(color.RGBA{20, 20, 40, 255}) // Dark blue background
	switch g.state {
	case StateSelect:
		g.selectUI.Draw(screen)
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

func DefaultNineSlice(base color.Color) *image.NineSlice {
	var size float32 = 64
	var tiles float32 = 16

	tile := size / tiles

	img := ebiten.NewImage(int(size), int(size))
	vector.DrawFilledRect(img, 0, tile, size, size-tile, colornames.Gainsboro, true)
	vector.DrawFilledRect(img, 0, tile, size, size-tile*2, colornames.Gainsboro, true)
	vector.DrawFilledRect(img, tile, tile*2, size-tile*2, size-tile*4, colornames.Gainsboro, true)

	return image.NewNineSliceBorder(img, int(tile*4))
}

func RoundedRectPath(x, y, w, h, tl, tr, br, bl float32) *vector.Path {
	path := &vector.Path{}

	path.Arc(x+w-tr, y+tr, tr, 3*math.Pi/2, 0, vector.Clockwise)
	path.LineTo(x+w, y+h-br)
	path.Arc(x+w-br, y+h-br, br, 0, math.Pi/2, vector.Clockwise)
	path.LineTo(x+bl, y+h)
	path.Arc(x+bl, y+h-bl, bl, math.Pi/2, math.Pi, vector.Clockwise)
	path.LineTo(x, y+tl)
	path.Arc(x+tl, y+tl, tl, math.Pi, 3*math.Pi/2, vector.Clockwise)
	path.Close()

	return path
}

func PressedNineSlice(base color.Color) *image.NineSlice {
	var size float32 = 64
	var tiles float32 = 16
	tile := size / tiles
	img := ebiten.NewImage(int(size), int(size))
	vector.DrawFilledRect(img, 0, 0, size, size, colornames.Gainsboro, true)
	vector.DrawFilledRect(img, tile, tile, size-tile*2, size-tile*2, colornames.Gainsboro, true)
	return image.NewNineSliceBorder(img, int(tile*4))
}

func Mix(a, b color.Color, percent float64) color.Color {
	rgba := func(c color.Color) (r, g, b, a uint8) {
		r16, g16, b16, a16 := c.RGBA()
		return uint8(r16 >> 8), uint8(g16 >> 8), uint8(b16 >> 8), uint8(a16 >> 8)
	}
	lerp := func(x, y uint8) uint8 {
		return uint8(math.Round(float64(x) + percent*(float64(y)-float64(x))))
	}
	r1, g1, b1, a1 := rgba(a)
	r2, g2, b2, a2 := rgba(b)

	return color.RGBA{
		R: lerp(r1, r2),
		G: lerp(g1, g2),
		B: lerp(b1, b2),
		A: lerp(a1, a2),
	}
}
