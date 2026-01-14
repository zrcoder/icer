import { GameWorld } from '@/world/gameWorld';
import { Player } from '@/entities';
import { PhysicsEngine, IceBlockSystem, PushSystem } from '@/physics';
import { GameStateManager, GameState } from '@/game/gameState';
import { InputHandler } from '@/input';
import { GameRenderer } from '@/rendering/gameRenderer';
import { LevelManager } from '@/levels/levelManager';
import { GameRulesSystem } from '@/rules/gameRules';
import { GRID_WIDTH, GRID_HEIGHT } from '@/game/constants';

/**
 * Main game class
 */
export class Game {
  private canvas: HTMLCanvasElement;
  private gameWorld: GameWorld;
  private stateManager: GameStateManager;
  private inputHandler: InputHandler;
  private renderer: GameRenderer;
  
  private physicsEngine: PhysicsEngine;
  private iceSystem: IceBlockSystem;
  private pushSystem: PushSystem;
  private levelManager: LevelManager;
  private gameRules: GameRulesSystem;
  
  private player: Player | null = null;
  private isRunning: boolean = true;
  private lastTime: number = 0;
  // private _accumulator: number = 0; // Reserved for future physics implementation

constructor() {
    // Initialize canvas
    this.canvas = document.getElementById('game-canvas') as HTMLCanvasElement;
    if (!this.canvas) {
      throw new Error('Game canvas not found');
    }

    // Hide loading message
    const loading = document.getElementById('loading');
    if (loading) {
      loading.classList.add('hidden');
    }

    // Initialize game systems
    this.gameWorld = new GameWorld(GRID_WIDTH, GRID_HEIGHT);
    this.stateManager = new GameStateManager();
    this.inputHandler = new InputHandler();
    this.renderer = new GameRenderer(this.canvas, this.gameWorld, this.stateManager);
     
    // Initialize physics systems
    this.physicsEngine = new PhysicsEngine(this.gameWorld);
    this.iceSystem = new IceBlockSystem();
    this.pushSystem = new PushSystem(this.gameWorld, this.physicsEngine);

    // Initialize rules system first
    this.gameRules = new GameRulesSystem(this.gameWorld, this.physicsEngine, this.iceSystem);
    
    // Initialize level system
    this.levelManager = new LevelManager(this.gameWorld, this.gameRules, this.physicsEngine, this.iceSystem);

    // Setup input callbacks
    this.setupInputCallbacks();
    
    // Initialize game asynchronously
    this.initializeGame().then(() => {
      // Start game loop after initialization
      this.start();
    });
  }

  /**
   * Setup input callbacks
   */
  private setupInputCallbacks(): void {
    this.inputHandler.bindActionCallback('pause', () => {
      if (this.stateManager.isState(GameState.PLAYING)) {
        this.stateManager.changeState(GameState.PAUSED);
      } else if (this.stateManager.isState(GameState.PAUSED)) {
        this.stateManager.changeState(GameState.PLAYING);
      }
    });

    this.inputHandler.bindActionCallback('menu', () => {
      if (this.stateManager.isState(GameState.PLAYING)) {
        this.stateManager.changeState(GameState.MENU);
      } else if (this.stateManager.isState(GameState.MENU)) {
        this.stateManager.changeState(GameState.PLAYING);
      }
    });

    this.inputHandler.bindActionCallback('restart', () => {
      if (this.stateManager.isState(GameState.PLAYING)) {
        this.resetLevel();
      }
    });

    this.inputHandler.bindActionCallback('quit', () => {
      this.quit();
    });
  }

  /**
   * Initialize game and load level for quick start
   */
  private async initializeGame(): Promise<void> {
    // Preload first level for quick start (section 1, level 1)
    await this.levelManager.loadLevel(1, 1);
    this.player = this.levelManager.getPlayer();
    this.stateManager.changeState(GameState.MENU);
  }

  

  /**
   * Reset current level
   */
  private resetLevel(): void {
    this.stateManager.resetLevelData();
    this.levelManager.restartLevel();
    this.player = this.levelManager.getPlayer();
  }

  /**
   * Handle player input during gameplay
   */
  private handlePlayerInput(_dt: number): void {
    if (!this.player || !this.stateManager.isState(GameState.PLAYING)) {
      return;
    }

    // Movement
    if (this.inputHandler.isKeyPressed('j') || this.inputHandler.isKeyPressed('ArrowLeft')) {
      if (this.player.moveLeft(this.gameWorld)) {
        this.stateManager.incrementMoves();
      }
    } else if (this.inputHandler.isKeyPressed('l') || this.inputHandler.isKeyPressed('ArrowRight')) {
      if (this.player.moveRight(this.gameWorld)) {
        this.stateManager.incrementMoves();
      }
    }

    // Ice creation
    if (this.inputHandler.isKeyPressed('a')) {
      if (this.player.createIceLeft(this.gameWorld, this.iceSystem)) {
        this.stateManager.incrementMoves();
      }
    } else if (this.inputHandler.isKeyPressed('d')) {
      if (this.player.createIceRight(this.gameWorld, this.iceSystem)) {
        this.stateManager.incrementMoves();
      }
    }

    // Jump
    if (this.inputHandler.isKeyJustPressed(' ')) {
      this.player.jump(this.gameWorld);
    }
  }

  /**
   * Check win conditions
   */
  private checkWinConditions(): void {
    const flameCount = this.gameWorld.countObjectsOfType('flame');
    
    if (flameCount === 0 && this.stateManager.isState(GameState.PLAYING)) {
      this.stateManager.completeLevel();
      this.stateManager.changeState(GameState.WIN);
    }
  }

  /**
   * Update menu logic
   */
  private updateMenu(_dt: number): void {
    // Handle level selection
    if (this.inputHandler.isKeyJustPressed(' ')) {
      this.stateManager.changeState(GameState.PLAYING);
      this.stateManager.resetLevelData();
    }

    // Handle level number selection
    const levels = this.levelManager.getAvailableLevels();
    for (let i = 0; i < Math.min(6, levels.length); i++) {
      const key = (i + 1).toString();
      if (this.inputHandler.isKeyJustPressed(key)) {
        // Parse levelId from "section-level" format
        const [section, level] = levels[i].levelId.split('-').map(Number);
        this.levelManager.loadLevel(section, level);
        this.player = this.levelManager.getPlayer();
        this.stateManager.changeState(GameState.PLAYING);
        this.stateManager.resetLevelData();
        break;
      }
    }
  }

  /**
   * Update win screen logic
   */
  private updateWinScreen(_dt: number): void {
    if (this.inputHandler.isKeyJustPressed(' ')) {
      this.levelManager.completeLevel();
      this.stateManager.changeState(GameState.MENU);
    } else if (this.inputHandler.isKeyJustPressed('r')) {
      this.resetLevel();
      this.stateManager.changeState(GameState.PLAYING);
    }

    // Handle level number selection
    const levels = this.levelManager.getAvailableLevels();
    for (let i = 0; i < Math.min(6, levels.length); i++) {
      const key = (i + 1).toString();
      if (this.inputHandler.isKeyJustPressed(key)) {
        // Parse levelId from "section-level" format
        const [section, level] = levels[i].levelId.split('-').map(Number);
        this.levelManager.loadLevel(section, level);
        this.player = this.levelManager.getPlayer();
        this.stateManager.changeState(GameState.PLAYING);
        this.stateManager.resetLevelData();
        break;
      }
    }
  }

  /**
   * Update lose screen logic
   */
  private updateLoseScreen(_dt: number): void {
    if (this.inputHandler.isKeyJustPressed('r')) {
      this.resetLevel();
      this.stateManager.changeState(GameState.PLAYING);
    } else if (this.inputHandler.isKeyJustPressed('Escape')) {
      this.stateManager.changeState(GameState.MENU);
    }
  }

  /**
   * Main game update
   */
  private update(currentTime: number): void {
    // Calculate delta time
    const dt = Math.min((currentTime - this.lastTime) / 1000, 0.1); // Cap at 0.1s
    this.lastTime = currentTime;

    // Update input
    this.inputHandler.update();

    // Update based on current state
    if (this.stateManager.isState(GameState.PLAYING)) {
      // Update game time
      this.stateManager.updateTime(dt);
      
      // Update game world and physics
      this.gameWorld.update(dt);
      this.physicsEngine.update(dt);
      this.iceSystem.updateAllIceBlocks(dt, this.gameWorld);
      this.pushSystem.processPushRequests();
      this.gameRules.update(dt);
      
      // Handle player input
      this.handlePlayerInput(dt);
      
      // Check win conditions
      this.checkWinConditions();
    } else if (this.stateManager.isState(GameState.MENU)) {
      this.updateMenu(dt);
    } else if (this.stateManager.isState(GameState.WIN)) {
      this.updateWinScreen(dt);
    } else if (this.stateManager.isState(GameState.LOSE)) {
      this.updateLoseScreen(dt);
    }

    // Render
    this.render();
  }

  /**
   * Render the game
   */
  private render(): void {
    this.renderer.renderObjects();
    this.renderer.renderUI();
  }

  /**
   * Start the game loop
   */
  public start(): void {
    console.log('Starting ICER TypeScript Game...');
    console.log('Controls:');
    console.log('  J/L or Arrow Keys: Move left/right');
    console.log('  A/D: Create/remove ice blocks');
    console.log('  Space: Jump');
    console.log('  ESC: Pause game');
    console.log('  R: Restart level');
    console.log('  Tab: Toggle menu');
    console.log('  Alt+F4: Quit game');

    this.lastTime = performance.now();
    this.gameLoop(this.lastTime);
  }

  /**
   * Game loop using requestAnimationFrame
   */
  private gameLoop = (currentTime: number): void => {
    if (!this.isRunning) return;

    this.update(currentTime);
    requestAnimationFrame(this.gameLoop);
  };

  /**
   * Quit the game
   */
  private quit(): void {
    this.isRunning = false;
    console.log('Game quit');
  }

  /**
   * Destroy the game and clean up resources
   */
  public destroy(): void {
    this.isRunning = false;
    this.inputHandler.destroy();
    this.renderer.destroy();
  }
}