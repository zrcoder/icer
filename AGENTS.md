# ICER TypeScript Game Development Guide

This document contains development guidelines and commands for working on the ICER TypeScript ice block puzzle game.

## Development Commands

### Running the Game
```bash
# Development server with hot-reload
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Build and serve locally
npm run build && npm run preview
```

### Development Workflow
```bash
# Type checking
npm run type-check

# Linting code
npm run lint

# Fix linting issues
npm run lint:fix

# Testing
npm test

# Clean build artifacts
npm run clean
```

### Package Management
```bash
# Install dependencies
npm install

# Add new dependency
npm install <package>

# Add dev dependency
npm install -D <package>

# Update dependencies
npm update
```

## Project Structure & Architecture

### Core Architecture
- **TypeScript strict mode** with comprehensive type safety
- **Component-based entity system** with `GameObject` base class
- **Fixed-timestep physics engine** for consistent gameplay
- **Grid-based world system** (20x15 grid by default)
- **State management** through `GameStateManager`
- **Level loading** via ASCII level definitions
- **PIXI.js rendering** for smooth 2D graphics
- **Vite build system** for modern development

### Module Organization
```
src/
├── game/              # Main game loop, state, constants
├── entities/          # Game objects (player, walls, items)
├── physics/           # Physics engine and systems
├── world/             # Grid system and game world
├── levels/            # Level loading and management
├── rendering/         # PIXI.js rendering and UI effects
├── input/             # Input handling system
├── utils/             # Helper classes (Vector2, etc.)
└── rules/             # Game rules and interactions
```

## Code Style Guidelines

### TypeScript Configuration
- **Strict type checking** enabled
- **Path mapping** for clean imports (`@/` shortcuts)
- **ESNext modules** with bundler resolution
- **No implicit any** - all types must be explicit
- **Unused variables** flagged as errors

### Import Organization
```typescript
// Standard library imports first
import { Game, GameObject } from '@/game';
import { Vector2 } from '@/utils';

// Third-party imports
import * as PIXI from 'pixi.js';

// Type imports
import type { GameState } from '@/game/gameState';
import type { Level } from '@/levels/levelManager';
```

### Class Naming & Structure
- Use **PascalCase** for class names (`GameObject`, `PhysicsEngine`)
- Use **camelCase** for methods and variables (`update()`, `gridX`)
- Use **protected/public** modifiers appropriately
- Include comprehensive JSDoc comments for all public methods
- Use **type annotations** for all parameters and return types

### Type Definitions
```typescript
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

class Vector2 {
  constructor(public x: number = 0.0, public y: number = 0.0) {}
  
  add(other: Vector2): Vector2 {
    return new Vector2(this.x + other.x, this.y + other.y);
  }
}
```

### Error Handling
```typescript
// Graceful handling of missing dependencies
import * as PIXI from 'pixi.js';

try {
  const app = new PIXI.Application({
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    backgroundColor: 0x000000
  });
} catch (error) {
  console.error('Failed to initialize PIXI:', error);
  throw new Error('Graphics initialization failed');
}

// Type checking with proper error messages
function addVectors(v1: Vector2, v2: Vector2): Vector2 {
  if (!v1 || !v2) {
    throw new Error('Both vectors must be valid Vector2 instances');
  }
  return new Vector2(v1.x + v2.x, v1.y + v2.y);
}
```

### Game Object Patterns
```typescript
class CustomObject extends GameObject {
  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    // Set object properties
    this.setProperty('solid', true);
    this.setProperty('pushable', false);
    this.setProperty('weight', 1);
  }
  
  getType(): string {
    return "custom_object";
  }
  
  getColor(): number {
    return COLOR_CUSTOM;
  }
  
  update(dt: number): void {
    // Update logic here
    super.update(dt);
  }
  
  onCollision(other: GameObject): void {
    // Handle collision with other object
    super.onCollision(other);
  }
}
```

## Testing Guidelines

### Test Structure
- Use **Jest** for unit and integration tests
- Place tests in `__tests__/` directories next to source files
- Use TypeScript for tests with `ts-jest` preset
- Mock external dependencies (PIXI.js, DOM APIs)

### Test Example
```typescript
// __tests__/utils/vector2.test.ts
import { Vector2 } from '@/utils/vector2';

describe('Vector2', () => {
  test('should create vector with default values', () => {
    const v = new Vector2();
    expect(v.x).toBe(0);
    expect(v.y).toBe(0);
  });

  test('should add two vectors correctly', () => {
    const v1 = new Vector2(1, 2);
    const v2 = new Vector2(3, 4);
    const result = v1.add(v2);
    
    expect(result.x).toBe(4);
    expect(result.y).toBe(6);
  });
});
```

## Development Workflow

### Adding New Game Objects
1. Create new class inheriting from `GameObject` in `src/entities/objects/`
2. Implement required methods: `getType()`, `getColor()`
3. Set appropriate properties (`solid`, `pushable`, `weight`, etc.)
4. Add object color constant to `src/game/constants.ts`
5. Add rendering logic in `src/rendering/gameRenderer.ts`
6. Add level character mapping in `src/levels/levelManager.ts`
7. Update game rules if needed in `src/rules/gameRules.ts`

### Adding New Levels
1. Add level data to `src/levels/levelManager.ts`
2. Follow existing level structure with ASCII characters
3. Set optimal moves and time for scoring
4. Test level loading and gameplay
5. Update level selection if needed

### Physics Integration
- All physics calculations should use the `PhysicsEngine` class
- Object interactions should be handled through `GameRulesSystem`
- Use fixed timestep for consistent physics
- Handle edge cases (boundaries, max speeds, etc.)

## Performance Optimization

### TypeScript Best Practices
- Use **readonly** for immutable data
- Leverage **type inference** where appropriate
- Use **generics** for reusable components
- Enable **strict null checks** and handle nulls explicitly

### Rendering Performance
- **Object pooling** for frequently created objects
- **Batch draw calls** where possible
- **Minimize state changes** in PIXI.js
- Use **delta time** for frame-independent movement

### Memory Management
- **Clean up event listeners** in destroy methods
- **Remove object references** to prevent memory leaks
- **Use weak references** for temporary object storage
- **Monitor memory usage** with browser dev tools

## Code Quality Standards

### Linting Rules
- **No unused variables** - use `_` prefix for unused parameters
- **Explicit returns** - all functions must have return type annotations
- **Consistent naming** - follow TypeScript conventions
- **No implicit any** - all types must be explicit

### Documentation
- All public methods must have JSDoc comments
- Complex algorithms should have inline comments
- Types and interfaces need clear descriptions
- Update README.md when adding major features

## Development Tools

### VS Code Extensions (Recommended)
- **TypeScript Importer** - automatic import management
- **ESLint** - real-time linting feedback
- **Prettier** - code formatting integration
- **GitLens** - enhanced Git capabilities

### Browser Testing
- **Chrome DevTools** - debugging and profiling
- **Firefox Developer Tools** - cross-browser testing
- **Network throttling** - performance testing
- **Mobile emulation** - responsive testing

## Deployment

### Build Process
```bash
# Development build with source maps
npm run build

# Production build (minified)
npm run build -- --mode production

# Analyze bundle size
npm run build -- --analyze
```

### Deployment Targets
- **Static hosting** - GitHub Pages, Netlify, Vercel
- **CDN deployment** - Cloudflare, AWS S3
- **Container deployment** - Docker, Kubernetes
- **PWA** - progressive web app capabilities

## Dependencies
- **pixi.js 7.3.2** - 2D graphics rendering engine
- **typescript 5.0.2** - TypeScript compiler
- **vite 4.2.1** - Build tool and dev server
- **jest 29.5.0** - Testing framework
- **eslint 8.37.0** - Code linting
- **@types/jest 29.5.0** - Jest type definitions

## Troubleshooting

### Common Issues
- **Type errors**: Check tsconfig.json and import paths
- **Module resolution**: Verify package.json and node_modules
- **Performance**: Use browser dev tools profiling
- **Build failures**: Check for circular dependencies

### Debug Mode
```typescript
// Enable debug mode
const DEBUG = process.env.NODE_ENV === 'development';

if (DEBUG) {
  console.log('Debug info:', data);
}
```

### Hot Reload Issues
- Ensure Vite dev server is running
- Check for syntax errors in TypeScript
- Verify file watching is working
- Refresh browser if needed