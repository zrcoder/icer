import * as PIXI from 'pixi.js';
import { GameWorld } from '@/world/gameWorld';
import { CELL_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT, GameState } from '@/game/constants';
import { GameObject } from '@/entities/base';
import { GameStateManager } from '@/game/gameState';

/**
 * Main game renderer using PIXI.js
 */
export class GameRenderer {
  private app: PIXI.Application;
  private gameWorld: GameWorld;
  private stateManager: GameStateManager;
  private container: PIXI.Container;
  private gridContainer: PIXI.Container;
  private objectContainer: PIXI.Container;
  private uiContainer: PIXI.Container;

  constructor(canvas: HTMLCanvasElement, gameWorld: GameWorld, stateManager: GameStateManager) {
    this.gameWorld = gameWorld;
    this.stateManager = stateManager;
    
    // Initialize PIXI application
    this.app = new PIXI.Application({
      width: WINDOW_WIDTH,
      height: WINDOW_HEIGHT,
      view: canvas,
      backgroundColor: 0x000000,
      antialias: true,
    });

    // Create containers for different rendering layers
    this.container = new PIXI.Container();
    this.gridContainer = new PIXI.Container();
    this.objectContainer = new PIXI.Container();
    this.uiContainer = new PIXI.Container();

    this.container.addChild(this.gridContainer);
    this.container.addChild(this.objectContainer);
    this.container.addChild(this.uiContainer);
    this.app.stage.addChild(this.container);

    // Initialize grid graphics
    this.createGrid();
  }

  /**
   * Create grid lines
   */
  private createGrid(): void {
    const gridGraphics = new PIXI.Graphics();
    gridGraphics.lineStyle(1, 0x808080, 0.5);

    // Draw vertical lines
    for (let x = 0; x <= GRID_WIDTH; x++) {
      const xPos = x * CELL_SIZE;
      gridGraphics.moveTo(xPos, 0);
      gridGraphics.lineTo(xPos, GRID_HEIGHT * CELL_SIZE);
    }

    // Draw horizontal lines
    for (let y = 0; y <= GRID_HEIGHT; y++) {
      const yPos = y * CELL_SIZE;
      gridGraphics.moveTo(0, yPos);
      gridGraphics.lineTo(GRID_WIDTH * CELL_SIZE, yPos);
    }

    this.gridContainer.addChild(gridGraphics);
  }

  /**
   * Render game objects
   */
  renderObjects(): void {
    // Clear object container
    this.objectContainer.removeChildren();

    // Render each grid cell
    for (const { x, y, object } of this.gameWorld.getGrid()) {
      if (object) {
        this.renderObject(object, x, y);
      }
    }
  }

  /**
   * Render a single game object
   */
  private renderObject(object: GameObject, gridX: number, gridY: number): void {
    const color = object.getColor();
    const x = gridX * CELL_SIZE + 5;
    const y = (GRID_HEIGHT - gridY - 1) * CELL_SIZE + 5;

    // Create sprite for object
    const sprite = new PIXI.Graphics();
    sprite.beginFill(color);
    
    // Draw object as rectangle with rounded corners
    const size = CELL_SIZE - 10;
    
    // Different shapes for different object types
    switch (object.getType()) {
      case 'player':
        this.drawPlayer(sprite, x, y, size, object);
        break;
      case 'wall':
        this.drawWall(sprite, x, y, size);
        break;
      case 'ice_block':
        this.drawIceBlock(sprite, x, y, size, object);
        break;
      case 'flame':
        this.drawFlame(sprite, x, y, size, object);
        break;
      case 'stone':
        this.drawStone(sprite, x, y, size);
        break;
      case 'pot':
        this.drawPot(sprite, x, y, size, object);
        break;
      case 'portal':
        this.drawPortal(sprite, x, y, size, object);
        break;
      default:
        sprite.drawRoundedRect(x, y, size, size, 4);
        break;
    }
    
    sprite.endFill();
    this.objectContainer.addChild(sprite);
  }

  /**
   * Draw player sprite
   */
  private drawPlayer(sprite: PIXI.Graphics, x: number, y: number, size: number, object: GameObject): void {
    // Get animation offset
    const offset = (object as any).getRenderOffset?.(this.stateManager.gameData.timeElapsed) || [0, 0];
    
    sprite.drawCircle(x + size/2 + offset[0], y + size/2 + offset[1], size/2);
    
    // Add eyes
    sprite.beginFill(0xFFFFFF);
    sprite.drawCircle(x + size/3 + offset[0], y + size/3 + offset[1], 2);
    sprite.drawCircle(x + 2*size/3 + offset[0], y + size/3 + offset[1], 2);
    sprite.endFill();
  }

  /**
   * Draw wall sprite
   */
  private drawWall(sprite: PIXI.Graphics, x: number, y: number, size: number): void {
    sprite.drawRoundedRect(x, y, size, size, 2);
    
    // Add brick pattern
    sprite.beginFill(0x303030, 0.3);
    sprite.drawRect(x + 2, y + 2, size - 4, size - 4);
    sprite.endFill();
  }

  /**
   * Draw ice block sprite
   */
  private drawIceBlock(sprite: PIXI.Graphics, x: number, y: number, size: number, object: GameObject): void {
    const melting = (object as any).getMeltingProgress?.() || 0;
    
    // Ice becomes more transparent as it melts
    const alpha = 1 - melting * 0.7;
    sprite.alpha = alpha;
    
    sprite.drawRoundedRect(x, y, size, size, 6);
    
    // Add ice crystal effect
    sprite.beginFill(0xFFFFFF, 0.3);
    sprite.drawCircle(x + size/3, y + size/3, 3);
    sprite.drawCircle(x + 2*size/3, y + 2*size/3, 2);
    sprite.endFill();
  }

  /**
   * Draw flame sprite
   */
  private drawFlame(sprite: PIXI.Graphics, x: number, y: number, size: number, object: GameObject): void {
    const brightness = (object as any).getBrightness?.() || 1;
    const flameHeight = size * (0.8 + brightness * 0.4);
    
    // Draw flame shape
    sprite.moveTo(x + size/2, y + size);
    sprite.lineTo(x + size * 0.3, y + size - flameHeight * 0.3);
    sprite.quadraticCurveTo(x + size * 0.2, y + size - flameHeight * 0.7, x + size/2, y + size - flameHeight);
    sprite.quadraticCurveTo(x + size * 0.8, y + size - flameHeight * 0.7, x + size * 0.7, y + size - flameHeight * 0.3);
    sprite.lineTo(x + size/2, y + size);
    
    // Add glow effect
    sprite.beginFill(0xFFA500, brightness * 0.5);
    sprite.drawCircle(x + size/2, y + size/2, size/2);
    sprite.endFill();
  }

  /**
   * Draw stone sprite
   */
  private drawStone(sprite: PIXI.Graphics, x: number, y: number, size: number): void {
    // Draw irregular stone shape
    sprite.moveTo(x + size * 0.3, y + size);
    sprite.lineTo(x, y + size * 0.6);
    sprite.lineTo(x + size * 0.1, y + size * 0.3);
    sprite.lineTo(x + size * 0.4, y);
    sprite.lineTo(x + size * 0.7, y + size * 0.1);
    sprite.lineTo(x + size, y + size * 0.4);
    sprite.lineTo(x + size * 0.9, y + size * 0.8);
    sprite.closePath();
  }

  /**
   * Draw pot sprite
   */
  private drawPot(sprite: PIXI.Graphics, x: number, y: number, size: number, object: GameObject): void {
    const isHot = object.getProperty('is_hot', false);
    const color = isHot ? 0xFFA500 : 0xFFFFFF;
    
    // Change color if hot/cold
    sprite.beginFill(color);
    
    // Draw pot shape
    sprite.drawRoundedRect(x + size * 0.1, y + size * 0.2, size * 0.8, size * 0.7, 4);
    
    // Draw pot handles
    sprite.drawRect(x - 2, y + size * 0.4, 4, size * 0.2);
    sprite.drawRect(x + size - 2, y + size * 0.4, 4, size * 0.2);
    
    sprite.endFill();
    
    // Add steam effect if hot
    if (isHot) {
      sprite.beginFill(0xFFFFFF, 0.3);
      for (let i = 0; i < 3; i++) {
        const steamX = x + size * (0.3 + i * 0.2);
        const steamY = y + size * 0.1;
        const steamSize = 2 + i;
        sprite.drawCircle(steamX, steamY, steamSize);
      }
      sprite.endFill();
    }
  }

  /**
   * Draw portal sprite
   */
  private drawPortal(sprite: PIXI.Graphics, x: number, y: number, size: number, object: GameObject): void {
    // const cooldown = (object as any).getCooldownProgress?.() || 0; // Reserved for future portal features
    const ready = (object as any).isReady?.();
    
    // Draw portal as glowing circle
    sprite.alpha = ready ? 1 : 0.5;
    sprite.drawCircle(x + size/2, y + size/2, size/2);
    
    // Add inner glow
    sprite.beginFill(0x00FF00, ready ? 0.6 : 0.3);
    sprite.drawCircle(x + size/2, y + size/2, size/3);
    sprite.endFill();
    
    // Add swirl effect
    const swirlRotation = Date.now() * 0.002;
    sprite.beginFill(0x80FF80, ready ? 0.4 : 0.2);
    for (let i = 0; i < 3; i++) {
      const angle = swirlRotation + (i * Math.PI * 2 / 3);
      const swirlX = x + size/2 + Math.cos(angle) * size/4;
      const swirlY = y + size/2 + Math.sin(angle) * size/4;
      sprite.drawCircle(swirlX, swirlY, 3);
    }
    sprite.endFill();
  }

  /**
   * Render UI elements
   */
  renderUI(): void {
    this.uiContainer.removeChildren();

    if (this.stateManager.isState(GameState.PLAYING)) {
      this.renderGameUI();
    } else if (this.stateManager.isState(GameState.MENU)) {
      this.renderMenu();
    } else if (this.stateManager.isState(GameState.PAUSED)) {
      this.renderPauseOverlay();
    } else if (this.stateManager.isState(GameState.WIN)) {
      this.renderWinScreen();
    } else if (this.stateManager.isState(GameState.LOSE)) {
      this.renderLoseScreen();
    }
  }

  /**
   * Render game UI
   */
  private renderGameUI(): void {
    // Create UI panel
    const uiPanel = new PIXI.Graphics();
    uiPanel.beginFill(0x282828, 0.8);
    uiPanel.drawRoundedRect(10, 10, 250, 100, 5);
    uiPanel.endFill();
    this.uiContainer.addChild(uiPanel);

    // Create text style
    const textStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 14,
      fill: 0xFFFFFF,
    });

    // Level info
    const levelName = "Ice Bridge"; // TODO: Get from level manager
    const levelText = new PIXI.Text(`Level: ${levelName}`, textStyle);
    levelText.position.set(20, 20);
    this.uiContainer.addChild(levelText);

    // Moves counter
    const movesText = new PIXI.Text(`Moves: ${this.stateManager.gameData.moves}`, textStyle);
    movesText.position.set(20, 45);
    this.uiContainer.addChild(movesText);

    // Timer
    const timeText = new PIXI.Text(`Time: ${this.stateManager.gameData.timeElapsed.toFixed(1)}s`, textStyle);
    timeText.position.set(20, 70);
    this.uiContainer.addChild(timeText);

    // Flame counter
    const flameCount = this.gameWorld.countObjectsOfType('flame');
    const flameText = new PIXI.Text(`Flames: ${flameCount}`, {
      ...textStyle,
      fill: 0xFF0000
    });
    flameText.position.set(150, 45);
    this.uiContainer.addChild(flameText);

    // Objective hint
    if (flameCount > 0) {
      const hintText = new PIXI.Text("Extinguish all flames!", {
        ...textStyle,
        fill: 0xC8C8C8
      });
      hintText.position.set(150, 70);
      this.uiContainer.addChild(hintText);
    }
  }

  /**
   * Render menu screen
   */
  private renderMenu(): void {
    // Background gradient
    const background = new PIXI.Graphics();
    for (let i = 0; i < WINDOW_HEIGHT; i += 2) {
      const colorValue = Math.floor(20 + (40 * i / WINDOW_HEIGHT));
      background.beginFill((colorValue << 16) | (colorValue << 8) | (colorValue + 10));
      background.drawRect(0, i, WINDOW_WIDTH, 2);
    }
    this.uiContainer.addChild(background);

    // Title
    const titleStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 48,
      fill: 0x0064FF,
      fontWeight: 'bold',
      dropShadow: true,
      dropShadowColor: 0x141414,
      dropShadowDistance: 3
    });

    const title = new PIXI.Text('ICER', titleStyle);
    title.anchor.set(0.5);
    title.position.set(WINDOW_WIDTH / 2, 50);
    this.uiContainer.addChild(title);

    // Subtitle
    const subtitleStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 20,
      fill: 0xFFFFFF,
    });

    const subtitle = new PIXI.Text('Ice Block Puzzle Game', subtitleStyle);
    subtitle.anchor.set(0.5);
    subtitle.position.set(WINDOW_WIDTH / 2, 100);
    this.uiContainer.addChild(subtitle);

    // Instructions
    const instructionStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 16,
      fill: 0xFFFFFF,
    });

    const instructions = new PIXI.Text('Press ENTER to start with Level 1-1', instructionStyle);
    instructions.anchor.set(0.5);
    instructions.position.set(WINDOW_WIDTH / 2, 250);
    this.uiContainer.addChild(instructions);

    // Quick play instructions
    const quickStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 14,
      fill: 0xAAAAAA,
    });

    const quickPlay = new PIXI.Text('Number keys 1-6: Quick play levels (when unlocked)', quickStyle);
    quickPlay.anchor.set(0.5);
    quickPlay.position.set(WINDOW_WIDTH / 2, 280);
    this.uiContainer.addChild(quickPlay);
  }

  /**
   * Render pause overlay
   */
  private renderPauseOverlay(): void {
    // Semi-transparent overlay
    const overlay = new PIXI.Graphics();
    overlay.beginFill(0x000000, 0.5);
    overlay.drawRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);
    overlay.endFill();
    this.uiContainer.addChild(overlay);

    // Pause text
    const pauseStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 36,
      fill: 0xFFFFFF,
    });

    const pauseText = new PIXI.Text('PAUSED', pauseStyle);
    pauseText.anchor.set(0.5);
    pauseText.position.set(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2);
    this.uiContainer.addChild(pauseText);

    // Resume instruction
    const resumeStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 18,
      fill: 0xFFFFFF,
    });

    const resumeText = new PIXI.Text('Press ESC to resume', resumeStyle);
    resumeText.anchor.set(0.5);
    resumeText.position.set(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50);
    this.uiContainer.addChild(resumeText);
  }

  /**
   * Render win screen
   */
  private renderWinScreen(): void {
    // TODO: Implement win screen
    const winStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 36,
      fill: 0x00FF00,
    });

    const winText = new PIXI.Text('🎉 LEVEL COMPLETE! 🎉', winStyle);
    winText.anchor.set(0.5);
    winText.position.set(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2);
    this.uiContainer.addChild(winText);
  }

  /**
   * Render lose screen
   */
  private renderLoseScreen(): void {
    // TODO: Implement lose screen
    const loseStyle = new PIXI.TextStyle({
      fontFamily: 'Arial',
      fontSize: 36,
      fill: 0xFF0000,
    });

    const loseText = new PIXI.Text('GAME OVER', loseStyle);
    loseText.anchor.set(0.5);
    loseText.position.set(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2);
    this.uiContainer.addChild(loseText);
  }

  /**
   * Get PIXI application instance
   */
  getApp(): PIXI.Application {
    return this.app;
  }

  /**
   * Resize renderer
   */
  resize(width: number, height: number): void {
    this.app.renderer.resize(width, height);
  }

  /**
   * Destroy renderer
   */
  destroy(): void {
    this.app.destroy(true, { children: true });
  }
}