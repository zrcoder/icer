# ICER TypeScript Game Requirements Documentation

## 1. Game Overview

### 1.1 Game Name
ICER - 2D Puzzle Game (Web-Based)

### 1.2 Game Type
Grid-based 2D puzzle game combining physics simulation and strategic planning, built for modern web browsers

### 1.3 Game Objective
Player controls ICER to extinguish all flames by creating and manipulating ice blocks, completing level challenges

## 2. Game World

### 2.1 World Structure
- Vertical plane grid system
- Each grid cell can contain one object
- Support for multi-layer height structures
- Rendered in browser canvas with hardware acceleration

### 2.2 Grid Specifications
- Standard level size: 20x15 grid
- Adjustable based on level requirements
- Coordinate system: (0,0) at bottom-left corner
- Grid size: 40px per cell (responsive scaling)

## 3. Game Characters and Objects

### 3.1 Main Character ICER
- **Movement**: Left/right movement (J/L keys or arrow keys)
- **Jumping**: Can jump 1 cell over obstacles (Space key)
- **Special Ability**: Create/remove ice blocks (A/D keys)
- **Ice Creation**: Left/bottom and right/bottom adjacent cells

### 3.2 Object Types

#### 3.2.1 Wall (WALL)
- **Properties**: Fixed obstacle, impassable
- **Interaction**: Can jump 1 cell higher
- **Characteristics**: Immovable, indestructible
- **Rendering**: Dark gray rectangle with brick pattern

#### 3.2.2 Ice Block (ICE_BLOCK)
- **Properties**: Createable, pushable, destructible
- **States**: Firm/unfirm state
- **Physics**: Smooth surface, slides when pushed
- **Creation Limit**: Cannot be placed directly on burning hot pot
- **Rendering**: Light blue with transparency effects when melting

#### 3.2.3 Stone (STONE)
- **Properties**: Pushable, heat resistant
- **Physics**: Rough surface, moves only 1 cell when pushed
- **Special**: Can be placed on hot pot
- **Rendering**: Gray with irregular stone shape

#### 3.2.4 Flame (FLAME)
- **Properties**: Target elimination object
- **Elimination**: Extinguished by ice block contact
- **Characteristics**: Ice blocks above won't melt
- **Rendering**: Red with animated flicker effect

#### 3.2.5 Pot (POT)
- **Ice Pot**: Initial state, can be ignited
- **Hot Pot**: Permanently heated after ignition
- **Interaction**: Player cannot stand on hot pot
- **Conversion**: Ice pot → Hot pot when touched by flame
- **Rendering**: White (cold) or orange (hot) with steam effects

#### 3.2.6 Portal (PORTAL)
- **Function**: Two-way teleportation
- **Usage**: Player position must be at least 1 level below portal
- **Characteristics**: Different shapes and lengths
- **Rendering**: Green with glowing animation and swirl effects

## 4. Game Rules

### 4.1 Basic Rules

#### 4.1.1 Win Condition
- Extinguish all flames to complete level

#### 4.1.2 Movement Rules
- Left/right movement: J/L keys or left/right arrow keys
- Jumping: Automatic 1-cell jump over obstacles
- Collision detection: Stop movement when encountering obstacles

#### 4.1.3 Ice Block Operations
- Create ice: A key (left/bottom), D key (right/bottom)
- Remove ice: Same key when ice already exists at position
- Position limit: Only adjacent left/bottom and right/bottom positions

### 4.2 Physics Rules

#### 4.2.1 Firm State Determination
Ice block is "firm" when:
- Ice block built next to another object left/right, OR
- Ice block has object support below

#### 4.2.2 Movement Properties
- **Ice Block**: Smooth surface, continues sliding after push until hitting obstacle or falling
- **Stone Block**: Rough surface, moves only 1 cell distance when pushed
- **Special Case**: Stone on ice block continues sliding until hitting rough surface

#### 4.2.3 Falling Rules
- Unfirm ice blocks will fall
- Fall until hitting fixed object or reaching bottom
- May trigger chain reactions

#### 4.2.4 Push Limits
- Can only push single ice block or stone with no adjacent objects
- Two or more connected ice blocks/stones cannot be pushed

### 4.3 Special Rules

#### 4.3.1 Pot Interactions
- Ice blocks cannot be placed directly on burning hot pot (will disappear)
- Ice blocks can be placed at higher positions than hot pot
- Stone blocks can be placed on hot pot

#### 4.3.2 Portal Usage
- Player can enter portal when at least 1 level below
- Teleport to other portal exit
- Maintain relative height relationship

#### 4.3.3 Weight Support
- Ice blocks or player above can support unlimited weight
- No weight support limits to consider

## 5. Game Mechanics

### 5.1 Strategy Elements
- **Platform Building**: Use ice blocks to form steps to reach higher places
- **Ice Bridge Construction**: Connect ice blocks to form paths to other areas
- **Object Combinations**: Utilize various ice block configurations to achieve goals
- **Resource Management**: Efficient use of limited ice block creation opportunities

### 5.2 Level Design Principles
- **Progressive Tutorial**: Gradually guide players through learning game rules
- **Increasing Complexity**: Multiple solution possibilities with escalating difficulty
- **Not All Objects Required**: Encourage creative problem-solving approaches

## 6. Technical Requirements

### 6.1 Technology Stack
- **Language**: TypeScript 5.0+
- **Rendering**: PIXI.js 7.3.2+ (WebGL)
- **Build System**: Vite 4.2.1+
- **Development Environment**: VS Code + TypeScript

### 6.2 Performance Requirements
- **Frame Rate**: 60 FPS target
- **Response Time**: Input delay < 100ms
- **Memory Usage**: < 100MB
- **Bundle Size**: < 2MB for production build

### 6.3 Input Support
- **Keyboard**: J/L (movement), A/D (ice operations), Arrow keys (alternate movement)
- **Accessibility**: Configurable key bindings support
- **Touch**: Planned mobile touch controls

## 7. User Interface

### 7.1 Game Interface
- **Main Game Area**: Grid-based game world with responsive scaling
- **Status Display**: Current level, operation hints
- **Control Instructions**: Keyboard operation guide
- **Responsive Design**: Adapts to different screen sizes

### 7.2 Level Interface
- **Level Selection**: Unlocked level list
- **Progress Display**: Completion status
- **Difficulty Indicators**: Level difficulty labels
- **Performance Tracking**: Best times and move counts

## 8. Level Design

### 8.1 Level Structure
- **Tutorial Levels**: 3-5 levels, gradually introduce game mechanics
- **Basic Levels**: 10-15 levels, master core gameplay
- **Advanced Levels**: 15-20 levels, complex strategic challenges
- **Expert Levels**: 5-10 levels, high-diculty puzzles

### 8.2 Level Elements
- **Grid Size**: Adjusted based on difficulty
- **Object Configuration**: Different types and quantities of objects
- **Goal Setting**: Flame positions and quantities
- **Solution Paths**: Primary and alternative solution methods

## 9. Development Milestones

### 9.1 First Phase - Basic Framework
- Game window and rendering system
- Grid coordinate system
- Basic input handling

### 9.2 Second Phase - Core Gameplay
- Character movement and jumping
- Ice block creation/removal
- Basic object types

### 9.3 Third Phase - Physics System
- Push and fall mechanics
- Slide and firm state
- Object interaction

### 9.4 Fourth Phase - Game Rules
- Flame elimination system
- Pot heating mechanism
- Portal functionality

### 9.5 Fifth Phase - Polish & Optimization
- Level system
- UI interface
- Testing and debugging

## 10. Quality Assurance

### 10.1 Testing Requirements
- **Functional Testing**: All game mechanics work correctly
- **Boundary Testing**: Edge case handling
- **Performance Testing**: Smooth operation
- **User Experience**: Intuitive controls, clear feedback

### 10.2 Acceptance Criteria
- All core functionality implemented
- No serious bugs
- Smooth game experience
- Complete tutorial levels

---

## Browser Compatibility

### Minimum Requirements
- **Chrome 90+**
- **Firefox 88+**
- **Safari 14+**
- **Edge 90+**

### Recommended Requirements
- **Chrome 100+**
- **Hardware acceleration enabled**
- **Modern device with GPU support**

---

**Documentation Version**: 2.0  
**Migration Date**: January 2025  
**Last Updated**: January 2025  

*This document describes the requirements for the TypeScript web-based version of ICER, focusing on modern browser implementation with enhanced performance and cross-platform compatibility.*