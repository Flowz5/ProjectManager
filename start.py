#!/usr/bin/env python3
import sys
import os

# Ensure we can import src
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from src.main import main
except ImportError as e:
    print(f"Erreur d'importation : {e}")
    sys.exit(1)

if __name__ == "__main__":
    main()
