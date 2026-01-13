# Main entry point for ICER game

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.game.main import main

if __name__ == "__main__":
    main()