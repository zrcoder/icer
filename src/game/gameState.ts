import { GameState } from './constants';

// Re-export GameState for external use
export { GameState };

/**
 * Game data structure to track level progress
 */
export interface GameData {
  moves: number;
  timeElapsed: number;
  levelCompleted: boolean;
  bestMoves: number;
  bestTime: number;
}

/**
 * Game state manager
 */
export class GameStateManager {
  private currentState: GameState;
  public gameData: GameData;

  constructor() {
    this.currentState = GameState.MENU;
    this.gameData = {
      moves: 0,
      timeElapsed: 0,
      levelCompleted: false,
      bestMoves: 0,
      bestTime: 0
    };
  }

  getCurrentState(): GameState {
    return this.currentState;
  }

  isState(state: GameState): boolean {
    return this.currentState === state;
  }

  changeState(newState: GameState): void {
    this.currentState = newState;
  }

  resetLevelData(): void {
    this.gameData = {
      moves: 0,
      timeElapsed: 0,
      levelCompleted: false,
      bestMoves: this.gameData.bestMoves,
      bestTime: this.gameData.bestTime
    };
  }

  incrementMoves(): void {
    this.gameData.moves++;
  }

  updateTime(dt: number): void {
    this.gameData.timeElapsed += dt;
  }

  completeLevel(): void {
    this.gameData.levelCompleted = true;
    
    // Update best scores
    if (this.gameData.bestMoves === 0 || this.gameData.moves < this.gameData.bestMoves) {
      this.gameData.bestMoves = this.gameData.moves;
    }
    
    if (this.gameData.bestTime === 0 || this.gameData.timeElapsed < this.gameData.bestTime) {
      this.gameData.bestTime = this.gameData.timeElapsed;
    }
  }
}