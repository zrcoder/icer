import { GameWorld } from '@/world/gameWorld';
import { IceBlock } from '@/entities/objects/iceBlock';

/**
 * Ice block system for managing ice block lifecycle
 */
export class IceBlockSystem {
  private activeIceBlocks: Map<string, IceBlock> = new Map();

  constructor() {}

  /**
   * Create a new ice block at specified position
   */
  createIceBlock(x: number, y: number): IceBlock | null {
    // Check if position is valid
    if (x < 0 || x >= 20 || y < 0 || y >= 15) {
      return null;
    }

    const iceBlock = new IceBlock(x, y);
    const key = `${x},${y}`;
    this.activeIceBlocks.set(key, iceBlock);
    
    return iceBlock;
  }

  /**
   * Remove an ice block from the system
   */
  removeIceBlock(x: number, y: number): boolean {
    const key = `${x},${y}`;
    return this.activeIceBlocks.delete(key);
  }

  /**
   * Get ice block at specific position
   */
  getIceBlockAt(x: number, y: number): IceBlock | null {
    const key = `${x},${y}`;
    return this.activeIceBlocks.get(key) || null;
  }

  /**
   * Update all ice blocks
   */
  updateAllIceBlocks(dt: number, gameWorld: GameWorld): void {
    // Update all ice blocks
    for (const [key, iceBlock] of this.activeIceBlocks.entries()) {
      if (iceBlock.isActive) {
        iceBlock.update(dt);

        // Remove destroyed ice blocks
        if (!iceBlock.isActive) {
          gameWorld.removeObject(iceBlock.gridX, iceBlock.gridY);
          this.activeIceBlocks.delete(key);
        }
      }
    }

    // Check for melting conditions
    this.checkMeltingConditions(gameWorld);
  }

  /**
   * Check for conditions that cause ice blocks to melt
   */
  private checkMeltingConditions(gameWorld: GameWorld): void {
    for (const iceBlock of this.activeIceBlocks.values()) {
      if (!iceBlock.isActive) continue;

      // Check for nearby flames
      if (this.isNearFlame(iceBlock, gameWorld)) {
        (iceBlock as any).startMelting?.();
      }

      // Check if on hot pot
      if (this.isOnHotPot(iceBlock, gameWorld)) {
        (iceBlock as any).startMelting?.();
      }
    }
  }

  /**
   * Check if ice block is near a flame
   */
  private isNearFlame(iceBlock: IceBlock, gameWorld: GameWorld): boolean {
    const checkPositions = [
      { x: iceBlock.gridX - 1, y: iceBlock.gridY }, // Left
      { x: iceBlock.gridX + 1, y: iceBlock.gridY }, // Right
      { x: iceBlock.gridX, y: iceBlock.gridY + 1 }, // Top
      { x: iceBlock.gridX, y: iceBlock.gridY - 1 }, // Bottom
    ];

    for (const pos of checkPositions) {
      const object = gameWorld.getObjectAt(pos.x, pos.y);
      if (object && object.getType() === 'flame') {
        return true;
      }
    }

    return false;
  }

  /**
   * Check if ice block is on a hot pot
   */
  private isOnHotPot(iceBlock: IceBlock, gameWorld: GameWorld): boolean {
    const belowObject = gameWorld.getObjectAt(iceBlock.gridX, iceBlock.gridY - 1);
    return !!(belowObject && 
           belowObject.getType() === 'pot' && 
           (belowObject.getProperty('is_hot', false) as boolean));
  }

  /**
   * Get all active ice blocks
   */
  getAllIceBlocks(): IceBlock[] {
    return Array.from(this.activeIceBlocks.values());
  }

  /**
   * Get count of active ice blocks
   */
  getIceBlockCount(): number {
    return this.activeIceBlocks.size;
  }

  /**
   * Reset the ice block system
   */
  reset(): void {
    this.activeIceBlocks.clear();
  }

  /**
   * Remove ice block by reference
   */
  removeIceBlockByRef(iceBlock: IceBlock): boolean {
    for (const [key, block] of this.activeIceBlocks.entries()) {
      if (block === iceBlock) {
        return this.activeIceBlocks.delete(key);
      }
    }
    return false;
  }
}