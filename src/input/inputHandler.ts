/**
 * Input action types
 */
export type InputAction = 
  | 'move_left'
  | 'move_right'
  | 'create_ice_left'
  | 'create_ice_right'
  | 'jump'
  | 'pause'
  | 'restart'
  | 'menu'
  | 'select_level_1'
  | 'select_level_2'
  | 'select_level_3'
  | 'select_level_4'
  | 'select_level_5'
  | 'select_level_6'
  | 'start_game'
  | 'quit';

/**
 * Key binding configuration
 */
interface KeyBinding {
  key: string;
  action: InputAction;
  requireShift?: boolean;
  requireCtrl?: boolean;
  requireAlt?: boolean;
}

/**
 * Input handler for keyboard and mouse input
 */
export class InputHandler {
  private keys: Map<string, boolean> = new Map();
  private previousKeys: Map<string, boolean> = new Map();
  private keyBindings: KeyBinding[] = [];
  private actionCallbacks: Map<InputAction, () => void> = new Map();
  private isActive: boolean = true;

  constructor() {
    this.setupDefaultBindings();
    this.setupEventListeners();
  }

  /**
   * Setup default key bindings
   */
  private setupDefaultBindings(): void {
    this.keyBindings = [
      // Movement
      { key: 'j', action: 'move_left' },
      { key: 'l', action: 'move_right' },
      { key: 'ArrowLeft', action: 'move_left' },
      { key: 'ArrowRight', action: 'move_right' },
      
      // Ice creation
      { key: 'a', action: 'create_ice_left' },
      { key: 'd', action: 'create_ice_right' },
      
      // Jump (using space for jump)
      { key: ' ', action: 'jump' },
      
      // Game control
      { key: 'Escape', action: 'pause' },
      { key: 'r', action: 'restart' },
      { key: 'Tab', action: 'menu' },
      
      // Level selection
      { key: '1', action: 'select_level_1' },
      { key: '2', action: 'select_level_2' },
      { key: '3', action: 'select_level_3' },
      { key: '4', action: 'select_level_4' },
      { key: '5', action: 'select_level_5' },
      { key: '6', action: 'select_level_6' },
      
      // Game control
      { key: ' ', action: 'start_game' },
      
      // Quit (Alt+F4)
      { key: 'F4', action: 'quit', requireAlt: true },
    ];
  }

  /**
   * Setup event listeners
   */
  private setupEventListeners(): void {
    // Keyboard events
    window.addEventListener('keydown', this.handleKeyDown.bind(this));
    window.addEventListener('keyup', this.handleKeyUp.bind(this));
    
    // Prevent default behavior for game keys
    window.addEventListener('keydown', this.preventDefaultActions.bind(this));
    
    // Focus/blur handling
    window.addEventListener('blur', this.handleBlur.bind(this));
    window.addEventListener('focus', this.handleFocus.bind(this));
  }

  /**
   * Handle key down event
   */
  private handleKeyDown(event: KeyboardEvent): void {
    if (!this.isActive) return;

    const key = event.code || event.key;
    this.keys.set(key, true);

    // Check for bound actions
    this.checkKeyBindings(event);
  }

  /**
   * Handle key up event
   */
  private handleKeyUp(event: KeyboardEvent): void {
    const key = event.code || event.key;
    this.keys.set(key, false);
  }

  /**
   * Check for key bound actions
   */
  private checkKeyBindings(event: KeyboardEvent): void {
    for (const binding of this.keyBindings) {
      if (this.matchesBinding(binding, event)) {
        this.triggerAction(binding.action);
        break; // Only trigger first matching action
      }
    }
  }

  /**
   * Check if event matches key binding
   */
  private matchesBinding(binding: KeyBinding, event: KeyboardEvent): boolean {
    const key = event.code || event.key;
    
    // Check main key
    if (key !== binding.key && event.key !== binding.key) {
      return false;
    }

    // Check modifier keys
    if (binding.requireShift && !event.shiftKey) return false;
    if (binding.requireCtrl && !event.ctrlKey) return false;
    if (binding.requireAlt && !event.altKey) return false;

    return true;
  }

  /**
   * Trigger an action
   */
  private triggerAction(action: InputAction): void {
    const callback = this.actionCallbacks.get(action);
    if (callback) {
      callback();
    }
  }

  /**
   * Prevent default actions for game keys
   */
  private preventDefaultActions(event: KeyboardEvent): void {
    const preventedKeys = [
      ' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
      'Tab', 'Escape'
    ];

    const key = event.code || event.key;
    if (preventedKeys.includes(key) || preventedKeys.includes(event.key)) {
      event.preventDefault();
    }
  }

  /**
   * Handle window blur (lose focus)
   */
  private handleBlur(): void {
    // Clear all keys when window loses focus
    this.keys.clear();
  }

  /**
   * Handle window focus (gain focus)
   */
  private handleFocus(): void {
    // Input is reactivated when window gains focus
    this.isActive = true;
  }

  /**
   * Update input state (call this each frame)
   */
  update(): void {
    // Store previous key states
    this.previousKeys = new Map(this.keys);
  }

  /**
   * Check if key is currently pressed
   */
  isKeyPressed(key: string): boolean {
    return this.keys.get(key) || false;
  }

  /**
   * Check if key was just pressed this frame
   */
  isKeyJustPressed(key: string): boolean {
    const current = this.keys.get(key) || false;
    const previous = this.previousKeys.get(key) || false;
    return current && !previous;
  }

  /**
   * Check if key was just released this frame
   */
  isKeyJustReleased(key: string): boolean {
    const current = this.keys.get(key) || false;
    const previous = this.previousKeys.get(key) || false;
    return !current && previous;
  }

  /**
   * Check if any movement key is pressed
   */
  isMovementPressed(): boolean {
    return this.isKeyPressed('j') || 
           this.isKeyPressed('l') || 
           this.isKeyPressed('ArrowLeft') || 
           this.isKeyPressed('ArrowRight');
  }

  /**
   * Get movement direction (-1 for left, 1 for right, 0 for none)
   */
  getMovementDirection(): number {
    if (this.isKeyPressed('j') || this.isKeyPressed('ArrowLeft')) {
      return -1;
    }
    if (this.isKeyPressed('l') || this.isKeyPressed('ArrowRight')) {
      return 1;
    }
    return 0;
  }

  /**
   * Check if ice creation key is pressed
   */
  isIceCreationPressed(): 'left' | 'right' | null {
    if (this.isKeyPressed('a')) return 'left';
    if (this.isKeyPressed('d')) return 'right';
    return null;
  }

  /**
   * Bind callback to action
   */
  bindActionCallback(action: InputAction, callback: () => void): void {
    this.actionCallbacks.set(action, callback);
  }

  /**
   * Unbind action callback
   */
  unbindActionCallback(action: InputAction): void {
    this.actionCallbacks.delete(action);
  }

  /**
   * Add custom key binding
   */
  addKeyBinding(binding: KeyBinding): void {
    this.keyBindings.push(binding);
  }

  /**
   * Remove key binding
   */
  removeKeyBinding(action: InputAction): void {
    this.keyBindings = this.keyBindings.filter(binding => binding.action !== action);
  }

  /**
   * Set input active state
   */
  setActive(active: boolean): void {
    this.isActive = active;
    if (!active) {
      this.keys.clear();
    }
  }

  /**
   * Get input active state
   */
  isInputActive(): boolean {
    return this.isActive;
  }

  /**
   * Clear all input state
   */
  clear(): void {
    this.keys.clear();
    this.previousKeys.clear();
  }

  /**
   * Get currently pressed keys (for debugging)
   */
  getPressedKeys(): string[] {
    return Array.from(this.keys.entries())
      .filter(([, pressed]) => pressed)
      .map(([key]) => key);
  }

  /**
   * Destroy input handler (remove event listeners)
   */
  destroy(): void {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    window.removeEventListener('keydown', this.preventDefaultActions);
    window.removeEventListener('blur', this.handleBlur);
    window.removeEventListener('focus', this.handleFocus);
    
    this.keys.clear();
    this.previousKeys.clear();
    this.actionCallbacks.clear();
  }
}