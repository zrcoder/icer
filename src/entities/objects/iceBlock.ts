import { GameObject } from '@/entities/base';
import { COLOR_ICE_BLOCK, ICE_MELT_TIME } from '@/game/constants';

/**
 * Ice Block object - can be pushed, melts near flames
 */
export class IceBlock extends GameObject {
  private meltTimer: number = 0;
  private isMelting: boolean = false;

  constructor(x: number = 0, y: number = 0) {
    super(x, y);
    this.setProperty('solid', true);
    this.setProperty('pushable', true);
    this.setProperty('fragile', true);
    this.setProperty('supports_weight', true);
    this.setProperty('weight', 1);
    this.setProperty('push_distance', 1);
    this.setProperty('extinguishes_flames', true);
  }

  getType(): string {
    return 'ice_block';
  }

  getColor(): number {
    return COLOR_ICE_BLOCK;
  }

  update(dt: number): void {
    if (this.isMelting) {
      this.meltTimer += dt;
      if (this.meltTimer >= ICE_MELT_TIME) {
        this.destroy();
      }
    }
  }

  onCollision(other: GameObject): void {
    // Check if colliding with flame
    if (other.getType() === 'flame') {
      this.startMelting();
      // Extinguish the flame
      other.destroy();
    }
  }

  private startMelting(): void {
    this.isMelting = true;
    this.meltTimer = 0;
  }

  canIgnite(): boolean {
    return false; // Ice blocks can't be ignited, but they melt
  }

  getMeltingProgress(): number {
    if (!this.isMelting) return 0;
    return Math.min(this.meltTimer / ICE_MELT_TIME, 1);
  }

  isFirm(): boolean {
    return !this.isMelting;
  }

  checkFirmStatus(_gameWorld: any): boolean {
    // Ice blocks become less firm as they melt
    const firmness = 1 - this.getMeltingProgress();
    this.setProperty('is_firm', firmness > 0.5);
    return this.getProperty('is_firm');
  }
}