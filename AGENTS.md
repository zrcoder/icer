# AGENTS.md

This file contains guidelines and commands for agentic coding agents working on the ICER Go project.

## Project Overview

ICER is a 2D ice block puzzle game built with Go and the Ebiten game engine. The project follows standard Go project structure with domain-driven design principles.

## Build, Test, and Lint Commands

### Building
```bash
# Build the main executable
go build -o icer ./main.go

# Build with race detection (for development)
go build -race -o icer ./main.go

# Build for different platforms
GOOS=linux GOARCH=amd64 go build -o icer-linux ./main.go
GOOS=windows GOARCH=amd64 go build -o icer.exe ./main.go
GOOS=darwin GOARCH=amd64 go build -o icer-mac ./main.go
```

### Running
```bash
# Run the game
go run main.go

# Run with verbose logging
go run -v main.go
```

### Testing
```bash
# Run all tests in the project
go test ./...

# Run tests in a specific package
go test ./internal/game
go test ./internal/sprites
go test ./internal/utils
go test ./internal/levels
go test ./internal/physics
go test ./internal/rendering

# Run a single test function
go test -run TestFunctionName ./internal/package

# Run tests with verbose output
go test -v ./...

# Run tests with coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html

# Run benchmarks
go test -bench=. ./...

# Run tests with race detection
go test -race ./...
```

### Code Quality
```bash
# Format all Go files
go fmt ./...

# Run static analysis
go vet ./...

# Run go vet on specific package
go vet ./internal/game

# Run with additional vet checks
go vet -vettool=$(which shadow) ./...

# Format imports
goimports -w .
```

## Project Structure

```
icer/
├── main.go                 # Entry point
├── go.mod                  # Go module definition
├── internal/               # Private application code
│   ├── game/              # Core game logic and state
│   ├── sprites/           # Game objects and entities
│   ├── utils/             # Shared utilities (vectors, helpers)
│   ├── levels/            # Level management and loading
│   ├── physics/           # Physics engine and collision detection
│   └── rendering/         # Rendering and graphics
└── README.md              # Project documentation
```

## Code Style Guidelines

### Import Organization
- Use `goimports` for consistent import formatting
- Group imports in three sections: standard library, third-party, internal
- Sort alphabetically within each group
- Import only what you use

### Naming Conventions
- **Package names**: lowercase, single words, descriptive (`game`, `sprites`, `utils`)
- **Constants**: `UPPER_SNAKE_CASE` for exported constants, `lowerSnakeCase` for unexported
- **Variables**: `camelCase` (exported starts with uppercase, unexported with lowercase)
- **Functions**: `camelCase` following same export rules
- **Interfaces**: Simple, descriptive names ending in "er" (e.g., `Sprite`, `Renderer`)
- **Structs**: `CamelCase`, descriptive nouns

### Type Definitions
- Use meaningful type names
- Prefer composition over inheritance
- Define clear interfaces for contracts between packages
- Use type aliases where appropriate for clarity

### Error Handling
- Always handle errors explicitly
- Use `if err != nil` pattern consistently
- Wrap errors with context using `fmt.Errorf` or custom error types
- Return errors as the last return value
- Log errors at appropriate levels

### Function Design
- Keep functions small and focused (single responsibility)
- Use clear, descriptive names
- Limit parameter count (consider struct for many parameters)
- Return early to reduce nesting
- Document exported functions with Godoc comments

### Constants and Configuration
- Define constants at package level for magic numbers
- Group related constants in blocks
- Use `iota` for enumerated constants
- Configuration should be centralized and documented

## Testing Guidelines

### Test Structure
- Place test files in the same package as the code they test
- Name test files with `_test.go` suffix
- Use descriptive test function names: `TestFunctionName_Condition_ExpectedResult`
- Use table-driven tests for multiple scenarios

### Test Organization
```go
func TestGame_Update_StateTransitions(t *testing.T) {
    tests := []struct {
        name     string
        initialState State
        input    ebiten.Key
        expected State
    }{
        // test cases...
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test implementation
        })
    }
}
```

### Testing Best Practices
- Write unit tests for business logic
- Mock external dependencies (Ebiten engine calls)
- Test both success and failure paths
- Use `testing.T` methods for assertions
- Keep tests fast and deterministic

## Game-Specific Guidelines

### Ebiten Integration
- Follow Ebiten lifecycle patterns
- Handle input in `Update()` method
- Perform rendering in `Draw()` method
- Use consistent coordinate system (grid-based)
- Maintain 60 FPS target

### Component Architecture
- Use interface-based design for game objects
- Implement `Sprite` interface for all game entities
- Separate physics, rendering, and game logic
- Use composition for complex behaviors

### State Management
- Use centralized state management
- Implement clear state transitions
- Handle state updates in `Update()` method
- Render based on current state

## Dependencies

### Required Libraries
- `github.com/hajimehoshi/ebiten/v2` - Main game engine
- `github.com/ebitenui/ebitenui` - UI components
- `github.com/BurntSushi/toml` - Configuration parsing

### Version Management
- Use Go modules for dependency management
- Pin to specific versions for stability
- Update dependencies regularly
- Review dependency changes for breaking changes

## Development Workflow

1. **Before Coding**: Run `go mod tidy` to clean dependencies
2. **During Development**: Use `go fmt ./...` and `go vet ./...` frequently
3. **Before Commit**: Run `go test ./...` to ensure all tests pass
4. **Code Review**: Ensure code follows all style guidelines

## Performance Considerations

- Use object pooling for frequently created/destroyed objects
- Minimize allocations in game loop
- Profile with `go test -bench` for performance bottlenecks
- Use `sync.Pool` for memory management in hot paths

## Debugging

- Use `log.Printf` for debugging output
- Implement debug modes with conditional compilation
- Use Ebiten's debug utilities when appropriate
- Profile with `pprof` for performance analysis