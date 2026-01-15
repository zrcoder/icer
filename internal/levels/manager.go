package levels

import (
	"bytes"
	"fmt"
	"log"
	"strconv"

	"github.com/BurntSushi/toml"
	"github.com/zrcoder/icer/internal/levels/sections"
	"github.com/zrcoder/icer/internal/sprites"
)

type Section struct {
	Meta
	LevelCount int     `toml:"levels"`
	Levels     []Level `toml:"-"`
}

type Level struct {
	Meta
	Grid    []byte `toml:"grid"`
	grid    [][]sprites.Sprite
	portals map[byte][]*sprites.Portal
}

type Meta struct {
	ID          int
	Title       string `toml:"title"`
	Description string `toml:"description"`
}

type Manager struct {
	Sections       []Section
	currentLevel   int
	currentSection int
}

func NewManager() *Manager {
	m := &Manager{}
	m.loadMeta()
	return m
}

func (m *Manager) SetCurrentSection(i int) {
	m.currentSection = i
	m.currentLevel = 0
	m.Sections[i].loadLevels()
}

func (m *Manager) loadMeta() {
	m.Sections = make([]Section, sections.Count)
	for i := range m.Sections {
		m.Sections[i] = m.loadSectionMeta(i)
	}
}

func (m *Manager) loadSectionMeta(section int) Section {
	id := section + 1
	indexPath := strconv.Itoa(id) + "/index.toml"
	indexData, err := sections.FS.ReadFile(indexPath)
	if err != nil {
		log.Fatal(err)
	}

	var meta Meta
	if err := toml.Unmarshal(indexData, &meta); err != nil {
		log.Fatal(err)
	}
	meta.ID = id

	return Section{
		Meta: meta,
	}
}

func (s *Section) loadLevels() {
	s.Levels = make([]Level, s.LevelCount)
	for i := range s.LevelCount {
		data, err := sections.FS.ReadFile(fmt.Sprintf("%d/%d.toml", s.ID, i+1))
		if err != nil {
			log.Fatal(err)
		}
		err = toml.Unmarshal(data, &s.Levels[i])
		if err != nil {
			log.Fatal(err)
		}
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
	l.portals = make(map[byte][]*sprites.Portal)
	lines := bytes.Split(l.Grid, []byte("\n"))
	l.grid = make([][]sprites.Sprite, len(lines))
	for i, line := range lines {
		l.grid[i] = make([]sprites.Sprite, len(line))
		for j, ch := range line {
			l.grid[i][j] = l.createObject(ch, i, j)
		}
	}
}

func (l *Level) createObject(char byte, x, y int) sprites.Sprite {
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
