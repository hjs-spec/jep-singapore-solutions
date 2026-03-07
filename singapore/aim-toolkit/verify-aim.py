#!/usr/bin/env python3
"""
JEP AIM Toolkit Verification Script
=====================================

This script exports JEP compliance evidence for the AIM Toolkit
(Competition & Consumer Protection) developed by CCS + IMDA.

This is a lightweight wrapper around export-script.py that provides
a dedicated verification interface for the AIM Toolkit.

Usage:
    python verify-aim.py --company "DBS Bank" --uen 12345678A --period Q1-2026
    
Examples:
    # Export evidence for Q1 2026
    python verify-aim.py --company "DBS Bank" --uen 12345678A --period Q1-2026
    
    # Generate HTML report for CCS submission
    python verify-aim.py --company "DBS Bank" --uen 12345678A --period Q1-2026 --format html
"""

import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import the actual implementation
from export_script import AIMToolkitExporter, main as export_main

def main():
    """
    Wrapper for export-script.py with AIM Toolkit specific interface.
    """
    parser = argparse.ArgumentParser(description="JEP AIM Toolkit Compliance Verification")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--uen", required=True, help="Company UEN")
    parser.add_argument("--period", help="Reporting period (e.g., Q1-2026)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--format", choices=["json", "html", "csv", "xml"], default="json", help="Output format")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Parse period into dates if needed
    start_date = args.start
    end_date = args.end
    
    if args.period and not (start_date and end_date):
        if args.period == "Q1-2026":
            start_date = "2026-01-01"
            end_date = "2026-03-31"
        elif args.period == "Q2-2026":
            start_date = "2026-04-01"
            end_date = "2026-06-30"
        elif args.period == "Q3-2026":
            start_date = "2026-07-01"
            end_date = "2026-09-30"
        elif args.period == "Q4-2026":
            start_date = "2026-10-01"
            end_date = "2026-12-31"
    
    # Initialize exporter
    exporter = AIMToolkitExporter(
        company_name=args.company,
        company_uen=args.uen
    )
    
    # Generate submission
    submission = exporter.generate_submission(
        start_date=start_date,
        end_date=end_date,
        output_format=args.format
    )
    
    # Save report
    output_file = args.output or f"aim-submission-{args.company}-{args.period or 'custom'}.{args.format}"
    if args.format == "json":
        with open(output_file, 'w') as f:
            json.dump(submission, f, indent=2, default=str)
    elif args.format == "html":
        html = exporter._generate_html_report(submission)
        with open(output_file, 'w') as f:
            f.write(html)
    
    print(f"✅ AIM Toolkit submission saved to {output_file}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
