import { GameWorld } from '@/world/gameWorld';
import { GameObject } from '@/entities/base';
import { GRAVITY, MAX_FALL_SPEED, FIXED_TIMESTEP } from '@/game/constants';

/**
 * Physics engine for handling gravity and collisions
 */
export class PhysicsEngine {
  private gameWorld: GameWorld;
  private accumulatedTime: number = 0;

  constructor(gameWorld: GameWorld) {
    this.gameWorld = gameWorld;
  }

  /**
   * Update physics with fixed timestep
   */
  update(dt: number): void {
    this.accumulatedTime += dt;

    // Fixed timestep update
    while (this.accumulatedTime >= FIXED_TIMESTEP) {
      this.fixedUpdate(FIXED_TIMESTEP);
      this.accumulatedTime -= FIXED_TIMESTEP;
    }

    // Clamp accumulated time to prevent spiral of death
    if (this.accumulatedTime > FIXED_TIMESTEP * 10) {
      this.accumulatedTime = 0;
    }
  }

  /**
   * Fixed timestep physics update
   */
  private fixedUpdate(dt: number): void {
    const objects = this.gameWorld.getAllObjects();

    // Apply gravity to all affected objects
    for (const object of objects) {
      if (this.isAffectedByGravity(object)) {
        this.applyGravity(object, dt);
      }
    }

    // Check collisions and resolve them
    this.resolveCollisions(objects);
  }

  /**
   * Check if object is affected by gravity
   */
  private isAffectedByGravity(object: GameObject): boolean {
    // Only solid, non-static objects are affected by gravity
    return object.isSolid() && 
           !object.getProperty('static', false) &&
           object.getType() !== 'wall';
  }

  /**
   * Apply gravity to an object
   */
  private applyGravity(object: GameObject, dt: number): void {
    const currentY = object.gridY;
    const belowY = currentY - 1;

    // Check if object should fall
    if (this.shouldFall(object, belowY)) {
      this.fallObject(object, belowY);
    }
  }

  /**
   * Check if object should fall
   */
  private shouldFall(object: GameObject, belowY: number): boolean {
    // Don't fall if at bottom
    if (belowY < 0) return false;

    // Check what's below
    const belowObject = this.gameWorld.getObjectAt(object.gridX, belowY);
    
    // Fall if nothing below or if below can't support weight
    return !belowObject || !belowObject.canSupportWeight();
  }

  /**
   * Make object fall to position below
   */
  private fallObject(object: GameObject, targetY: number): void {
    const success = this.gameWorld.moveObject(
      object.gridX, 
      object.gridY, 
      object.gridX, 
      targetY
    );

    if (success) {
      // Handle landing on fragile objects
      this.handleLanding(object, targetY);
    }
  }

  /**
   * Handle object landing on another object
   */
  private handleLanding(object: GameObject, targetY: number): void {
    const belowY = targetY - 1;
    
    if (belowY >= 0) {
      const belowObject = this.gameWorld.getObjectAt(object.gridX, belowY);
      
      if (belowObject) {
        // Trigger collision events
        object.onCollision(belowObject);
        belowObject.onCollision(object);

        // Check if heavy object crushes fragile one
        if (object.getWeight() > belowObject.getWeight() && belowObject.isFragile()) {
          belowObject.destroy();
        }
      }
    }
  }

  /**
   * Resolve collisions between objects
   */
  private resolveCollisions(objects: GameObject[]): void {
    for (let i = 0; i < objects.length; i++) {
      for (let j = i + 1; j < objects.length; j++) {
        const obj1 = objects[i];
        const obj2 = objects[j];

        if (this.areColliding(obj1, obj2)) {
          this.resolveCollision(obj1, obj2);
        }
      }
    }
  }

  /**
   * Check if two objects are colliding
   */
  private areColliding(obj1: GameObject, obj2: GameObject): boolean {
    // Objects collide if they're in the same cell
    return obj1.gridX === obj2.gridX && obj1.gridY === obj2.gridY;
  }

  /**
   * Resolve collision between two objects
   */
  private resolveCollision(obj1: GameObject, obj2: GameObject): void {
    // Trigger collision events
    obj1.onCollision(obj2);
    obj2.onCollision(obj1);

    // Handle special collision cases
    this.handleSpecialCollisions(obj1, obj2);
  }

  /**
   * Handle special collision cases (fire, ice, etc.)
   */
  private handleSpecialCollisions(obj1: GameObject, obj2: GameObject): void {
    // Fire vs Ice
    if (this.isFireIceCollision(obj1, obj2)) {
      const fire = this.getFireObject(obj1, obj2);
      const ice = this.getIceObject(obj1, obj2);
      
      if (fire && ice) {
        // Fire extinguishes ice
        ice.destroy();
        fire.destroy();
      }
    }

    // Hot pot vs Ice
    if (this.isHotPotIceCollision(obj1, obj2)) {
      const hotPot = this.getHotPotObject(obj1, obj2);
      const ice = this.getIceObject(obj1, obj2);
      
      if (hotPot && ice) {
        ice.destroy();
        // Cool down the pot
        (hotPot as any).coolDown?.();
      }
    }
  }

  private isFireIceCollision(obj1: GameObject, obj2: GameObject): boolean {
    return (obj1.getType() === 'flame' && obj2.getType() === 'ice_block') ||
           (obj1.getType() === 'ice_block' && obj2.getType() === 'flame');
  }

  private isHotPotIceCollision(obj1: GameObject, obj2: GameObject): boolean {
    return (this.isHotPot(obj1) && obj2.getType() === 'ice_block') ||
           (this.isHotPot(obj2) && obj1.getType() === 'ice_block');
  }

  private isHotPot(obj: GameObject): boolean {
    return obj.getType() === 'pot' && obj.getProperty('is_hot', false);
  }

  private getFireObject(obj1: GameObject, obj2: GameObject): GameObject | null {
    return obj1.getType() === 'flame' ? obj1 : (obj2.getType() === 'flame' ? obj2 : null);
  }

  private getIceObject(obj1: GameObject, obj2: GameObject): GameObject | null {
    return obj1.getType() === 'ice_block' ? obj1 : (obj2.getType() === 'ice_block' ? obj2 : null);
  }

  private getHotPotObject(obj1: GameObject, obj2: GameObject): GameObject | null {
    return this.isHotPot(obj1) ? obj1 : (this.isHotPot(obj2) ? obj2 : null);
  }
}