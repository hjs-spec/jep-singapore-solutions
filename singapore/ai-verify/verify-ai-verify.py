#!/usr/bin/env python3
"""
JEP AI Verify Framework Verification Script
=============================================

This script verifies that a JEP implementation complies with
IMDA's AI Verify Testing Framework, specifically the Accountability principle.

This is a lightweight wrapper around accountability-plugin.py that provides
a dedicated verification interface for AI Verify.

Usage:
    python verify-ai-verify.py [--model MODEL] [--test-cases FILE] [--output FORMAT]
    
Examples:
    # Run accountability tests
    python verify-ai-verify.py --model-path ./model.pkl --test-cases ./tests.json
    
    # Generate AI Verify compatible report
    python verify-ai-verify.py --output ai-verify --report report.json
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the actual implementation
from accountability_plugin import JEPAccountabilityPlugin, main as plugin_main

def main():
    """
    Wrapper for accountability-plugin.py with AI Verify specific interface.
    """
    parser = argparse.ArgumentParser(description="JEP AI Verify Compliance Verification")
    parser.add_argument("--model-path", help="Path to model file")
    parser.add_argument("--test-cases", help="Path to test cases JSON")
    parser.add_argument("--output", choices=["json", "html", "ai-verify"], default="json", help="Output format")
    parser.add_argument("--report", help="Output report file")
    
    args = parser.parse_args()
    
    if not args.model_path or not args.test_cases:
        print("❌ Error: --model-path and --test-cases are required")
        return 1
    
    # Load test cases
    with open(args.test_cases, 'r') as f:
        test_cases = json.load(f)
    
    # Load model (simulated)
    model = {"name": args.model_path}
    
    # Initialize plugin
    plugin = JEPAccountabilityPlugin()
    
    # Run tests
    results = plugin.run_tests(model, test_cases)
    
    # Generate report
    output_file = args.report or f"ai-verify-report-{results.timestamp}.json"
    plugin.generate_report(results, format=args.output, output_file=output_file)
    
    print(f"✅ AI Verify compliance report saved to {output_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
