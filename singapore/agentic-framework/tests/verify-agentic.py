#!/usr/bin/env python3
"""
JEP Agentic AI Framework Verification Script
==============================================

This script verifies that a JEP implementation fully complies with
Singapore's Model AI Governance Framework for Agentic AI (2026).

This is a lightweight wrapper around verify-all-pillars.py that provides
the same functionality with a more specific filename for the Agentic AI Framework.

Usage:
    python verify-agentic.py [--pillar PILLAR] [--verbose]
    
Examples:
    # Run complete framework verification
    python verify-agentic.py
    
    # Run only Pillar 2 (Human Accountability)
    python verify-agentic.py --pillar 2
    
    # Generate HTML report
    python verify-agentic.py --output html --report agentic-audit.html
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the actual implementation
from verify-all-pillars import main as verify_main

if __name__ == "__main__":
    # This script passes all arguments to verify-all-pillars.py
    # so it maintains the same interface
    sys.exit(verify_main())
