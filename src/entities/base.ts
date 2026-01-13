import { Vector2 } from '@/utils/vector2';

/**
 * Base class for all game objects
 */
export abstract class GameObject {
  public gridX: number;
  public gridY: number;
  public position: Vector2;
  public isActive: boolean = true;
  public properties: Map<string, any> = new Map();

  constructor(x: number = 0, y: number = 0) {
    this.gridX = x;
    this.gridY = y;
    this.position = new Vector2(x, y);
  }

  toString(): string {
    return `${this.constructor.name}(${this.gridX}, ${this.gridY})`;
  }

  // Abstract methods that must be implemented by subclasses
  abstract getType(): string;
  abstract getColor(): number;

  // Virtual methods that can be overridden
  update(dt: number): void {
    // Update logic (called each frame)
  }

  // Position methods
  setPosition(x: number, y: number): void {
    this.gridX = x;
    this.gridY = y;
    this.position = new Vector2(x, y);
  }

  getPosition(): Vector2 {
    return this.position;
  }

  getGridPosition(): [number, number] {
    return [this.gridX, this.gridY];
  }

  // Property methods
  setProperty(key: string, value: any): void {
    this.properties.set(key, value);
  }

  getProperty<T = any>(key: string, defaultValue?: T): T {
    return this.properties.has(key) ? this.properties.get(key) : defaultValue!;
  }

  hasProperty(key: string): boolean {
    return this.properties.has(key);
  }

  // Game object properties
  isSolid(): boolean {
    return this.getProperty('solid', true);
  }

  isPushable(): boolean {
    return this.getProperty('pushable', false);
  }

  isFragile(): boolean {
    return this.getProperty('fragile', false);
  }

  canSupportWeight(): boolean {
    return this.getProperty('supports_weight', true);
  }

  getWeight(): number {
    return this.getProperty('weight', 1);
  }

  isInteractive(): boolean {
    return this.getProperty('interactive', false);
  }

  // Interaction methods
  onCollision(_other: GameObject): void {
    // Handle collision with another object
  }

  onDestroy(): void {
    this.isActive = false;
  }

  destroy(): boolean {
    if (this.isFragile()) {
      this.onDestroy();
      return true;
    }
    return false;
  }

  activate(): void {
    this.isActive = true;
  }

  deactivate(): void {
    this.isActive = false;
  }

  interact(actor: GameObject): boolean {
    if (this.isInteractive()) {
      return this.onInteract(actor);
    }
    return false;
  }

  onInteract(_actor: GameObject): boolean {
    return true;
  }

  // Physics-related methods
  stopSliding(): void {
    this.setProperty('sliding', false);
    this.setProperty('slide_direction', null);
  }

  canIgnite(): boolean {
    return false;
  }

  canBePlacedOnHotPot(_hotPotY: number = 0): boolean {
    return false;
  }

  isFirm(): boolean {
    return this.getProperty('is_firm', false);
  }

  getPushDistance(): number {
    return this.getProperty('push_distance', 1);
  }

  checkFirmStatus(_gameWorld: any): boolean {
    this.setProperty('is_firm', false);
    return false;
  }
}