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
 * Level section info
 */
export interface SectionInfo {
  section: number;
  name?: string;
  levelCount: number;
}

/**
 * Level info in a section
 */
export interface LevelInfo {
  levelId: string;
  level: number;
  name?: string;
  difficulty?: Difficulty;
}

/**
 * Known sections and levels configuration
 */
const SECTIONS_CONFIG = {
  1: { name: 'Tutorial Section', levels: [1, 2] },
  2: { name: 'Basic Section', levels: [1, 2] },
  3: { name: 'Advanced Section', levels: [1] }
};

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
  }

  /**
   * Get available sections
   */
  getSections(): SectionInfo[] {
    const sections: SectionInfo[] = [];
    
    Object.entries(SECTIONS_CONFIG).forEach(([section, config]) => {
      sections.push({
        section: parseInt(section),
        name: config.name,
        levelCount: config.levels.length
      });
    });
    
    // Sort by section number
    sections.sort((a, b) => a.section - b.section);
    return sections;
  }

  /**
   * Get levels in a specific section
   */
  async getLevelsInSection(section: number): Promise<LevelInfo[]> {
    const levels: LevelInfo[] = [];
    const config = (SECTIONS_CONFIG as any)[section];
    
    if (!config) {
      console.warn(`Section ${section} not found`);
      return levels;
    }
    
    // Load each level to get metadata
    for (const levelNum of config.levels) {
      const levelId = `${section}-${levelNum}`;
      const levelData = await this.loadLevelData(section, levelNum);
      
      levels.push({
        levelId,
        level: levelNum,
        name: levelData?.name,
        difficulty: levelData?.difficulty
      });
    }
    
    return levels;
  }

  /**
   * Load level data dynamically
   */
  private async loadLevelData(section: number, level: number): Promise<Level | null> {
    const levelId = `${section}-${level}`;
    
    // Check cache first
    if (this.levels.has(levelId)) {
      return this.levels.get(levelId)!;
    }
    
    try {
      const levelModule = await import(`./levels/${section}/${level}.js`);
      const levelData = levelModule.default;
      
      if (!levelData || !levelData.grid) {
        throw new Error(`Invalid level data structure`);
      }
      
      const processedLevel: Level = {
        name: levelData.name || `Level ${section}-${level}`,
        difficulty: this.parseDifficulty(levelData.difficulty || 'basic'),
        width: Math.max(...levelData.grid.map((row: string) => row.length)),
        height: levelData.grid.length,
        data: levelData.grid,
        optimalMoves: levelData.optimal_moves,
        optimalTime: levelData.optimal_time,
        description: levelData.description
      };
      
      // Cache the level
      this.levels.set(levelId, processedLevel);
      return processedLevel;
    } catch (error) {
      console.error(`Failed to load level ${levelId}:`, error);
      return null;
    }
  }

  /**
   * Load a level by section and level number
   */
  async loadLevel(section: number, levelNum: number): Promise<boolean> {
    const levelId = `${section}-${levelNum}`;
    
    const level = await this.loadLevelData(section, levelNum);
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
   * Load a level by ID (for backward compatibility)
   */
  async loadLevelById(levelId: string): Promise<boolean> {
    const [section, level] = levelId.split('-').map(Number);
    if (isNaN(section) || isNaN(level)) {
      console.error(`Invalid level ID format: ${levelId}`);
      return false;
    }
    
    return this.loadLevel(section, level);
  }

  /**
   * Parse difficulty string to Difficulty enum
   */
  private parseDifficulty(difficultyStr: string): Difficulty {
    switch (difficultyStr.toLowerCase()) {
      case 'tutorial':
        return Difficulty.TUTORIAL;
      case 'basic':
        return Difficulty.BASIC;
      case 'medium':
        return Difficulty.MEDIUM;
      case 'hard':
        return Difficulty.HARD;
      default:
        return Difficulty.BASIC;
    }
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
   * Get available levels (for backward compatibility)
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
    // For now, return all configured levels
    const levels = [];
    for (const [section, config] of Object.entries(SECTIONS_CONFIG)) {
      for (const level of config.levels) {
        const levelId = `${section}-${level}`;
        const cachedLevel = this.levels.get(levelId);
        levels.push({
          levelId,
          name: cachedLevel?.name || `Level ${levelId}`,
          difficulty: cachedLevel?.difficulty || Difficulty.BASIC,
          isUnlocked: true,
          isCompleted: false,
          bestMoves: 0,
          bestTime: 0
        });
      }
    }
    return levels;
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
  addCustomLevel(levelId: string, level: Level): void {
    this.levels.set(levelId, level);
  }

  /**
   * Get level by ID
   */
  getLevel(levelId: string): Level | null {
    return this.levels.get(levelId) || null;
  }

  /**
   * Get all loaded levels
   */
  getAllLevels(): Level[] {
    return Array.from(this.levels.values());
  }

  /**
   * Get all loaded levels with their IDs
   */
  getAllLevelsWithIds(): Array<{ id: string; level: Level }> {
    return Array.from(this.levels.entries()).map(([id, level]) => ({ id, level }));
  }

  /**
   * Restart current level
   */
  async restartLevel(): Promise<void> {
    if (this.currentLevelId) {
      await this.loadLevelById(this.currentLevelId);
    }
  }
}