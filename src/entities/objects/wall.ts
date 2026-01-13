import { GameObject } from '@/entities/base';
import { COLOR_WALL } from '@/game/constants';

/**
 * Wall object - static solid objects
 */
export class Wall extends GameObject {
  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    this.setProperty('solid', true);
    this.setProperty('pushable', false);
    this.setProperty('fragile', false);
    this.setProperty('supports_weight', true);
    this.setProperty('weight', Number.MAX_SAFE_INTEGER);
  }

  getType(): string {
    return 'wall';
  }

  getColor(): number {
    return COLOR_WALL;
  }

  update(_dt: number): void {
    // Walls don't need to update - they're static
  }
}