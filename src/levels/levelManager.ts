import { GameWorld } from '@/world/gameWorld';
import { GameRulesSystem } from '@/rules/gameRules';
import { PhysicsEngine } from '@/physics/physicsEngine';
import { IceBlockSystem } from '@/physics/iceSystem';
import { GameObject, Player, Wall, IceBlock, Flame, Stone, Pot, Portal } from '@/entities';
import { Difficulty } from '@/game/constants';

/**
 * Level data structure
 */
export interface Level {
  id: string;
  name: string;
  difficulty: Difficulty;
  width: number;
  height: number;
  data: string[]; // Level layout as strings
  optimalMoves?: number;
  optimalTime?: number;
  description?: string;
}

/**
 * Level manager for loading and managing game levels
 */
export class LevelManager {
  private gameWorld: GameWorld;
  // Future system integrations
  // private gameRules: GameRulesSystem;
  // private physicsEngine: PhysicsEngine;
  // private iceSystem: IceBlockSystem;
  
  private levels: Map<string, Level> = new Map();
  private currentLevel: Level | null = null;
  private currentLevelId: string | null = null;
  private player: Player | null = null;

  constructor(
    gameWorld: GameWorld,
    _gameRules: GameRulesSystem,
    _physicsEngine: PhysicsEngine,
    _iceSystem: IceBlockSystem
  ) {
    this.gameWorld = gameWorld;
    // this.gameRules = gameRules;
    // this.physicsEngine = physicsEngine;
    // this.iceSystem = iceSystem;
    
    this.loadBuiltInLevels();
  }

  /**
   * Load built-in levels
   */
  private loadBuiltInLevels(): void {
    const builtInLevels: Level[] = [
      {
        id: 'tutorial_1',
        name: 'Movement Basics',
        difficulty: Difficulty.TUTORIAL,
        width: 10,
        height: 8,
        optimalMoves: 5,
        optimalTime: 10,
        description: 'Learn basic movement controls',
        data: [
          'WWWWWWWWWW',
          'W........W',
          'W..P.....W',
          'W........W',
          'W....F...W',
          'WWWWWWWWWW'
        ]
      },
      {
        id: 'tutorial_2',
        name: 'Ice Creation',
        difficulty: Difficulty.TUTORIAL,
        width: 12,
        height: 8,
        optimalMoves: 8,
        optimalTime: 15,
        description: 'Master ice magic',
        data: [
          'WWWWWWWWWWWW',
          'W..........W',
          'W..P.......W',
          'W....F.....W',
          'W..........W',
          'WWWWWWWWWWWW'
        ]
      },
      {
        id: 'basic_1',
        name: 'Ice Bridge',
        difficulty: Difficulty.BASIC,
        width: 15,
        height: 10,
        optimalMoves: 15,
        optimalTime: 30,
        description: 'Build an ice bridge to reach the flame',
        data: [
          'WWWWWWWWWWWWWWW',
          'W.............W',
          'W..P.........W',
          'W.............W',
          'WWW.....WWWWWWW',
          '...............',
          '........F.....',
          'WWWWWWWWWWWWWW'
        ]
      },
      {
        id: 'basic_2',
        name: 'Stone Pusher',
        difficulty: Difficulty.BASIC,
        width: 12,
        height: 10,
        optimalMoves: 12,
        optimalTime: 25,
        description: 'Use stones to solve the puzzle',
        data: [
          'WWWWWWWWWWWW',
          'W..........W',
          'W..P..S....W',
          'W..........W',
          'WWWW...WWWWWW',
          '............F',
          'WWWWWWWWWWWW'
        ]
      },
      {
        id: 'medium_1',
        name: 'Portal Maze',
        difficulty: Difficulty.MEDIUM,
        width: 20,
        height: 12,
        optimalMoves: 20,
        optimalTime: 45,
        description: 'Navigate through portals to extinguish all flames',
        data: [
          'WWWWWWWWWWWWWWWWWWWW',
          'W..................W',
          'W..P....1.........W',
          'W..................W',
          'WWWWWW....WWWWWWWWWW',
          '..................W',
          'W....F...........2W',
          'W..................W',
          'WWWWWW....WWWWWWWWWW',
          '..................W',
          'W............F....W',
          'WWWWWWWWWWWWWWWWWWWW'
        ]
      }
    ];

    for (const level of builtInLevels) {
      this.levels.set(level.id, level);
    }
  }

  /**
   * Load a level by ID
   */
  loadLevel(levelId: string): boolean {
    const level = this.levels.get(levelId);
    if (!level) {
      console.error(`Level not found: ${levelId}`);
      return false;
    }

    this.currentLevel = level;
    this.currentLevelId = levelId;

    // Clear current world
    this.gameWorld.clear();
    // this.iceSystem.reset();

    // Parse and create level
    this.parseLevelData(level);

    console.log(`Loaded level: ${level.name}`);
    return true;
  }

  /**
   * Parse level data string and create objects
   */
  private parseLevelData(level: Level): void {
    const objects: GameObject[] = [];
    
    for (let y = 0; y < level.data.length; y++) {
      const row = level.data[y];
      for (let x = 0; x < Math.min(row.length, level.width); x++) {
        const char = row[x];
        const gameObject = this.createGameObjectFromChar(char, x, level.height - y - 1);
        
        if (gameObject) {
          objects.push(gameObject);
        }
      }
    }

    // Create portal pairs
    this.createPortalPairs(objects);

    // Add all objects to game world
    for (const obj of objects) {
      if (obj.getType() !== 'portal') { // Portals added separately
        this.gameWorld.addObject(obj, obj.gridX, obj.gridY);
      }
    }

    // Add portals after all other objects
    for (const obj of objects) {
      if (obj.getType() === 'portal') {
        this.gameWorld.addObject(obj, obj.gridX, obj.gridY);
      }
    }
  }

  /**
   * Create game object from character
   */
  private createGameObjectFromChar(char: string, x: number, y: number): GameObject | null {
    switch (char) {
      case 'P':
        this.player = new Player(x, y);
        return this.player;
      
      case 'W':
        return new Wall(x, y);
      
      case 'I':
        return new IceBlock(x, y);
      
      case 'S':
        return new Stone(x, y);
      
      case 'F':
        return new Flame(x, y);
      
      case 'C':
        return new Pot(x, y, true); // Cold pot
      
      case 'H':
        return new Pot(x, y, false); // Hot pot
      
      case '1':
      case '2':
      case '3':
        // Store portal info for later pairing
        const portal = new Portal(x, y, `portal_${char}`);
        portal.setProperty('portal_group', char);
        return portal;
      
      case '.':
      case ' ':
        return null; // Empty space
      
      default:
        console.warn(`Unknown level character: ${char}`);
        return null;
    }
  }

  /**
   * Create portal pairs from portal objects
   */
  private createPortalPairs(objects: GameObject[]): void {
    const portalGroups: Map<string, Portal[]> = new Map();
    
    // Group portals by their group number
    for (const obj of objects) {
      if (obj.getType() === 'portal') {
        const group = obj.getProperty('portal_group');
        if (!portalGroups.has(group)) {
          portalGroups.set(group, []);
        }
        portalGroups.get(group)!.push(obj as Portal);
      }
    }

    // Create pairs within each group
    for (const [group, portals] of portalGroups.entries()) {
      if (portals.length === 2) {
        const [portal1, portal2] = portals;
        Portal.createPortalPair(
          portal1.gridX, portal1.gridY,
          portal2.gridX, portal2.gridY,
          `pair_${group}`
        );
      }
    }
  }

  /**
   * Get available levels
   */
  getAvailableLevels(): Array<{
    levelId: string;
    name: string;
    difficulty: Difficulty;
    isUnlocked: boolean;
    isCompleted: boolean;
    bestMoves: number;
    bestTime: number;
  }> {
    // For now, return all levels as unlocked and incomplete
    // In a full implementation, this would track progress
    return Array.from(this.levels.values()).map(level => ({
      levelId: level.id,
      name: level.name,
      difficulty: level.difficulty,
      isUnlocked: true,
      isCompleted: false,
      bestMoves: 0,
      bestTime: 0
    }));
  }

  /**
   * Complete current level
   */
  completeLevel(): void {
    if (this.currentLevelId) {
      // Mark level as completed
      console.log(`Level completed: ${this.currentLevel?.name || 'Unknown'}`);
    }
  }

  /**
   * Get current level
   */
  getCurrentLevel(): Level | null {
    return this.currentLevel;
  }

  /**
   * Get current level ID
   */
  getCurrentLevelId(): string | null {
    return this.currentLevelId;
  }

  /**
   * Get player instance
   */
  getPlayer(): Player | null {
    return this.player;
  }

  /**
   * Add custom level
   */
  addCustomLevel(level: Level): void {
    this.levels.set(level.id, level);
  }

  /**
   * Get level by ID
   */
  getLevel(levelId: string): Level | null {
    return this.levels.get(levelId) || null;
  }

  /**
   * Get all levels
   */
  getAllLevels(): Level[] {
    return Array.from(this.levels.values());
  }

  /**
   * Restart current level
   */
  restartLevel(): void {
    if (this.currentLevelId) {
      this.loadLevel(this.currentLevelId);
    }
  }
}