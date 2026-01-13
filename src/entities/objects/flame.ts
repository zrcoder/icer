import { GameObject } from '@/entities/base';
import { COLOR_FLAME } from '@/game/constants';

/**
 * Flame object - needs to be extinguished to win
 */
export class Flame extends GameObject {
  private brightness: number = 1.0;
  private flickerTime: number = 0;

  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    this.setProperty('solid', false); // Flames don't block movement
    this.setProperty('pushable', false);
    this.setProperty('fragile', true); // Can be extinguished
    this.setProperty('supports_weight', false);
    this.setProperty('weight', 0);
    this.setProperty('is_fire', true);
  }

  getType(): string {
    return 'flame';
  }

  getColor(): number {
    return COLOR_FLAME;
  }

  update(dt: number): void {
    // Flicker animation
    this.flickerTime += dt * 3; // 3 flickers per second
    this.brightness = 0.7 + Math.sin(this.flickerTime) * 0.3;
  }

  onCollision(other: GameObject): void {
    // Check if colliding with ice block
    if (other.getType() === 'ice_block') {
      this.extinguish();
    }
    
    // Check if colliding with ice pot
    if (other.getType() === 'pot' && other.getProperty('is_cold')) {
      this.extinguish();
    }
  }

  private extinguish(): void {
    this.destroy();
  }

  getBrightness(): number {
    return this.brightness;
  }

  canIgnite(): boolean {
    return true; // Flames can ignite other objects
  }

  isFirm(): boolean {
    return false; // Flames are not firm
  }
}