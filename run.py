#!/usr/bin/env python3

# Apply patches first
import patch_parsimonious
import patch_starkware

# Now import and run the main application
from main import main

if __name__ == "__main__":
    main()
