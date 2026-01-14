import { GameObject } from '@/entities/base';
import { COLOR_PLAYER } from '@/game/constants';
import { Vector2 } from '@/utils/vector2';

/**
 * Player character class
 */
export class Player extends GameObject {
  private jumpCooldown: number = 0;
  private moveDirection: number = 0; // -1 for left, 1 for right, 0 for none
  private iceCreateCooldown: number = 0;
  private animationOffset: Vector2 = Vector2.zero();
  private animationTime: number = 0;

  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    this.setProperty('solid', true);
    this.setProperty('pushable', false);
    this.setProperty('weight', 1);
    this.setProperty('can_jump', true);
  }

  getType(): string {
    return 'player';
  }

  getColor(): number {
    return COLOR_PLAYER;
  }

  update(dt: number): void {
    // Update cooldowns
    if (this.jumpCooldown > 0) {
      this.jumpCooldown -= dt;
    }
    
    if (this.iceCreateCooldown > 0) {
      this.iceCreateCooldown -= dt;
    }

    // Update animation
    this.animationTime += dt;
    this.updateAnimation();

    // Reset move direction each frame
    this.moveDirection = 0;
  }

  private updateAnimation(): void {
    // Simple idle animation
    const bobAmount = Math.sin(this.animationTime * 3) * 2;
    this.animationOffset = new Vector2(0, bobAmount);
  }

  getRenderOffset(_currentTime?: number): [number, number] {
    return this.animationOffset.toTuple();
  }

  // Movement methods
  moveLeft(gameWorld: any): boolean {
    this.moveDirection = -1;
    return this.tryMove(this.gridX - 1, this.gridY, gameWorld);
  }

  moveRight(gameWorld: any): boolean {
    this.moveDirection = 1;
    return this.tryMove(this.gridX + 1, this.gridY, gameWorld);
  }

  private tryMove(newX: number, newY: number, gameWorld: any): boolean {
    // Check boundaries
    if (newX < 0 || newX >= gameWorld.width || newY < 0 || newY >= gameWorld.height) {
      return false;
    }

    // Check collision
    const targetObject = gameWorld.getObjectAt(newX, newY);
    if (targetObject && targetObject.isSolid()) {
      // Try to push if it's pushable
      if (targetObject.isPushable()) {
        return this.tryPush(targetObject, this.moveDirection, gameWorld);
      }
      return false;
    }

    // Check if we can stand at the new position
    if (this.canStandAt(newX, newY, gameWorld)) {
      // Move the player
      gameWorld.moveObject(this.gridX, this.gridY, newX, newY);
      this.setPosition(newX, newY);
      return true;
    }

    return false;
  }

  private canStandAt(x: number, y: number, gameWorld: any): boolean {
    // Check if there's solid ground below
    if (y > 0) {
      const groundObject = gameWorld.getObjectAt(x, y - 1);
      return groundObject && groundObject.canSupportWeight();
    }
    return false; // Can't stand at bottom
  }

  private tryPush(object: GameObject, direction: number, gameWorld: any): boolean {
    const pushDistance = object.getPushDistance();
    const targetX = object.gridX + direction * pushDistance;

    // Check if object can be pushed to target position
    if (targetX >= 0 && targetX < gameWorld.width) {
      const targetObject = gameWorld.getObjectAt(targetX, object.gridY);
      if (!targetObject || !targetObject.isSolid()) {
        // Move the object
        gameWorld.moveObject(object.gridX, object.gridY, targetX, object.gridY);
        object.setPosition(targetX, object.gridY);
        return true;
      }
    }
    return false;
  }

  // Ice creation methods
  createIceLeft(gameWorld: any, iceSystem: any): boolean {
    return this.tryCreateIce(this.gridX - 1, this.gridY, gameWorld, iceSystem);
  }

  createIceRight(gameWorld: any, iceSystem: any): boolean {
    return this.tryCreateIce(this.gridX + 1, this.gridY, gameWorld, iceSystem);
  }

  private tryCreateIce(x: number, y: number, gameWorld: any, iceSystem: any): boolean {
    if (this.iceCreateCooldown > 0) return false;
    
    // Check boundaries and if space is empty
    if (x < 0 || x >= gameWorld.width || y < 0 || y >= gameWorld.height) {
      return false;
    }

    const existingObject = gameWorld.getObjectAt(x, y);
    if (existingObject) return false;

    // Create ice block
    const iceBlock = iceSystem.createIceBlock(x, y);
    if (iceBlock) {
      gameWorld.addObject(iceBlock, x, y);
      this.iceCreateCooldown = 0.5; // 0.5 second cooldown
      return true;
    }

    return false;
  }

  // Jump method (1-unit jumping as in original)
  jump(gameWorld: any): boolean {
    if (this.jumpCooldown > 0) return false;

    // Try to jump 1 unit up
    const jumpY = this.gridY + 1;
    if (jumpY < gameWorld.height) {
      const aboveObject = gameWorld.getObjectAt(this.gridX, jumpY);
      if (!aboveObject || !aboveObject.isSolid()) {
        // Perform jump
        gameWorld.moveObject(this.gridX, this.gridY, this.gridX, jumpY);
        this.setPosition(this.gridX, jumpY);
        this.jumpCooldown = 0.3; // 0.3 second cooldown
        return true;
      }
    }
    return false;
  }
}