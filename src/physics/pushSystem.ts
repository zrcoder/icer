import { GameWorld } from '@/world/gameWorld';
import { PhysicsEngine } from './physicsEngine';
import { GameObject } from '@/entities/base';

/**
 * Push system for handling object pushing mechanics
 */
export class PushSystem {
  private gameWorld: GameWorld;
  private physicsEngine: PhysicsEngine;
  private pushRequests: PushRequest[] = [];

  constructor(gameWorld: GameWorld, physicsEngine: PhysicsEngine) {
    this.gameWorld = gameWorld;
    this.physicsEngine = physicsEngine;
  }

  /**
   * Request to push an object in a direction
   */
  requestPush(
    object: GameObject, 
    direction: 'left' | 'right', 
    force: number = 1
  ): void {
    if (!object.isPushable()) return;

    const request: PushRequest = {
      object,
      direction,
      force,
      distance: object.getPushDistance()
    };

    this.pushRequests.push(request);
  }

  /**
   * Process all pending push requests
   */
  processPushRequests(): void {
    const requests = [...this.pushRequests];
    this.pushRequests = []; // Clear requests

    for (const request of requests) {
      this.processPushRequest(request);
    }
  }

  /**
   * Process a single push request
   */
  private processPushRequest(request: PushRequest): void {
    const { object, direction, distance } = request;

    // Calculate target position
    const targetX = direction === 'left' ? 
      object.gridX - distance : 
      object.gridX + distance;

    // Check if push is possible
    if (this.canPushTo(object, targetX, object.gridY)) {
      this.performPush(object, targetX, object.gridY);
    }
  }

  /**
   * Check if object can be pushed to target position
   */
  private canPushTo(
    object: GameObject, 
    targetX: number, 
    targetY: number
  ): boolean {
    // Check boundaries
    if (targetX < 0 || targetX >= this.gameWorld.width || 
        targetY < 0 || targetY >= this.gameWorld.height) {
      return false;
    }

    // Check target cell
    const targetObject = this.gameWorld.getObjectAt(targetX, targetY);
    if (targetObject && targetObject.isSolid()) {
      return false;
    }

    // Check if object can be pushed (weight limits, etc.)
    return this.checkPushConstraints(object);
  }

  /**
   * Check if push respects physical constraints
   */
  private checkPushConstraints(object: GameObject): boolean {
    // Check if object is on solid ground
    if (!this.isOnSolidGround(object)) {
      return false;
    }

    // Check weight constraints
    const objectWeight = object.getWeight();
    if (objectWeight > 5) { // Maximum pushable weight
      return false;
    }

    // Check if object is not sliding
    const isSliding = object.getProperty('sliding', false);
    if (isSliding) {
      return false;
    }

    return true;
  }

  /**
   * Check if object is on solid ground
   */
  private isOnSolidGround(object: GameObject): boolean {
    if (object.gridY <= 0) return true; // At bottom

    const groundObject = this.gameWorld.getObjectAt(object.gridX, object.gridY - 1);
    return groundObject !== null && groundObject.canSupportWeight();
  }

  /**
   * Perform the actual push
   */
  private performPush(
    object: GameObject, 
    targetX: number, 
    targetY: number
  ): void {
    // Move object
    const success = this.gameWorld.moveObject(
      object.gridX,
      object.gridY,
      targetX,
      targetY
    );

    if (success) {
      // Apply push effects
      this.applyPushEffects(object, targetX, targetY);
    }
  }

  /**
   * Apply effects after successful push
   */
  private applyPushEffects(
    object: GameObject, 
    targetX: number, 
    targetY: number
  ): void {
    // Trigger push events
    object.setProperty('just_pushed', true);

    // Check for chaining pushes (pushing other objects)
    this.checkChainPushes(object, targetX, targetY);

    // Update physics
    this.updatePhysicsAfterPush(object);
  }

  /**
   * Check if this push creates chain reactions
   */
  private checkChainPushes(
    pushedObject: GameObject, 
    x: number, 
    y: number
  ): void {
    // Check adjacent cells for other pushable objects
    const adjacentPositions = [
      { x: x - 1, y },
      { x: x + 1, y },
      { x, y: y - 1 },
      { x, y: y + 1 }
    ];

    for (const pos of adjacentPositions) {
      const object = this.gameWorld.getObjectAt(pos.x, pos.y);
      
      if (object && object.isPushable() && object !== pushedObject) {
        // Calculate push direction based on position
        const dx = pos.x - x;
        const dy = pos.y - y;

        if (Math.abs(dx) > 0) { // Horizontal chain push
          const direction = dx > 0 ? 'right' : 'left';
          this.requestPush(object, direction, 0.5); // Reduced force for chain
        }
      }
    }
  }

  /**
   * Update physics after push
   */
  private updatePhysicsAfterPush(object: GameObject): void {
    // Update object state
    object.setProperty('last_push_time', Date.now());

    // Clear just_pushed flag after a frame
    setTimeout(() => {
      object.setProperty('just_pushed', false);
    }, 16); // One frame
  }

  /**
   * Get all pending push requests (for debugging)
   */
  getPendingPushRequests(): PushRequest[] {
    return [...this.pushRequests];
  }

  /**
   * Clear all push requests
   */
  clearPushRequests(): void {
    this.pushRequests = [];
  }
}

/**
 * Push request interface
 */
interface PushRequest {
  object: GameObject;
  direction: 'left' | 'right';
  force: number;
  distance: number;
}