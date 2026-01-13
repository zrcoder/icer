import { GameWorld } from '@/world/gameWorld';
import { PhysicsEngine } from './physicsEngine';
import { IceBlockSystem } from './iceSystem';
import { GameObject } from '@/entities/base';

/**
 * Game rules system for handling object interactions
 */
export class GameRulesSystem {
  private gameWorld: GameWorld;
  private physicsEngine: PhysicsEngine;
  private iceSystem: IceBlockSystem;

  constructor(gameWorld: GameWorld, physicsEngine: PhysicsEngine, iceSystem: IceBlockSystem) {
    this.gameWorld = gameWorld;
    this.physicsEngine = physicsEngine;
    this.iceSystem = iceSystem;
  }

  /**
   * Update game rules
   */
  update(dt: number): void {
    // Check all object interactions
    this.checkObjectInteractions();
    
    // Handle special game rules
    this.handleSpecialRules();
    
    // Clean up destroyed objects
    this.cleanupDestroyedObjects();
  }

  /**
   * Check interactions between objects
   */
  private checkObjectInteractions(): void {
    const objects = this.gameWorld.getAllObjects();
    
    for (let i = 0; i < objects.length; i++) {
      for (let j = i + 1; j < objects.length; j++) {
        const obj1 = objects[i];
        const obj2 = objects[j];
        
        if (this.areInteracting(obj1, obj2)) {
          this.handleInteraction(obj1, obj2);
        }
      }
    }
  }

  /**
   * Check if two objects are interacting
   */
  private areInteracting(obj1: GameObject, obj2: GameObject): boolean {
    // Objects interact if they're in the same cell or adjacent cells
    const sameCell = obj1.gridX === obj2.gridX && obj1.gridY === obj2.gridY;
    
    if (sameCell) return true;
    
    // Check adjacent cells for certain interactions
    const adjacentX = Math.abs(obj1.gridX - obj2.gridX) === 1 && obj1.gridY === obj2.gridY;
    const adjacentY = Math.abs(obj1.gridY - obj2.gridY) === 1 && obj1.gridX === obj2.gridX;
    
    return adjacentX || adjacentY;
  }

  /**
   * Handle interaction between two objects
   */
  private handleInteraction(obj1: GameObject, obj2: GameObject): void {
    const type1 = obj1.getType();
    const type2 = obj2.getType();

    // Fire interactions
    this.handleFireInteractions(obj1, obj2);
    
    // Ice interactions
    this.handleIceInteractions(obj1, obj2);
    
    // Pot interactions
    this.handlePotInteractions(obj1, obj2);
    
    // Portal interactions
    this.handlePortalInteractions(obj1, obj2);
    
    // Stone interactions
    this.handleStoneInteractions(obj1, obj2);
  }

  /**
   * Handle fire-related interactions
   */
  private handleFireInteractions(obj1: GameObject, obj2: GameObject): void {
    if (obj1.getType() === 'flame' || obj2.getType() === 'flame') {
      const flame = obj1.getType() === 'flame' ? obj1 : obj2;
      const other = obj1.getType() === 'flame' ? obj2 : obj1;
      
      // Fire ignites cold pots
      if (other.getType() === 'pot' && other.getProperty('is_cold')) {
        this.ignitePot(other, flame);
      }
      
      // Fire melts ice blocks
      if (other.getType() === 'ice_block') {
        this.meltIceBlock(other, flame);
      }
      
      // Fire spreads to flammable objects
      if (other.getProperty('flammable')) {
        this.spreadFire(flame, other);
      }
    }
  }

  /**
   * Handle ice-related interactions
   */
  private handleIceInteractions(obj1: GameObject, obj2: GameObject): void {
    if (obj1.getType() === 'ice_block' || obj2.getType() === 'ice_block') {
      const ice = obj1.getType() === 'ice_block' ? obj1 : obj2;
      const other = obj1.getType() === 'ice_block' ? obj2 : obj1;
      
      // Ice extinguishes flames
      if (other.getType() === 'flame') {
        this.extinguishFlame(other, ice);
      }
      
      // Ice cools hot pots
      if (other.getType() === 'pot' && other.getProperty('is_hot')) {
        this.coolPot(other, ice);
      }
    }
  }

  /**
   * Handle pot interactions
   */
  private handlePotInteractions(obj1: GameObject, obj2: GameObject): void {
    if (obj1.getType() === 'pot' || obj2.getType() === 'pot') {
      const pot1 = obj1.getType() === 'pot' ? obj1 : obj2;
      const pot2 = obj1.getType() === 'pot' ? obj2 : obj1;
      
      // Pot to pot interactions (temperature exchange)
      if (pot2.getType() === 'pot') {
        this.handlePotPotInteraction(pot1, pot2);
      }
    }
  }

  /**
   * Handle portal interactions
   */
  private handlePortalInteractions(obj1: GameObject, obj2: GameObject): void {
    if (obj1.getType() === 'portal' || obj2.getType() === 'portal') {
      const portal = obj1.getType() === 'portal' ? obj1 : obj2;
      const other = obj1.getType() === 'portal' ? obj2 : obj1;
      
      // Portal teleports compatible objects
      if (this.canTeleport(other)) {
        (portal as any).onCollision?.(other);
      }
    }
  }

  /**
   * Handle stone interactions
   */
  private handleStoneInteractions(obj1: GameObject, obj2: GameObject): void {
    if (obj1.getType() === 'stone' || obj2.getType() === 'stone') {
      const stone = obj1.getType() === 'stone' ? obj1 : obj2;
      const other = obj1.getType() === 'stone' ? obj2 : obj1;
      
      // Stone crushes fragile objects when falling
      if (this.isFalling(stone) && other.isFragile()) {
        this.crushObject(other, stone);
      }
    }
  }

  /**
   * Handle special game rules
   */
  private handleSpecialRules(): void {
    // Check win conditions
    this.checkWinCondition();
    
    // Check lose conditions
    this.checkLoseCondition();
    
    // Apply environmental effects
    this.applyEnvironmentalEffects();
  }

  /**
   * Check win condition
   */
  private checkWinCondition(): void {
    const flameCount = this.gameWorld.countObjectsOfType('flame');
    // Win condition handled in game class
  }

  /**
   * Check lose condition
   */
  private checkLoseCondition(): void {
    // Check if player is destroyed
    const player = this.gameWorld.getObjectsOfType('player')[0];
    if (player && !player.isActive) {
      // Player lost - this would be handled in game class
    }
  }

  /**
   * Apply environmental effects
   */
  private applyEnvironmentalEffects(): void {
    // Melt ice blocks near heat sources
    this.applyHeatEffects();
    
    // Extinguish flames near water/ice
    this.applyCoolingEffects();
  }

  /**
   * Apply heat effects to nearby objects
   */
  private applyHeatEffects(): void {
    const iceBlocks = this.gameWorld.getObjectsOfType('ice_block');
    const hotObjects = this.gameWorld.getAllObjects().filter(obj => 
      obj.getType() === 'flame' || 
      (obj.getType() === 'pot' && obj.getProperty('is_hot'))
    );

    for (const iceBlock of iceBlocks) {
      for (const hotObject of hotObjects) {
        const distance = Math.sqrt(
          Math.pow(iceBlock.gridX - hotObject.gridX, 2) + 
          Math.pow(iceBlock.gridY - hotObject.gridY, 2)
        );
        
        if (distance <= 2) { // Heat affects objects within 2 cells
          (iceBlock as any).startMelting?.();
        }
      }
    }
  }

  /**
   * Apply cooling effects to nearby objects
   */
  private applyCoolingEffects(): void {
    const flames = this.gameWorld.getObjectsOfType('flame');
    const coldObjects = this.gameWorld.getAllObjects().filter(obj => 
      obj.getType() === 'ice_block' || 
      (obj.getType() === 'pot' && obj.getProperty('is_cold'))
    );

    for (const flame of flames) {
      for (const coldObject of coldObjects) {
        const distance = Math.sqrt(
          Math.pow(flame.gridX - coldObject.gridX, 2) + 
          Math.pow(flame.gridY - coldObject.gridY, 2)
        );
        
        if (distance <= 1) { // Cooling affects objects within 1 cell
          if (coldObject.getType() === 'ice_block') {
            // Ice block extinguishes flame
            this.extinguishFlame(flame, coldObject);
          }
        }
      }
    }
  }

  /**
   * Clean up destroyed objects
   */
  private cleanupDestroyedObjects(): void {
    const objects = this.gameWorld.getAllObjects();
    
    for (const object of objects) {
      if (!object.isActive) {
        this.gameWorld.removeObject(object.gridX, object.gridY);
      }
    }
  }

  // Helper methods for specific interactions
  private ignitePot(pot: GameObject, flame: GameObject): void {
    (pot as any).startHeating?.();
    flame.destroy();
  }

  private meltIceBlock(ice: GameObject, flame: GameObject): void {
    (ice as any).startMelting?.();
  }

  private extinguishFlame(flame: GameObject, ice: GameObject): void {
    flame.destroy();
    (ice as any).startMelting?.();
  }

  private coolPot(pot: GameObject, ice: GameObject): void {
    (pot as any).coolDown?.();
    ice.destroy();
  }

  private handlePotPotInteraction(pot1: GameObject, pot2: GameObject): void {
    const pot1Hot = pot1.getProperty('is_hot');
    const pot2Hot = pot2.getProperty('is_hot');
    
    // Temperature exchange
    if (pot1Hot && !pot2Hot) {
      (pot1 as any).coolDown?.();
      (pot2 as any).startHeating?.();
    } else if (!pot1Hot && pot2Hot) {
      (pot2 as any).coolDown?.();
      (pot1 as any).startHeating?.();
    }
  }

  private canTeleport(obj: GameObject): boolean {
    const teleportableTypes = ['player', 'ice_block', 'stone', 'pot'];
    return teleportableTypes.includes(obj.getType());
  }

  private isFalling(obj: GameObject): boolean {
    // Check if object is falling (simplified check)
    return obj.getProperty('falling', false);
  }

  private crushObject(obj: GameObject, crusher: GameObject): void {
    if (crusher.getWeight() > obj.getWeight()) {
      obj.destroy();
    }
  }

  private spreadFire(flame: GameObject, target: GameObject): void {
    if (target.getProperty('flammable')) {
      // Create new flame at target position
      // This would create a new flame object
      target.destroy();
    }
  }
}