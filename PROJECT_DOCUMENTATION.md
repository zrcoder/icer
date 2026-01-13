# ICER TypeScript Project Documentation

## 📋 Overview

ICER is a TypeScript-based ice block puzzle game that demonstrates modern web game development with type-safe architecture, component-based design, and cross-browser compatibility.

## 🏗️ Architecture Overview

### Design Principles
- **Type Safety**: Comprehensive TypeScript definitions prevent runtime errors
- **Component-Based**: Modular game objects with inheritance and composition
- **Separation of Concerns**: Clear boundaries between rendering, physics, input, and game logic
- **Performance-Oriented**: Fixed-timestep physics and efficient rendering with PIXI.js

### Core Systems

#### 1. Game Loop & State Management
- **Location**: `src/game/`
- **Key Classes**: `Game`, `GameStateManager`
- **Responsibilities**: 
  - Main game loop with fixed timestep
  - State transitions (Menu, Playing, Paused, Win, Lose)
  - Game data tracking (moves, time, progress)

#### 2. Entity System
- **Location**: `src/entities/`
- **Key Classes**: `GameObject`, `Player`, `Wall`, `IceBlock`, etc.
- **Design Pattern**: 
  - Base `GameObject` class with common properties
  - Specialized subclasses for each object type
  - Property-based configuration system

#### 3. Physics Engine
- **Location**: `src/physics/`
- **Key Classes**: `PhysicsEngine`, `IceBlockSystem`, `PushSystem`
- **Features**:
  - Gravity simulation
  - Collision detection and response
  - Object pushing with weight constraints
  - Specialized ice block lifecycle management

#### 4. World Management
- **Location**: `src/world/`
- **Key Classes**: `GameWorld`
- **Responsibilities**:
  - Grid-based spatial organization
  - Object placement and movement
  - Boundary checking
  - Efficient object queries

#### 5. Rendering System
- **Location**: `src/rendering/`
- **Key Classes**: `GameRenderer`
- **Technology**: PIXI.js for hardware-accelerated 2D graphics
- **Features**:
  - Layered rendering (grid, objects, UI)
  - Animated sprites and effects
  - Responsive UI components

#### 6. Input Handling
- **Location**: `src/input/`
- **Key Classes**: `InputHandler`
- **Capabilities**:
  - Keyboard input with customizable bindings
  - Action callback system
  - State management (pressed, just-pressed, just-released)

#### 7. Level System
- **Location**: `src/levels/`
- **Key Classes**: `LevelManager`, `Level`
- **Features**:
  - ASCII-based level definitions
  - Built-in levels with progression
  - Level completion tracking
  - Extensible for custom levels

#### 8. Game Rules
- **Location**: `src/rules/`
- **Key Classes**: `GameRulesSystem`
- **Responsibilities**:
  - Object interaction logic
  - Environmental effects
  - Win/lose condition checking
  - Special game mechanics

## 🎮 Game Mechanics

### Core Interactions

#### Ice Blocks
- **Creation**: A/D keys create ice blocks adjacent to player
- **Properties**: Pushable, extinguishes flames, melts near heat
- **Melting**: Gradual transparency increase when near heat sources
- **Interaction**: Extinguishes flames on contact

#### Flames
- **Objective**: Primary win condition - extinguish all flames
- **Behavior**: Animated flickering effect
- **Interactions**: 
  - Extinguished by ice blocks and cold pots
  - Ignites cold pots on contact
  - Spreads to flammable objects

#### Pots
- **Two Types**: Cold (white) and Hot (orange)
- **Temperature Exchange**: 
  - Cold → Hot when touched by flame
  - Hot → Cold when ice block placed on it
- **Visual Feedback**: Steam particles for hot pots

#### Portals
- **Mechanic**: Instant teleportation between paired portals
- **Cooldown**: 1-second delay between uses
- **Compatibility**: Teleports player, ice blocks, stones, pots

#### Stones
- **Properties**: Heavy pushable objects
- **Weight**: 3 units (compared to ice block's 1 unit)
- **Function**: Crush fragile objects, solve weight-based puzzles

### Physics System

#### Gravity
- **Fixed Timestep**: 60 FPS physics updates for consistency
- **Fall Mechanics**: Objects fall when no support below
- **Terminal Velocity**: Maximum fall speed to prevent tunneling

#### Collision Detection
- **Grid-Based**: Simple position checking for efficiency
- **Collision Response**: Object-specific reactions
- **Layer System**: Ground check for movement validation

#### Push System
- **Force-Based**: Objects can push if weight allows
- **Distance Limits**: Configurable push distance per object
- **Chain Reactions**: Pushes can trigger additional pushes

## 🔧 Development Guide

### Project Setup

#### Prerequisites
```bash
# Node.js 16+ and npm 8+
node --version
npm --version
```

#### Installation
```bash
# Clone and navigate to project
cd ts-icer
npm install
```

#### Development Workflow
```bash
# Start development server with hot reload
npm run dev

# Type checking during development
npm run type-check

# Linting for code quality
npm run lint

# Build for production
npm run build
```

### Code Organization

#### Module Structure
```typescript
// Clean import structure
import { GameObject } from '@/entities/base';
import { Vector2 } from '@/utils/vector2';
import { GameState } from '@/game/gameState';
```

#### Class Design Patterns
```typescript
// Base class with protected properties
export abstract class GameObject {
  constructor(public gridX: number = 0, public gridY: number = 0) {
    // Initialize common properties
  }
  
  // Abstract methods for implementation
  abstract getType(): string;
  abstract getColor(): number;
  
  // Virtual methods for optional override
  update(dt: number): void {}
  onCollision(other: GameObject): void {}
}
```

### Type Safety

#### Interface Definitions
```typescript
// Comprehensive type definitions
interface GameData {
  moves: number;
  timeElapsed: number;
  levelCompleted: boolean;
  bestMoves: number;
  bestTime: number;
}

enum GameState {
  MENU = 'menu',
  PLAYING = 'playing',
  PAUSED = 'paused',
  WIN = 'win',
  LOSE = 'lose'
}
```

#### Property-Based Configuration
```typescript
// Flexible object configuration
class IceBlock extends GameObject {
  constructor(x: number, y: number) {
    super(x, y);
    this.setProperty('solid', true);
    this.setProperty('pushable', true);
    this.setProperty('fragile', true);
    this.setProperty('weight', 1);
  }
}
```

## 🎨 Rendering System

### PIXI.js Integration
- **Canvas Setup**: 800x600 game window with responsive scaling
- **Layer Architecture**: 
  - Background layer for gradients and effects
  - Grid layer for visual guides
  - Object layer for game entities
  - UI layer for interface elements

### Object Rendering
```typescript
// Dynamic rendering based on object type
renderObject(object: GameObject, gridX: number, gridY: number): void {
  switch (object.getType()) {
    case 'player':
      this.drawPlayer(object, gridX, gridY);
      break;
    case 'flame':
      this.drawFlame(object, gridX, gridY);
      break;
    // ... other cases
  }
}
```

### Animation System
- **Frame-Based**: deltaTime-based animations for smooth motion
- **Object-Specific**: Each object type handles its own animations
- **Performance**: Efficient sprite pooling and batch rendering

## 🧪 Testing Strategy

### Unit Testing
```typescript
// Component testing with Jest
describe('Vector2', () => {
  test('should add vectors correctly', () => {
    const v1 = new Vector2(1, 2);
    const v2 = new Vector2(3, 4);
    const result = v1.add(v2);
    
    expect(result.x).toBe(4);
    expect(result.y).toBe(6);
  });
});
```

### Integration Testing
- **Game Loop**: Test state transitions and update cycles
- **Physics**: Validate collision detection and response
- **Level Loading**: Ensure proper level initialization

### Performance Testing
- **Profiling**: Monitor frame rates and memory usage
- **Stress Testing**: Test with maximum object counts
- **Cross-Browser**: Verify compatibility across browsers

## 🚀 Deployment

### Build Process
```bash
# Development build with source maps
npm run build

# Production build (minified and optimized)
npm run build -- --mode production
```

### Distribution Targets
- **Static Hosting**: GitHub Pages, Netlify, Vercel
- **CDN Deployment**: Cloudflare Workers, AWS S3
- **PWA**: Progressive Web App capabilities

### Browser Compatibility
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+
- **ES2020**: Modern JavaScript features with polyfills
- **WebGL**: Hardware acceleration for PIXI.js

## 🔍 Debugging

### Development Tools
```typescript
// Debug mode configuration
const DEBUG = process.env.NODE_ENV === 'development';

if (DEBUG) {
  console.log('Debug info:', gameState);
  window.game = game; // Expose for debugging
}
```

### Common Issues
- **Type Errors**: Check tsconfig.json path mappings
- **Module Resolution**: Verify package.json dependencies
- **Performance**: Use browser DevTools profiler
- **Memory**: Monitor object pooling and cleanup

## 📈 Performance Optimizations

### Rendering Optimizations
- **Object Pooling**: Reuse objects instead of creating/destroying
- **Batch Operations**: Group similar rendering operations
- **Culling**: Only render visible objects
- **LOD**: Level-of-detail for distant objects

### Physics Optimizations
- **Spatial Partitioning**: Grid-based collision detection
- **Sleep Objects**: Skip updates for stationary objects
- **Broad Phase**: Quick collision filtering before detailed checks

### Memory Management
- **Cleanup**: Proper destruction of event listeners
- **References**: Avoid memory leaks with careful reference management
- **Garbage Collection**: Minimize object creation in hot paths

## 🔄 Future Enhancements

### Planned Features
- **Custom Level Editor**: Web-based level creation tool
- **Multiplayer**: Real-time collaborative puzzle solving
- **Achievements**: Progress tracking and unlockables
- **Themes**: Visual themes and customizations

### Technical Improvements
- **WebGL Shaders**: Advanced visual effects
- **Audio System**: Sound effects and background music
- **Save System**: Cloud-based progress synchronization
- **Mobile Support**: Touch controls and responsive design

---

This documentation provides a comprehensive guide to the ICER TypeScript project architecture, development practices, and future roadmap for continued development and maintenance.