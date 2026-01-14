import { GameObject } from '@/entities/base';
import { COLOR_PORTAL } from '@/game/constants';

/**
 * Portal object - transports player and some objects
 */
export class Portal extends GameObject {
  private pairedPortal: Portal | null = null;
  private portalId: string;
  private cooldown: number = 0;

  constructor(x: number = 0, y: number = 0, portalId: string = '') {
    super(x, y);
    this.portalId = portalId;
    
    this.setProperty('solid', false); // Portals don't block movement
    this.setProperty('pushable', false);
    this.setProperty('fragile', false);
    this.setProperty('supports_weight', false);
    this.setProperty('weight', 0);
    this.setProperty('portal_id', portalId);
  }

  getType(): string {
    return 'portal';
  }

  getColor(): number {
    return COLOR_PORTAL;
  }

  update(dt: number): void {
    if (this.cooldown > 0) {
      this.cooldown -= dt;
    }
  }

  onCollision(other: GameObject): void {
    if (!this.pairedPortal || this.cooldown > 0) return;

    // Check if object can be teleported
    if (this.canTeleport(other)) {
      this.teleport(other);
    }
  }

  private canTeleport(obj: GameObject): boolean {
    // Player, ice blocks, stones, and pots can be teleported
    const teleportableTypes = ['player', 'ice_block', 'stone', 'pot'];
    return teleportableTypes.includes(obj.getType());
  }

  private teleport(obj: GameObject): void {
    if (!this.pairedPortal) return;

    const targetX = this.pairedPortal.gridX;
    const targetY = this.pairedPortal.gridY;

    // Move object to paired portal location
    obj.setPosition(targetX, targetY);
    
    // Set cooldown on both portals
    this.cooldown = 1.0; // 1 second cooldown
    this.pairedPortal.cooldown = 1.0;

    // Trigger teleport effect if available
    this.onTeleport(obj);
  }

  protected onTeleport(_obj: GameObject): void {
    // Override for visual effects
  }

  // Static method to create portal pairs
  static createPortalPair(
    x1: number, y1: number, 
    x2: number, y2: number, 
    portalId: string
  ): [Portal, Portal] {
    const portal1 = new Portal(x1, y1, portalId);
    const portal2 = new Portal(x2, y2, portalId);
    
    portal1.pairedPortal = portal2;
    portal2.pairedPortal = portal1;
    
    return [portal1, portal2];
  }

  getPairedPortal(): Portal | null {
    return this.pairedPortal;
  }

  getPortalId(): string {
    return this.portalId;
  }

  isReady(): boolean {
    return this.cooldown <= 0 && this.pairedPortal !== null;
  }

  getCooldownProgress(): number {
    if (this.cooldown <= 0) return 0;
    return Math.min(this.cooldown / 1.0, 1);
  }
}