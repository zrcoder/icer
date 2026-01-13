import { Game } from '@/game/game';

/**
 * Main entry point for the ICER TypeScript game
 */
function main(): void {
  try {
    const game = new Game();
    game.start();
  } catch (error) {
    console.error('Failed to start game:', error);
    
    // Show error message on screen
    const loading = document.getElementById('loading');
    if (loading) {
      loading.textContent = `Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
      loading.classList.remove('hidden');
      loading.style.color = '#ff0000';
    }
  }
}

// Start the game when DOM is loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', main);
} else {
  main();
}