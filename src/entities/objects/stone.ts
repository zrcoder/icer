import { GameObject } from '@/entities/base';
import { COLOR_STONE } from '@/game/constants';

/**
 * Stone object - heavy pushable object
 */
export class Stone extends GameObject {
  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    this.setProperty('solid', true);
    this.setProperty('pushable', true);
    this.setProperty('fragile', false);
    this.setProperty('supports_weight', true);
    this.setProperty('weight', 3); // Heavier than ice blocks
    this.setProperty('push_distance', 1);
  }

  getType(): string {
    return 'stone';
  }

  getColor(): number {
    return COLOR_STONE;
  }

  update(_dt: number): void {
    // Stones don't have special update logic
  }

  // Stones can crush fragile objects
  onCollision(other: GameObject): void {
    if (other.getType() === 'flame') {
      // Stones extinguish flames they fall on
      other.destroy();
    }
  }

  isFirm(): boolean {
    return true; // Stones are always firm
  }

  getWeight(): number {
    return 3; // Heavy objects
  }
}