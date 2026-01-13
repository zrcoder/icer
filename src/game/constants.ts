/**
 * Game constants and configuration
 */

// Window settings
export const WINDOW_WIDTH = 800;
export const WINDOW_HEIGHT = 600;
export const FPS = 60;

// Grid settings
export const GRID_WIDTH = 20;
export const GRID_HEIGHT = 15;
export const CELL_SIZE = 40;

// Colors
export const BLACK = 0x000000;
export const WHITE = 0xFFFFFF;
export const GRAY = 0x808080;
export const LIGHT_GRAY = 0xC8C8C8;
export const DARK_GRAY = 0x404040;
export const RED = 0xFF0000;
export const BLUE = 0x0064FF;
export const LIGHT_BLUE = 0xADD8E6;
export const GREEN = 0x00FF00;
export const YELLOW = 0xFFFF00;
export const ORANGE = 0xFFA500;

// Game object colors
export const COLOR_PLAYER = BLUE;
export const COLOR_WALL = DARK_GRAY;
export const COLOR_ICE_BLOCK = LIGHT_BLUE;
export const COLOR_STONE = GRAY;
export const COLOR_FLAME = RED;
export const COLOR_ICE_POT = WHITE;
export const COLOR_HOT_POT = ORANGE;
export const COLOR_PORTAL = GREEN;

// Input keys
export const KEY_MOVE_LEFT = 'j';
export const KEY_MOVE_RIGHT = 'l';
export const KEY_ICE_LEFT = 'a';
export const KEY_ICE_RIGHT = 'd';

// Alternative arrow keys
export const KEY_ALT_LEFT = 'left';
export const KEY_ALT_RIGHT = 'right';

// Game states
export enum GameState {
  MENU = 'menu',
  PLAYING = 'playing',
  PAUSED = 'paused',
  WIN = 'win',
  LOSE = 'lose'
}

// Physics constants
export const GRAVITY = 9.8;
export const MAX_FALL_SPEED = 10.0;
export const PUSH_STRENGTH = 5.0;
export const ICE_MELT_TIME = 3.0;

// Game timing
export const FIXED_TIMESTEP = 1.0 / 60.0; // 60 FPS physics
export const MAX_ACCUMULATED_TIME = 0.25; // Maximum time to process in one frame

// Object types
export enum ObjectType {
  PLAYER = 'player',
  WALL = 'wall',
  ICE_BLOCK = 'ice_block',
  STONE = 'stone',
  FLAME = 'flame',
  POT = 'pot',
  PORTAL = 'portal'
}

// Level difficulty
export enum Difficulty {
  TUTORIAL = 'tutorial',
  BASIC = 'basic',
  MEDIUM = 'medium',
  HARD = 'hard'
}