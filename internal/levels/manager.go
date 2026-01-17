package levels

import (
	"fmt"
	"strings"

	"strconv"

	"github.com/BurntSushi/toml"
	"github.com/charmbracelet/log"
	"github.com/zrcoder/icer/internal/levels/sections"
	"github.com/zrcoder/icer/internal/sprites"
)

type Section struct {
	Meta
	LevelCount int `toml:"levels"`
	levels     []*Level
}

type Level struct {
	Meta
	Grid    string `toml:"grid"`
	grid    [][]sprites.Sprite
	portals map[rune][]*sprites.Portal
}

type Meta struct {
	ID          int    `toml:"-"`
	Title       string `toml:"title"`
	Description string `toml:"description"`
}

type Manager struct {
	Sections       []*Section
	currentLevel   *Level
	currentSection *Section
}

func NewManager() *Manager {
	m := &Manager{}
	m.load()
	log.Debug("levels loaded",
		"sections", len(m.Sections),
		"section", m.currentSection,
	)
	return m
}

func (m *Manager) SetCurrentSection(i int) {
	m.currentSection = m.Sections[i]
	m.currentLevel = m.currentSection.levels[0]
}

func (m *Manager) SetCurrentLevel(i int) {
	m.currentLevel = m.currentSection.levels[i]
}

func (m *Manager) CurrentSection() *Section {
	return m.currentSection
}
func (m *Manager) CurrentLevel() *Level {
	return m.currentLevel
}

func (m *Manager) load() {
	m.Sections = make([]*Section, sections.Count)
	for i := range m.Sections {
		m.Sections[i] = m.loadSection(i)
		m.Sections[i].loadLevels()
		log.Debug("section loaded", "id", i, "title", m.Sections[i].Title, "levels", m.Sections[i].LevelCount)
	}
	m.SetCurrentSection(0)
}

func (m *Manager) loadSection(section int) *Section {
	indexPath := strconv.Itoa(section+1) + "/index.toml"
	indexData, err := sections.FS.ReadFile(indexPath)
	if err != nil {
		log.Fatal(err)
	}

	res := &Section{}
	if err := toml.Unmarshal(indexData, res); err != nil {
		log.Fatal(err)
	}
	res.ID = section
	return res
}

func (s *Section) loadLevels() {
	s.levels = make([]*Level, s.LevelCount)
	for i := range s.LevelCount {
		data, err := sections.FS.ReadFile(fmt.Sprintf("%d/%d.toml", s.ID+1, i+1))
		if err != nil {
			log.Fatal(err)
		}
		var level = &Level{}
		err = toml.Unmarshal(data, &level)
		if err != nil {
			log.Fatal(err)
		}
		level.ID = i
		log.Debug("level loaded", "id", i, "title", level.Title)
		s.levels[i] = level
	}
}

func (s *Section) loadLevel(id int) Level {
	levelPath := strconv.Itoa(s.Meta.ID) + "/" + strconv.Itoa(id) + ".toml"
	levelData, err := sections.FS.ReadFile(levelPath)
	if err != nil {
		log.Fatal(err)
	}

	var level Level
	if err := toml.Unmarshal(levelData, &level); err != nil {
		log.Fatal(err)
	}

	level.regular()

	return level
}

func (l *Level) regular() {
	l.portals = make(map[rune][]*sprites.Portal)
	lines := strings.Split(l.Grid, "\n")
	l.grid = make([][]sprites.Sprite, len(lines))
	for i, line := range lines {
		l.grid[i] = make([]sprites.Sprite, len(line))
		for j, ch := range line {
			l.grid[i][j] = l.createObject(ch, i, j)
		}
	}
}

func (l *Level) createObject(char rune, x, y int) sprites.Sprite {
	switch char {
	case 'M':
		return sprites.NewPlayer(x, y)
	case '#':
		return sprites.NewWall(x, y)
	case 'I':
		return sprites.NewIce(x, y)
	case 'S':
		return sprites.NewStone(x, y)
	case 'F':
		return sprites.NewFlame(x, y)
	case 'P':
		return sprites.NewPot(x, y)
	case '.':
		return nil
	default:
		portal := sprites.NewPortal(char, x, y)
		l.portals[char] = append(l.portals[char], portal)
		return portal
	}
}
