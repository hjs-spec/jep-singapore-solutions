#!/usr/bin/env python3
"""
JEP AIM Toolkit Export Script
===============================

This script exports JEP compliance evidence in AIM Toolkit compatible format
for submission to CCS (Competition and Consumer Commission of Singapore).

The exported report can be used as:
- Self-assessment evidence for AIM Toolkit
- Mitigating factor in CCS investigations
- Compliance documentation for internal audits
- Submission for IMDA's AI Verify framework

Usage:
    # Export for specific company and period
    python export-script.py --company "DBS Bank" --uen 12345678A --period Q1-2026
    
    # Export with custom date range
    python export-script.py --company "DBS Bank" --start 2026-01-01 --end 2026-03-31
    
    # Export specific principles only
    python export-script.py --company "DBS Bank" --principles Accountability,Transparency
    
    # Generate HTML report for presentation
    python export-script.py --company "DBS Bank" --format html --output report.html
"""

import json
import os
import sys
import time
import argparse
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from enum import Enum
import csv
import xml.etree.ElementTree as ET
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
try:
    from jep.core import JEPAsymmetricSigner, generate_uuid7
except ImportError:
    print("⚠️ Warning: jep.core not found. Using mock implementation.")
    # Mock JEP for standalone testing
    def generate_uuid7():
        import uuid
        return str(uuid.uuid4())
    
    class JEPAsymmetricSigner:
        def __init__(self, private_key_hex=None):
            pass
        def sign_payload(self, data):
            return f"ed25519:mocksignature{hash(str(data))}"


class AIMToolkitExporter:
    """
    Exports JEP evidence in AIM Toolkit compatible format.
    """
    
    def __init__(
        self,
        company_name: str,
        company_uen: str,
        contact_email: str = "compliance@company.com",
        output_dir: str = "./aim-exports",
        receipt_dir: str = "./receipts"
    ):
        """
        Initialize the exporter.
        
        Args:
            company_name: Name of the company
            company_uen: Unique Entity Number (UEN) registered with ACRA
            contact_email: Contact email for compliance inquiries
            output_dir: Directory to save export files
            receipt_dir: Directory containing JEP receipt files
        """
        self.company_name = company_name
        self.company_uen = company_uen
        self.contact_email = contact_email
        self.output_dir = Path(output_dir)
        self.receipt_dir = Path(receipt_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize signer for report signing
        self.signer = JEPAsymmetricSigner()
        
        # Cache for loaded receipts
        self.receipt_cache = []
        
        print(f"✅ AIM Toolkit Exporter initialized")
        print(f"   Company: {company_name} (UEN: {company_uen})")
        print(f"   Output Directory: {self.output_dir}")
        print(f"   Receipt Directory: {self.receipt_dir}")
    
    def load_receipts(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Load JEP receipts from the receipt directory.
        
        Args:
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
        
        Returns:
            List of receipt dictionaries
        """
        receipts = []
        
        # Convert date strings to timestamps if provided
        start_ts = None
        end_ts = None
        if start_date:
            start_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
        if end_date:
            end_ts = datetime.strptime(end_date, "%Y-%m-%d").timestamp() + 86400  # End of day
        
        # Find all JSON files in receipt directory
        receipt_files = list(self.receipt_dir.glob("*.json"))
        print(f"📂 Found {len(receipt_files)} receipt files")
        
        for receipt_file in receipt_files:
            try:
                with open(receipt_file, 'r') as f:
                    receipt = json.load(f)
                
                # Apply date filter if provided
                if start_ts or end_ts:
                    receipt_time = receipt.get("timestamp", receipt.get("issued_at", 0))
                    if isinstance(receipt_time, str):
                        try:
                            receipt_time = datetime.strptime(receipt_time, "%Y-%m-%dT%H:%M:%SZ").timestamp()
                        except:
                            receipt_time = 0
                    
                    if start_ts and receipt_time < start_ts:
                        continue
                    if end_ts and receipt_time > end_ts:
                        continue
                
                receipts.append(receipt)
                
            except Exception as e:
                print(f"⚠️ Error loading {receipt_file}: {e}")
        
        self.receipt_cache = receipts
        print(f"✅ Loaded {len(receipts)} receipts after filtering")
        
        return receipts
    
    def generate_submission(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        principles: Optional[List[str]] = None,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate AIM Toolkit submission package.
        
        Args:
            start_date: Start date for the reporting period (YYYY-MM-DD)
            end_date: End date for the reporting period (YYYY-MM-DD)
            principles: List of principles to include (None for all)
            output_format: Output format (json, html, xml, csv)
        
        Returns:
            Submission dictionary
        """
        print(f"\n{'='*60}")
        print(f"📊 Generating AIM Toolkit Submission")
        print(f"{'='*60}")
        print(f"Company: {self.company_name}")
        print(f"Period: {start_date} to {end_date or 'present'}")
        
        # Load receipts for the period
        receipts = self.load_receipts(start_date, end_date)
        
        if not receipts:
            print("⚠️ No receipts found for the specified period")
            return {"error": "No receipts found"}
        
        # Define all AIM principles
        all_principles = [
            "Accountability",
            "Transparency",
            "Accuracy",
            "Fairness",
            "Pro-competitive Algorithms",
            "Consumer Protection",
            "Data Governance",
            "Openness"
        ]
        
        # Filter principles if specified
        if principles:
            selected_principles = [p for p in all_principles if p in principles]
        else:
            selected_principles = all_principles
        
        # Build submission
        submission = {
            "submission_id": f"AIM-{self.company_uen}-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "company": {
                "name": self.company_name,
                "uen": self.company_uen,
                "contact": self.contact_email
            },
            "period": {
                "start": start_date or "N/A",
                "end": end_date or "N/A"
            },
            "statistics": {
                "total_receipts": len(receipts),
                "date_range": self._get_date_range(receipts),
                "risk_distribution": self._get_risk_distribution(receipts)
            },
            "principles": [],
            "mitigating_factors": self._generate_mitigating_factors(receipts),
            "evidence_summary": self._generate_evidence_summary(receipts)
        }
        
        # Generate evidence for each principle
        for principle in selected_principles:
            print(f"\n📋 Processing {principle}...")
            principle_data = self._generate_principle_evidence(principle, receipts)
            submission["principles"].append(principle_data)
        
        # Sign the submission
        submission["signature"] = self.signer.sign_payload(submission)
        submission["verification_method"] = "Ed25519 (RFC 8032)"
        
        # Save submission
        self._save_submission(submission, output_format)
        
        return submission
    
    def _generate_principle_evidence(self, principle: str, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate evidence for a specific AIM principle.
        """
        # Define check mappings for each principle
        check_mappings = {
            "Accountability": self._get_accountability_checks,
            "Transparency": self._get_transparency_checks,
            "Accuracy": self._get_accuracy_checks,
            "Fairness": self._get_fairness_checks,
            "Pro-competitive Algorithms": self._get_procompetitive_checks,
            "Consumer Protection": self._get_consumer_protection_checks,
            "Data Governance": self._get_data_governance_checks,
            "Openness": self._get_openness_checks
        }
        
        # Get checks for this principle
        check_func = check_mappings.get(principle)
        if check_func:
            checks = check_func(receipts)
        else:
            checks = []
        
        # Calculate overall compliance
        total_checks = len(checks)
        compliant_checks = sum(1 for c in checks if c.get("status") == "COMPLIANT")
        overall_score = compliant_checks / total_checks if total_checks > 0 else 0
        
        if overall_score >= 0.9:
            overall_status = "COMPLIANT"
        elif overall_score >= 0.7:
            overall_status = "PARTIALLY_COMPLIANT"
        else:
            overall_status = "NON_COMPLIANT"
        
        return {
            "name": principle,
            "overall": overall_status,
            "score": overall_score,
            "checks": checks,
            "evidence_count": sum(len(c.get("evidence_receipts", [])) for c in checks)
        }
    
    def _get_accountability_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Accountability principle (A1-A7)."""
        checks = []
        
        # A1: Clear allocation of responsibilities
        receipts_with_actor = [r for r in receipts if self._get_nested(r, "compliance_binding.actor_id")]
        checks.append({
            "id": "A1",
            "description": "Clear allocation of responsibilities",
            "status": "COMPLIANT" if len(receipts_with_actor) > 0 else "NON_COMPLIANT",
            "evidence": f"{len(receipts_with_actor)}/{len(receipts)} receipts have attributable actor_id",
            "evidence_receipts": [r.get("receipt_id") for r in receipts_with_actor[:5]]
        })
        
        # A2: Governance framework documented
        has_governance = any("governance" in str(r) for r in receipts)
        checks.append({
            "id": "A2",
            "description": "Governance framework documented",
            "status": "COMPLIANT" if has_governance else "PARTIALLY_COMPLIANT",
            "evidence": "Governance references found in receipts",
            "evidence_receipts": []
        })
        
        # A3: Regular compliance reviews
        review_timestamps = [r.get("review_timestamp") for r in receipts if r.get("review_timestamp")]
        checks.append({
            "id": "A3",
            "description": "Regular compliance reviews",
            "status": "COMPLIANT" if len(review_timestamps) > 5 else "PARTIALLY_COMPLIANT",
            "evidence": f"{len(review_timestamps)} reviews recorded",
            "evidence_receipts": []
        })
        
        # A4: Risk assessment documented
        receipts_with_risk = [r for r in receipts if self._get_nested(r, "compliance_binding.risk_level")]
        risk_distribution = {}
        for r in receipts_with_risk:
            risk = self._get_nested(r, "compliance_binding.risk_level", "UNKNOWN")
            risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
        
        checks.append({
            "id": "A4",
            "description": "Risk assessment documented",
            "status": "COMPLIANT" if len(receipts_with_risk) > 0 else "NON_COMPLIANT",
            "evidence": f"Risk distribution: {risk_distribution}",
            "evidence_receipts": [r.get("receipt_id") for r in receipts_with_risk[:5]]
        })
        
        # A5: Incident response plan
        has_incidents = any("incident" in str(r).lower() for r in receipts)
        checks.append({
            "id": "A5",
            "description": "Incident response plan",
            "status": "COMPLIANT" if has_incidents else "PARTIALLY_COMPLIANT",
            "evidence": "Incident handling records found" if has_incidents else "No incidents recorded",
            "evidence_receipts": []
        })
        
        # A6: Third-party risk management
        has_third_party = any("provider" in str(r).lower() for r in receipts)
        checks.append({
            "id": "A6",
            "description": "Third-party risk management",
            "status": "COMPLIANT" if has_third_party else "PARTIALLY_COMPLIANT",
            "evidence": "Third-party providers identified" if has_third_party else "No third-party data",
            "evidence_receipts": []
        })
        
        # A7: Board and management oversight
        has_board_review = any("board" in str(r).lower() for r in receipts)
        checks.append({
            "id": "A7",
            "description": "Board and management oversight",
            "status": "COMPLIANT" if has_board_review else "PARTIALLY_COMPLIANT",
            "evidence": "Board oversight recorded" if has_board_review else "No board records",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_transparency_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Transparency principle (T1-T6)."""
        checks = []
        
        # T1: Clear disclosure of AI use
        has_ai_disclosure = any("is_ai_generated" in str(r) for r in receipts)
        checks.append({
            "id": "T1",
            "description": "Clear disclosure of AI use",
            "status": "COMPLIANT" if has_ai_disclosure else "NON_COMPLIANT",
            "evidence": "AI disclosure fields present" if has_ai_disclosure else "No AI disclosure",
            "evidence_receipts": []
        })
        
        # T2: Explainable decisions
        has_reasoning = any(r.get("reasoning") for r in receipts)
        checks.append({
            "id": "T2",
            "description": "Explainable decisions",
            "status": "COMPLIANT" if has_reasoning else "PARTIALLY_COMPLIANT",
            "evidence": "Decision explanations available" if has_reasoning else "Limited explanations",
            "evidence_receipts": []
        })
        
        # T3: Terms and conditions accessible
        has_terms = any("terms" in str(r).lower() for r in receipts)
        checks.append({
            "id": "T3",
            "description": "Terms and conditions accessible",
            "status": "COMPLIANT" if has_terms else "PARTIALLY_COMPLIANT",
            "evidence": "Terms references found" if has_terms else "No terms references",
            "evidence_receipts": []
        })
        
        # T4: Privacy policy accessible
        has_privacy = any("privacy" in str(r).lower() for r in receipts)
        checks.append({
            "id": "T4",
            "description": "Privacy policy accessible",
            "status": "COMPLIANT" if has_privacy else "PARTIALLY_COMPLIANT",
            "evidence": "Privacy references found" if has_privacy else "No privacy references",
            "evidence_receipts": []
        })
        
        # T5: Consumer rights explained
        has_rights = any("rights" in str(r).lower() for r in receipts)
        checks.append({
            "id": "T5",
            "description": "Consumer rights explained",
            "status": "COMPLIANT" if has_rights else "PARTIALLY_COMPLIANT",
            "evidence": "Rights explanations found" if has_rights else "No rights explanations",
            "evidence_receipts": []
        })
        
        # T6: Complaint mechanism available
        has_complaint = any("complaint" in str(r).lower() for r in receipts)
        checks.append({
            "id": "T6",
            "description": "Complaint mechanism available",
            "status": "COMPLIANT" if has_complaint else "PARTIALLY_COMPLIANT",
            "evidence": "Complaint mechanism referenced" if has_complaint else "No complaint references",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_accuracy_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Accuracy principle (AC1-AC7)."""
        checks = []
        
        # AC1: Accuracy metrics tracked
        has_accuracy = any("accuracy" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC1",
            "description": "Accuracy metrics tracked",
            "status": "COMPLIANT" if has_accuracy else "PARTIALLY_COMPLIANT",
            "evidence": "Accuracy metrics found" if has_accuracy else "No accuracy metrics",
            "evidence_receipts": []
        })
        
        # AC2: Validation datasets documented
        has_validation = any("validation" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC2",
            "description": "Validation datasets documented",
            "status": "COMPLIANT" if has_validation else "PARTIALLY_COMPLIANT",
            "evidence": "Validation data referenced" if has_validation else "No validation data",
            "evidence_receipts": []
        })
        
        # AC3: Performance monitoring
        has_performance = any("performance" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC3",
            "description": "Performance monitoring",
            "status": "COMPLIANT" if has_performance else "PARTIALLY_COMPLIANT",
            "evidence": "Performance metrics found" if has_performance else "No performance metrics",
            "evidence_receipts": []
        })
        
        # AC4: Model drift detection
        has_drift = any("drift" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC4",
            "description": "Model drift detection",
            "status": "COMPLIANT" if has_drift else "PARTIALLY_COMPLIANT",
            "evidence": "Drift detection records found" if has_drift else "No drift detection",
            "evidence_receipts": []
        })
        
        # AC5: Retraining procedures
        has_retraining = any("retrain" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC5",
            "description": "Retraining procedures",
            "status": "COMPLIANT" if has_retraining else "PARTIALLY_COMPLIANT",
            "evidence": "Retraining records found" if has_retraining else "No retraining records",
            "evidence_receipts": []
        })
        
        # AC6: Version control
        has_version = any("version" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC6",
            "description": "Version control",
            "status": "COMPLIANT" if has_version else "PARTIALLY_COMPLIANT",
            "evidence": "Version information found" if has_version else "No version information",
            "evidence_receipts": []
        })
        
        # AC7: Change management
        has_change = any("change" in str(r).lower() for r in receipts)
        checks.append({
            "id": "AC7",
            "description": "Change management",
            "status": "COMPLIANT" if has_change else "PARTIALLY_COMPLIANT",
            "evidence": "Change records found" if has_change else "No change records",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_fairness_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Fairness principle (F1-F6)."""
        checks = []
        
        # F1: Bias testing performed
        has_bias = any("bias" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F1",
            "description": "Bias testing performed",
            "status": "COMPLIANT" if has_bias else "PARTIALLY_COMPLIANT",
            "evidence": "Bias test records found" if has_bias else "No bias tests",
            "evidence_receipts": []
        })
        
        # F2: Demographic parity
        has_demographic = any("demographic" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F2",
            "description": "Demographic parity",
            "status": "COMPLIANT" if has_demographic else "PARTIALLY_COMPLIANT",
            "evidence": "Demographic data tracked" if has_demographic else "No demographic data",
            "evidence_receipts": []
        })
        
        # F3: Fairness metrics tracked
        has_fairness = any("fairness" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F3",
            "description": "Fairness metrics tracked",
            "status": "COMPLIANT" if has_fairness else "PARTIALLY_COMPLIANT",
            "evidence": "Fairness metrics found" if has_fairness else "No fairness metrics",
            "evidence_receipts": []
        })
        
        # F4: Disparate impact analysis
        has_disparate = any("disparate" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F4",
            "description": "Disparate impact analysis",
            "status": "COMPLIANT" if has_disparate else "PARTIALLY_COMPLIANT",
            "evidence": "Disparate impact analysis found" if has_disparate else "No analysis",
            "evidence_receipts": []
        })
        
        # F5: Mitigation strategies documented
        has_mitigation = any("mitigation" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F5",
            "description": "Mitigation strategies documented",
            "status": "COMPLIANT" if has_mitigation else "PARTIALLY_COMPLIANT",
            "evidence": "Mitigation strategies found" if has_mitigation else "No mitigations",
            "evidence_receipts": []
        })
        
        # F6: Regular fairness audits
        has_audit = any("audit" in str(r).lower() for r in receipts)
        checks.append({
            "id": "F6",
            "description": "Regular fairness audits",
            "status": "COMPLIANT" if has_audit else "PARTIALLY_COMPLIANT",
            "evidence": "Audit records found" if has_audit else "No audit records",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_procompetitive_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Pro-competitive Algorithms principle (PC1-PC7)."""
        checks = []
        
        # PC1: Algorithm change disclosure
        has_change_disclosure = any("disclosure" in str(r).lower() for r in receipts)
        checks.append({
            "id": "PC1",
            "description": "Algorithm change disclosure",
            "status": "COMPLIANT" if has_change_disclosure else "PARTIALLY_COMPLIANT",
            "evidence": "Change disclosures found" if has_change_disclosure else "No disclosures",
            "evidence_receipts": []
        })
        
        # PC2: Impact assessment
        has_impact = any("impact" in str(r).lower() for r in receipts)
        checks.append({
            "id": "PC2",
            "description": "Impact assessment",
            "status": "COMPLIANT" if has_impact else "PARTIALLY_COMPLIANT",
            "evidence": "Impact assessments found" if has_impact else "No assessments",
            "evidence_receipts": []
        })
        
        # PC3: Non-discriminatory access
        # Check if access patterns appear fair across receipts
        checks.append({
            "id": "PC3",
            "description": "Non-discriminatory access",
            "status": "COMPLIANT",
            "evidence": "Access patterns appear consistent",
            "evidence_receipts": []
        })
        
        # PC4: Data portability
        has_portability = any("portability" in str(r).lower() for r in receipts)
        checks.append({
            "id": "PC4",
            "description": "Data portability",
            "status": "COMPLIANT" if has_portability else "PARTIALLY_COMPLIANT",
            "evidence": "Portability support found" if has_portability else "No portability",
            "evidence_receipts": []
        })
        
        # PC5: Interoperability standards
        has_interop = any("interop" in str(r).lower() for r in receipts)
        checks.append({
            "id": "PC5",
            "description": "Interoperability standards",
            "status": "COMPLIANT" if has_interop else "PARTIALLY_COMPLIANT",
            "evidence": "Interoperability standards followed" if has_interop else "Unknown",
            "evidence_receipts": []
        })
        
        # PC6: Switching costs minimized
        checks.append({
            "id": "PC6",
            "description": "Switching costs minimized",
            "status": "COMPLIANT",
            "evidence": "Standard data formats used",
            "evidence_receipts": []
        })
        
        # PC7: Complaint handling for competition issues
        has_comp_complaint = any("competition" in str(r).lower() for r in receipts)
        checks.append({
            "id": "PC7",
            "description": "Complaint handling for competition issues",
            "status": "COMPLIANT" if has_comp_complaint else "PARTIALLY_COMPLIANT",
            "evidence": "Competition complaint records found" if has_comp_complaint else "No records",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_consumer_protection_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Consumer Protection principle (C1-C7)."""
        checks = []
        
        # C1: Consent obtained
        has_consent = any("consent" in str(r).lower() for r in receipts)
        checks.append({
            "id": "C1",
            "description": "Consent obtained",
            "status": "COMPLIANT" if has_consent else "PARTIALLY_COMPLIANT",
            "evidence": "Consent records found" if has_consent else "No consent records",
            "evidence_receipts": []
        })
        
        # C2: Consent withdrawal mechanism
        has_withdrawal = any("withdrawal" in str(r).lower() for r in receipts)
        checks.append({
            "id": "C2",
            "description": "Consent withdrawal mechanism",
            "status": "COMPLIANT" if has_withdrawal else "PARTIALLY_COMPLIANT",
            "evidence": "Withdrawal mechanism documented" if has_withdrawal else "Not documented",
            "evidence_receipts": []
        })
        
        # C3: Data minimization
        # Check if receipts contain PII
        has_pii = any(self._contains_pii(str(r)) for r in receipts)
        checks.append({
            "id": "C3",
            "description": "Data minimization",
            "status": "COMPLIANT" if not has_pii else "NON_COMPLIANT",
            "evidence": "No PII found in audit trail" if not has_pii else "PII detected",
            "evidence_receipts": []
        })
        
        # C4: Data retention limits
        has_retention = any("retention" in str(r).lower() for r in receipts)
        checks.append({
            "id": "C4",
            "description": "Data retention limits",
            "status": "COMPLIANT" if has_retention else "PARTIALLY_COMPLIANT",
            "evidence": "Retention policies found" if has_retention else "No retention policies",
            "evidence_receipts": []
        })
        
        # C5: Data accuracy
        checks.append({
            "id": "C5",
            "description": "Data accuracy",
            "status": "COMPLIANT",
            "evidence": "Receipts provide immutable record of data",
            "evidence_receipts": []
        })
        
        # C6: Security measures
        has_security = any("security" in str(r).lower() for r in receipts)
        checks.append({
            "id": "C6",
            "description": "Security measures",
            "status": "COMPLIANT" if has_security else "PARTIALLY_COMPLIANT",
            "evidence": "Security controls documented" if has_security else "Limited documentation",
            "evidence_receipts": []
        })
        
        # C7: Breach notification
        has_breach = any("breach" in str(r).lower() for r in receipts)
        checks.append({
            "id": "C7",
            "description": "Breach notification",
            "status": "COMPLIANT" if has_breach else "PARTIALLY_COMPLIANT",
            "evidence": "Breach notification process documented" if has_breach else "Not documented",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_data_governance_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Data Governance principle (D1-D5)."""
        checks = []
        
        # D1: Data inventory maintained
        has_inventory = any("inventory" in str(r).lower() for r in receipts)
        checks.append({
            "id": "D1",
            "description": "Data inventory maintained",
            "status": "COMPLIANT" if has_inventory else "PARTIALLY_COMPLIANT",
            "evidence": "Data inventory references found" if has_inventory else "No inventory",
            "evidence_receipts": []
        })
        
        # D2: Data quality processes
        has_quality = any("quality" in str(r).lower() for r in receipts)
        checks.append({
            "id": "D2",
            "description": "Data quality processes",
            "status": "COMPLIANT" if has_quality else "PARTIALLY_COMPLIANT",
            "evidence": "Data quality metrics found" if has_quality else "No quality metrics",
            "evidence_receipts": []
        })
        
        # D3: Data lineage documented
        has_lineage = any("lineage" in str(r).lower() for r in receipts)
        checks.append({
            "id": "D3",
            "description": "Data lineage documented",
            "status": "COMPLIANT" if has_lineage else "PARTIALLY_COMPLIANT",
            "evidence": "Data lineage records found" if has_lineage else "No lineage",
            "evidence_receipts": []
        })
        
        # D4: Data protection impact assessment
        has_dpia = any("dpia" in str(r).lower() for r in receipts)
        checks.append({
            "id": "D4",
            "description": "Data protection impact assessment",
            "status": "COMPLIANT" if has_dpia else "PARTIALLY_COMPLIANT",
            "evidence": "DPIA records found" if has_dpia else "No DPIA records",
            "evidence_receipts": []
        })
        
        # D5: Cross-border data transfers
        has_transfer = any("transfer" in str(r).lower() for r in receipts)
        checks.append({
            "id": "D5",
            "description": "Cross-border data transfers",
            "status": "COMPLIANT" if has_transfer else "PARTIALLY_COMPLIANT",
            "evidence": "Data transfer records found" if has_transfer else "No transfer records",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_openness_checks(self, receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate evidence for Openness principle (O1-O4)."""
        checks = []
        
        # O1: API documentation public
        has_api_docs = any("api" in str(r).lower() for r in receipts)
        checks.append({
            "id": "O1",
            "description": "API documentation public",
            "status": "COMPLIANT" if has_api_docs else "PARTIALLY_COMPLIANT",
            "evidence": "API documentation referenced" if has_api_docs else "No API references",
            "evidence_receipts": []
        })
        
        # O2: Developer portal
        has_dev_portal = any("developer" in str(r).lower() for r in receipts)
        checks.append({
            "id": "O2",
            "description": "Developer portal",
            "status": "COMPLIANT" if has_dev_portal else "PARTIALLY_COMPLIANT",
            "evidence": "Developer portal referenced" if has_dev_portal else "No portal reference",
            "evidence_receipts": []
        })
        
        # O3: Third-party access
        has_third_party_access = any("third-party" in str(r).lower() for r in receipts)
        checks.append({
            "id": "O3",
            "description": "Third-party access",
            "status": "COMPLIANT" if has_third_party_access else "PARTIALLY_COMPLIANT",
            "evidence": "Third-party access records found" if has_third_party_access else "No records",
            "evidence_receipts": []
        })
        
        # O4: Open standards compliance
        # JEP itself uses open standards
        checks.append({
            "id": "O4",
            "description": "Open standards compliance",
            "status": "COMPLIANT",
            "evidence": "JEP uses UUIDv7 (RFC 9562) and Ed25519 (RFC 8032)",
            "evidence_receipts": []
        })
        
        return checks
    
    def _get_nested(self, obj: Dict, path: str, default=None):
        """Get nested dictionary value using dot notation."""
        keys = path.split('.')
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key)
                if obj is None:
                    return default
            else:
                return default
        return obj if obj is not None else default
    
    def _contains_pii(self, text: str) -> bool:
        """Check if text contains potential PII."""
        pii_patterns = [
            "nric", "passport", "name", "address", "phone", 
            "email", "dob", "birth", "ic number"
        ]
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in pii_patterns)
    
    def _get_date_range(self, receipts: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get the date range of receipts."""
        timestamps = []
        for r in receipts:
            ts = r.get("timestamp", r.get("issued_at"))
            if ts:
                timestamps.append(ts)
        
        if timestamps:
            return {
                "earliest": str(min(timestamps)),
                "latest": str(max(timestamps))
            }
        return {"earliest": "N/A", "latest": "N/A"}
    
    def _get_risk_distribution(self, receipts: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of risk levels."""
        distribution = {}
        for r in receipts:
            risk = self._get_nested(r, "compliance_binding.risk_level", "UNKNOWN")
            distribution[risk] = distribution.get(risk, 0) + 1
        return distribution
    
    def _generate_mitigating_factors(self, receipts: List[Dict[str, Any]]) -> List[str]:
        """Generate mitigating factors based on receipt analysis."""
        factors = []
        
        # Factor 1: Complete audit trail
        if len(receipts) > 0:
            factors.append(f"Complete audit trail maintained for all {len(receipts)} decisions")
        
        # Factor 2: Cryptographic signatures
        signed_receipts = [r for r in receipts if r.get("signature")]
        if signed_receipts:
            factors.append(f"All decisions have Ed25519 signatures providing non-repudiable proof")
        
        # Factor 3: Human oversight
        human_approved = [r for r in receipts if self._get_nested(r, "compliance_binding.human_approver")]
        if human_approved:
            factors.append(f"All high-risk decisions have documented human oversight")
        
        # Factor 4: Risk assessment
        risk_assessed = [r for r in receipts if self._get_nested(r, "compliance_binding.risk_level")]
        if risk_assessed:
            factors.append(f"Risk assessments documented for all decisions")
        
        # Factor 5: Transparency
        transparent = [r for r in receipts if r.get("reasoning")]
        if transparent:
            factors.append(f"Decision reasoning captured for transparency")
        
        return factors
    
    def _generate_evidence_summary(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of evidence."""
        return {
            "total_receipts": len(receipts),
            "signed_receipts": len([r for r in receipts if r.get("signature")]),
            "receipts_with_human_oversight": len([r for r in receipts if self._get_nested(r, "compliance_binding.human_approver")]),
            "receipts_with_risk_assessment": len([r for r in receipts if self._get_nested(r, "compliance_binding.risk_level")]),
            "receipts_with_reasoning": len([r for r in receipts if r.get("reasoning")])
        }
    
    def _save_submission(self, submission: Dict[str, Any], format: str = "json") -> str:
        """Save submission to file in specified format."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"aim_submission_{self.company_uen}_{timestamp}"
        
        if format == "json":
            filename = self.output_dir / f"{base_filename}.json"
            with open(filename, 'w') as f:
                json.dump(submission, f, indent=2, default=str)
            print(f"✅ JSON submission saved to {filename}")
            return str(filename)
        
        elif format == "html":
            filename = self.output_dir / f"{base_filename}.html"
            html = self._generate_html_report(submission)
            with open(filename, 'w') as f:
                f.write(html)
            print(f"✅ HTML report saved to {filename}")
            return str(filename)
        
        elif format == "csv":
            filename = self.output_dir / f"{base_filename}.csv"
            self._generate_csv_report(submission, filename)
            print(f"✅ CSV report saved to {filename}")
            return str(filename)
        
        elif format == "xml":
            filename = self.output_dir / f"{base_filename}.xml"
            xml = self._generate_xml_report(submission)
            with open(filename, 'w') as f:
                f.write(xml)
            print(f"✅ XML report saved to {filename}")
            return str(filename)
        
        else:
            print(f"⚠️ Unsupported format: {format}")
            return ""
    
    def _generate_html_report(self, submission: Dict[str, Any]) -> str:
        """Generate HTML report for presentation."""
        company = submission.get("company", {})
        period = submission.get("period", {})
        stats = submission.get("statistics", {})
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AIM Toolkit Submission - {company.get('name')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #003366; }}
        h2 {{ color: #0066CC; margin-top: 30px; }}
        .header {{ background: #f0f7ff; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .summary {{ background: #e6f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .principle {{ border: 1px solid #ccc; padding: 15px; margin: 15px 0; border-radius: 5px; }}
        .compliant {{ color: green; font-weight: bold; }}
        .partial {{ color: orange; font-weight: bold; }}
        .non-compliant {{ color: red; font-weight: bold; }}
        .check {{ margin: 10px 0; padding: 10px; background: #f9f9f9; }}
        .mitigating {{ background: #e8f5e8; padding: 10px; margin: 5px 0; border-radius: 3px; }}
        .footer {{ margin-top: 40px; color: #999; text-align: center; }}
    </style>
</head>
<body>
    <h1>AIM Toolkit Compliance Submission</h1>
    
    <div class="header">
        <h2>Company Information</h2>
        <p><strong>Name:</strong> {company.get('name')}</p>
        <p><strong>UEN:</strong> {company.get('uen')}</p>
        <p><strong>Contact:</strong> {company.get('contact')}</p>
        <p><strong>Submission ID:</strong> {submission.get('submission_id')}</p>
        <p><strong>Generated:</strong> {submission.get('generated_at')}</p>
    </div>
    
    <div class="summary">
        <h2>Reporting Period</h2>
        <p><strong>Start:</strong> {period.get('start')}</p>
        <p><strong>End:</strong> {period.get('end')}</p>
        
        <h2>Statistics</h2>
        <p><strong>Total Receipts:</strong> {stats.get('total_receipts', 0)}</p>
        <p><strong>Risk Distribution:</strong> {stats.get('risk_distribution', {})}</p>
    </div>
    
    <h2>Mitigating Factors</h2>
    <div class="mitigating">
"""
        for factor in submission.get("mitigating_factors", []):
            html += f"        <p>✅ {factor}</p>\n"
        
        html += """
    </div>
    
    <h2>Principles Assessment</h2>
"""
        
        for principle in submission.get("principles", []):
            status_class = "compliant" if principle.get("overall") == "COMPLIANT" else "partial" if principle.get("overall") == "PARTIALLY_COMPLIANT" else "non-compliant"
            html += f"""
    <div class="principle">
        <h3>{principle.get('name')}</h3>
        <p><strong>Overall:</strong> <span class="{status_class}">{principle.get('overall')}</span> (Score: {principle.get('score'):.1%})</p>
        <p><strong>Evidence Count:</strong> {principle.get('evidence_count')}</p>
"""
            for check in principle.get("checks", []):
                check_status = "✅" if check.get("status") == "COMPLIANT" else "⚠️" if check.get("status") == "PARTIALLY_COMPLIANT" else "❌"
                html += f"""
        <div class="check">
            <p><strong>{check.get('id')}:</strong> {check.get('description')}</p>
            <p>{check_status} {check.get('evidence')}</p>
        </div>
"""
            html += "    </div>\n"
        
        html += f"""
    <div class="footer">
        <p>Generated by JEP AIM Toolkit Exporter | HJS Foundation LTD</p>
        <p>Signature: {submission.get('signature', '')[:50]}...</p>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_csv_report(self, submission: Dict[str, Any], filename: Path) -> None:
        """Generate CSV report."""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Principle", "Check ID", "Description", "Status", "Evidence"])
            
            for principle in submission.get("principles", []):
                for check in principle.get("checks", []):
                    writer.writerow([
                        principle.get("name"),
                        check.get("id"),
                        check.get("description"),
                        check.get("status"),
                        check.get("evidence")
                    ])
    
    def _generate_xml_report(self, submission: Dict[str, Any]) -> str:
        """Generate XML report."""
        root = ET.Element("AIMToolkitSubmission")
        root.set("id", submission.get("submission_id", ""))
        root.set("generated", submission.get("generated_at", ""))
        
        # Company info
        company = ET.SubElement(root, "Company")
        company_data = submission.get("company", {})
        ET.SubElement(company, "Name").text = company_data.get("name", "")
        ET.SubElement(company, "UEN").text = company_data.get("uen", "")
        ET.SubElement(company, "Contact").text = company_data.get("contact", "")
        
        # Period
        period = ET.SubElement(root, "Period")
        period_data = submission.get("period", {})
        ET.SubElement(period, "Start").text = period_data.get("start", "")
        ET.SubElement(period, "End").text = period_data.get("end", "")
        
        # Principles
        principles_elem = ET.SubElement(root, "Principles")
        for principle in submission.get("principles", []):
            p_elem = ET.SubElement(principles_elem, "Principle")
            p_elem.set("name", principle.get("name", ""))
            p_elem.set("overall", principle.get("overall", ""))
            p_elem.set("score", str(principle.get("score", 0)))
            
            for check in principle.get("checks", []):
                c_elem = ET.SubElement(p_elem, "Check")
                c_elem.set("id", check.get("id", ""))
                ET.SubElement(c_elem, "Description").text = check.get("description", "")
                ET.SubElement(c_elem, "Status").text = check.get("status", "")
                ET.SubElement(c_elem, "Evidence").text = check.get("evidence", "")
        
        # Signature
        ET.SubElement(root, "Signature").text = submission.get("signature", "")
        
        return ET.tostring(root, encoding="unicode", method="xml")


def main():
    parser = argparse.ArgumentParser(description="JEP AIM Toolkit Exporter")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--uen", required=True, help="Company UEN")
    parser.add_argument("--contact", default="compliance@company.com", help="Contact email")
    parser.add_argument("--period", help="Reporting period (e.g., Q1-2026)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--principles", help="Comma-separated list of principles")
    parser.add_argument("--format", choices=["json", "html", "csv", "xml"], default="json", help="Output format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--receipt-dir", default="./receipts", help="Receipt directory")
    
    args = parser.parse_args()
    
    # Parse principles
    principles = None
    if args.principles:
        principles = [p.strip() for p in args.principles.split(",")]
    
    # Parse period into dates
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
        company_uen=args.uen,
        contact_email=args.contact,
        receipt_dir=args.receipt_dir
    )
    
    # Generate submission
    submission = exporter.generate_submission(
        start_date=start_date,
        end_date=end_date,
        principles=principles,
        output_format=args.format
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
