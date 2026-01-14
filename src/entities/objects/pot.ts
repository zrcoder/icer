import { GameObject } from '@/entities/base';
import { COLOR_ICE_POT, COLOR_HOT_POT } from '@/game/constants';

/**
 * Pot object - can be cold or hot, interacts with ice and fire
 */
export class Pot extends GameObject {
  private isCold: boolean;
  private heatTimer: number = 0;
  private isHeating: boolean = false;

  constructor(x: number = 0, y: number = 0, isCold: boolean = true) {
    super(x, y);
    this.isCold = isCold;
    
    this.setProperty('solid', true);
    this.setProperty('pushable', true);
    this.setProperty('fragile', false);
    this.setProperty('supports_weight', true);
    this.setProperty('weight', 2);
    this.setProperty('push_distance', 1);
    this.setProperty('is_cold', isCold);
    this.setProperty('is_hot', !isCold);
  }

  getType(): string {
    return 'pot';
  }

  getColor(): number {
    return this.isCold ? COLOR_ICE_POT : COLOR_HOT_POT;
  }

  update(dt: number): void {
    if (this.isHeating) {
      this.heatTimer += dt;
      if (this.heatTimer >= 2.0) { // 2 seconds to heat up
        this.heatUp();
        this.isHeating = false;
      }
    }
  }

  onCollision(other: GameObject): void {
    if (other.getType() === 'flame' && this.isCold) {
      // Cold pot heats up when touched by flame
      this.startHeating();
      // Flame gets extinguished
      other.destroy();
    }
    
    if (other.getType() === 'ice_block' && !this.isCold) {
      // Hot pot melts ice blocks
      other.destroy();
      this.coolDown();
    }
  }

  private startHeating(): void {
    this.isHeating = true;
    this.heatTimer = 0;
  }

  private heatUp(): void {
    this.isCold = false;
    this.setProperty('is_cold', false);
    this.setProperty('is_hot', true);
  }

  private coolDown(): void {
    this.isCold = true;
    this.setProperty('is_cold', true);
    this.setProperty('is_hot', false);
  }

  canBePlacedOnHotPot(_hotPotY: number = 0): boolean {
    // Only ice blocks can be placed on hot pots (to melt them)
    return this.isCold === false; // This is a hot pot
  }

  canIgnite(): boolean {
    return false; // Pots can't be ignited directly
  }

  isFirm(): boolean {
    return true; // Pots are always firm
  }

  getHeatingProgress(): number {
    if (!this.isHeating) return 0;
    return Math.min(this.heatTimer / 2.0, 1);
  }
}