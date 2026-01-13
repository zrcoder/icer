import { GameObject } from '@/entities/base';
import { GRID_WIDTH, GRID_HEIGHT } from '@/game/constants';

/**
 * Grid cell containing a game object
 */
interface GridCell {
  object: GameObject | null;
}

/**
 * Game world - manages the grid and all game objects
 */
export class GameWorld {
  public width: number;
  public height: number;
  private grid: GridCell[][];
  private objects: Map<string, GameObject> = new Map();

  constructor(width: number = GRID_WIDTH, height: number = GRID_HEIGHT) {
    this.width = width;
    this.height = height;
    this.grid = Array(height).fill(null).map(() => 
      Array(width).fill(null).map(() => ({ object: null }))
    );
  }

  /**
   * Add an object to the world at specified grid position
   */
  addObject(object: GameObject, x: number, y: number): boolean {
    if (this.isOutOfBounds(x, y)) {
      return false;
    }

    if (this.grid[y][x].object !== null) {
      return false; // Cell already occupied
    }

    // Set object position and add to grid
    object.setPosition(x, y);
    this.grid[y][x].object = object;
    this.objects.set(`${x},${y}`, object);

    return true;
  }

  /**
   * Remove an object from the world
   */
  removeObject(x: number, y: number): GameObject | null {
    if (this.isOutOfBounds(x, y)) {
      return null;
    }

    const object = this.grid[y][x].object;
    if (object) {
      this.grid[y][x].object = null;
      this.objects.delete(`${x},${y}`);
    }

    return object;
  }

  /**
   * Move an object from one position to another
   */
  moveObject(fromX: number, fromY: number, toX: number, toY: number): boolean {
    if (this.isOutOfBounds(fromX, fromY) || this.isOutOfBounds(toX, toY)) {
      return false;
    }

    const object = this.grid[fromY][fromX].object;
    if (!object) {
      return false;
    }

    if (this.grid[toY][toX].object !== null) {
      return false; // Target cell occupied
    }

    // Move object
    this.grid[fromY][fromX].object = null;
    this.grid[toY][toX].object = object;
    
    // Update maps
    this.objects.delete(`${fromX},${fromY}`);
    this.objects.set(`${toX},${toY}`, object);

    // Update object position
    object.setPosition(toX, toY);

    return true;
  }

  /**
   * Get object at specified grid position
   */
  getObjectAt(x: number, y: number): GameObject | null {
    if (this.isOutOfBounds(x, y)) {
      return null;
    }

    return this.grid[y][x].object;
  }

  /**
   * Check if position is within world bounds
   */
  isOutOfBounds(x: number, y: number): boolean {
    return x < 0 || x >= this.width || y < 0 || y >= this.height;
  }

  /**
   * Get all objects in the world
   */
  getAllObjects(): GameObject[] {
    return Array.from(this.objects.values());
  }

  /**
   * Get objects of specific type
   */
  getObjectsOfType<T extends GameObject>(type: string): T[] {
    return Array.from(this.objects.values())
      .filter(obj => obj.getType() === type) as T[];
  }

  /**
   * Count objects of specific type
   */
  countObjectsOfType(type: string): number {
    return Array.from(this.objects.values())
      .filter(obj => obj.getType() === type).length;
  }

  /**
   * Clear all objects from the world
   */
  clear(): void {
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        this.grid[y][x].object = null;
      }
    }
    this.objects.clear();
  }

  /**
   * Update all objects in the world
   */
  update(dt: number): void {
    // Update all objects
    for (const object of this.objects.values()) {
      if (object.isActive) {
        object.update(dt);
      }
    }

    // Remove destroyed objects
    this.removeDestroyedObjects();
  }

  /**
   * Remove objects that have been destroyed
   */
  private removeDestroyedObjects(): void {
    const toRemove: string[] = [];

    for (const [key, object] of this.objects.entries()) {
      if (!object.isActive) {
        const [x, y] = key.split(',').map(Number);
        this.grid[y][x].object = null;
        toRemove.push(key);
      }
    }

    for (const key of toRemove) {
      this.objects.delete(key);
    }
  }

  /**
   * Get objects in a specific area
   */
  getObjectsInArea(x: number, y: number, width: number, height: number): GameObject[] {
    const objects: GameObject[] = [];

    for (let dy = 0; dy < height; dy++) {
      for (let dx = 0; dx < width; dx++) {
        const objX = x + dx;
        const objY = y + dy;
        
        if (!this.isOutOfBounds(objX, objY)) {
          const object = this.grid[objY][objX].object;
          if (object) {
            objects.push(object);
          }
        }
      }
    }

    return objects;
  }

  /**
   * Check if there's a solid object at position
   */
  isSolidAt(x: number, y: number): boolean {
    const object = this.getObjectAt(x, y);
    return object !== null && object.isSolid();
  }

  /**
   * Get grid iterator for all cells
   */
  getGrid(): Array<{x: number, y: number, object: GameObject | null}> {
    const cells: Array<{x: number, y: number, object: GameObject | null}> = [];
    
    for (let y = 0; y < this.height; y++) {
      for (let x = 0; x < this.width; x++) {
        cells.push({
          x,
          y,
          object: this.grid[y][x].object
        });
      }
    }

    return cells;
  }
}