/**
 * 2D Vector class for position and movement calculations
 */
export class Vector2 {
  constructor(
    public x: number = 0.0,
    public y: number = 0.0
  ) {}

  toString(): string {
    return `Vector2(${this.x}, ${this.y})`;
  }

  equals(other: Vector2): boolean {
    return Math.abs(this.x - other.x) < 1e-9 && Math.abs(this.y - other.y) < 1e-9;
  }

  add(other: Vector2 | [number, number]): Vector2 {
    if (other instanceof Vector2) {
      return new Vector2(this.x + other.x, this.y + other.y);
    } else if (Array.isArray(other) && other.length === 2) {
      return new Vector2(this.x + other[0], this.y + other[1]);
    }
    throw new Error("Can only add Vector2 to Vector2 or [number, number]");
  }

  subtract(other: Vector2 | [number, number]): Vector2 {
    if (other instanceof Vector2) {
      return new Vector2(this.x - other.x, this.y - other.y);
    } else if (Array.isArray(other) && other.length === 2) {
      return new Vector2(this.x - other[0], this.y - other[1]);
    }
    throw new Error("Can only subtract Vector2 from Vector2 or [number, number]");
  }

  multiply(scalar: number): Vector2 {
    if (typeof scalar === 'number') {
      return new Vector2(this.x * scalar, this.y * scalar);
    }
    throw new Error("Can only multiply Vector2 by scalar");
  }

  divide(scalar: number): Vector2 {
    if (typeof scalar === 'number' && scalar !== 0) {
      return new Vector2(this.x / scalar, this.y / scalar);
    }
    throw new Error("Can only divide Vector2 by non-zero scalar");
  }

  negate(): Vector2 {
    return new Vector2(-this.x, -this.y);
  }

  get(index: number): number {
    if (index === 0) return this.x;
    if (index === 1) return this.y;
    throw new Error("Vector2 index out of range");
  }

  magnitude(): number {
    return Math.sqrt(this.x * this.x + this.y * this.y);
  }

  magnitudeSquared(): number {
    return this.x * this.x + this.y * this.y;
  }

  normalize(): Vector2 {
    const mag = this.magnitude();
    if (mag > 0) {
      return new Vector2(this.x / mag, this.y / mag);
    }
    return new Vector2(0, 0);
  }

  distanceTo(other: Vector2): number {
    return this.subtract(other).magnitude();
  }

  distanceSquaredTo(other: Vector2): number {
    return this.subtract(other).magnitudeSquared();
  }

  dot(other: Vector2): number {
    return this.x * other.x + this.y * other.y;
  }

  cross(other: Vector2): number {
    return this.x * other.y - this.y * other.x;
  }

  lerp(other: Vector2, t: number): Vector2 {
    const clampedT = Math.max(0, Math.min(1, t));
    return this.add(other.subtract(this).multiply(clampedT));
  }

  toTuple(): [number, number] {
    return [this.x, this.y];
  }

  toIntTuple(): [number, number] {
    return [Math.floor(this.x), Math.floor(this.y)];
  }

  copy(): Vector2 {
    return new Vector2(this.x, this.y);
  }

  // Static methods
  static zero(): Vector2 {
    return new Vector2(0, 0);
  }

  static one(): Vector2 {
    return new Vector2(1, 1);
  }

  static up(): Vector2 {
    return new Vector2(0, 1);
  }

  static down(): Vector2 {
    return new Vector2(0, -1);
  }

  static left(): Vector2 {
    return new Vector2(-1, 0);
  }

  static right(): Vector2 {
    return new Vector2(1, 0);
  }

  static fromTuple(tuple: [number, number]): Vector2 {
    return new Vector2(tuple[0], tuple[1]);
  }
}