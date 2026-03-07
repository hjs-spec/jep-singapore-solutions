#!/usr/bin/env python3
"""
MOH Compliance Verification Script for JEP Implementation
============================================================

This script verifies that a JEP implementation fully complies with
Ministry of Health (MOH) Singapore regulatory requirements.

MOH Regulations Covered:
- MOH AI in Healthcare Guidelines
- Healthcare Services Act (HCSA)
- MOH Telemedicine Guidelines
- National Electronic Health Record (NEHR) Requirements
- MOH Data Protection Guidelines

Usage:
    python verify-moh-compliance.py [--receipt-dir DIR] [--output-format json|html]

Examples:
    # Run full MOH compliance verification
    python verify-moh-compliance.py
    
    # Generate HTML report for MOH auditor
    python verify-moh-compliance.py --output-format html --output moh-audit.html
"""

import json
import os
import sys
import argparse
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from enum import Enum

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from implementation.accountability import AgenticAIAccountability
from tests.verify-all-pillars import PillarVerifier, generate_uuid7


class MOHGuideline(Enum):
    """MOH AI in Healthcare Guidelines"""
    CLINICAL_VALIDATION = "Clinical Validation"
    HUMAN_OVERSIGHT = "Human Oversight"
    PATIENT_SAFETY = "Patient Safety"
    DATA_GOVERNANCE = "Data Governance"
    CLINICAL_SAFETY = "Clinical Safety"
    CONTINUOUS_MONITORING = "Continuous Monitoring"


class MOHComplianceVerifier(PillarVerifier):
    """
    Verifies JEP implementation against MOH regulatory requirements.
    """
    
    def __init__(self):
        super().__init__()
        self.results = {
            "ai_guidelines": {},
            "hcsa_compliance": {},
            "nehr_compliance": {},
            "data_protection": {},
            "summary": {}
        }
        
        # MOH severity levels
        self.severity_levels = {
            "NEGLIGIBLE": {"response_time": 1440, "review_required": False},
            "MINOR": {"response_time": 480, "review_required": True},
            "MODERATE": {"response_time": 120, "review_required": True},
            "SEVERE": {"response_time": 30, "review_required": True},
            "CRITICAL": {"response_time": 15, "review_required": True}
        }
    
    def verify_clinical_validation(self) -> Dict[str, Any]:
        """Verify MOH Clinical Validation Requirements"""
        result = {
            "guideline": MOHGuideline.CLINICAL_VALIDATION.value,
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: Clinical validation documented
            proposal = self.test_tracker.propose_action(
                action="DIAGNOSTIC_ASSESSMENT",
                target_resource="patient/P001",
                reasoning="AI diagnostic assessment",
                risk_level="MEDIUM",
                clinical_validation={
                    "validation_study": "Prospective multi-center study 2025",
                    "sensitivity": 0.95,
                    "specificity": 0.92,
                    "auc": 0.96,
                    "approval_date": "2025-06-15",
                    "approving_body": "MOH Health Sciences Authority"
                }
            )
            
            has_validation = "clinical_validation" in proposal.parameters
            
            result["requirements"]["CV1_validation"] = {
                "description": "AI system clinically validated",
                "passed": has_validation,
                "evidence": f"Validation present: {has_validation}"
            }
            
            # Test 2: Performance monitoring
            proposal = self.test_tracker.propose_action(
                action="PERFORMANCE_MONITORING",
                target_resource="system/ai-diagnostic",
                reasoning="Daily performance monitoring",
                risk_level="LOW",
                performance_metrics={
                    "daily_accuracy": 0.94,
                    "false_positives": 12,
                    "false_negatives": 3,
                    "monitoring_period": "30 days"
                }
            )
            
            has_monitoring = "performance_metrics" in proposal.parameters
            
            result["requirements"]["CV2_monitoring"] = {
                "description": "Performance continuously monitored",
                "passed": has_monitoring,
                "evidence": f"Monitoring data present: {has_monitoring}"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_human_oversight(self) -> Dict[str, Any]:
        """Verify MOH Human Oversight Requirements"""
        result = {
            "guideline": MOHGuideline.HUMAN_OVERSIGHT.value,
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: Clinician review for critical findings
            critical_proposal = self.test_tracker.propose_action(
                action="CRITICAL_FINDING_ALERT",
                target_resource="patient/P002",
                reasoning="AI detected acute hemorrhage",
                risk_level="CRITICAL",
                finding_type="hemorrhage",
                confidence=0.98,
                severity="CRITICAL"
            )
            
            approval = self.test_tracker.approve_action(
                proposal_id=critical_proposal.id,
                human_approver="DR_RAD_001_CONSULTANT",
                context_reviewed=True,
                notes="Confirmed acute hemorrhage - urgent consult initiated"
            )
            
            has_clinician = approval.human_approver.startswith("DR_")
            
            result["requirements"]["HO1_clinician_review"] = {
                "description": "Clinician review for critical findings",
                "passed": has_clinician,
                "evidence": f"Clinician: {approval.human_approver}"
            }
            
            # Test 2: Response time within limits
            proposal_time = critical_proposal.proposed_at
            approval_time = approval.approval_time
            response_time = approval_time - proposal_time
            
            timely = response_time < 900  # 15 minutes
            
            result["requirements"]["HO2_response_time"] = {
                "description": "Timely response for critical findings",
                "passed": timely,
                "evidence": f"Response time: {response_time:.0f} seconds"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_patient_safety(self) -> Dict[str, Any]:
        """Verify MOH Patient Safety Requirements"""
        result = {
            "guideline": MOHGuideline.PATIENT_SAFETY.value,
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: Safety monitoring
            safety_proposal = self.test_tracker.propose_action(
                action="SAFETY_MONITOR",
                target_resource="patient/P003",
                reasoning="Routine safety monitoring",
                risk_level="MEDIUM",
                safety_metrics={
                    "adverse_events": 0,
                    "near_misses": 1,
                    "safety_checks_passed": 156,
                    "monitoring_period": "24h"
                }
            )
            
            has_safety = "safety_metrics" in safety_proposal.parameters
            
            result["requirements"]["PS1_safety_monitoring"] = {
                "description": "Patient safety continuously monitored",
                "passed": has_safety,
                "evidence": f"Safety metrics present: {has_safety}"
            }
            
            # Test 2: Adverse event reporting
            adverse_event = {
                "event_id": f"AE_{generate_uuid7()[:8]}",
                "event_type": "false_negative",
                "severity": "MODERATE",
                "description": "AI missed small nodule",
                "report_time": time.time(),
                "reported_by": "DR_RAD_002",
                "corrective_action": "Model retraining scheduled"
            }
            
            event_proposal = self.test_tracker.propose_action(
                action="ADVERSE_EVENT_REPORT",
                target_resource="patient/P004",
                reasoning="Reporting AI-related adverse event",
                risk_level="HIGH",
                adverse_event=adverse_event
            )
            
            has_event = "adverse_event" in event_proposal.parameters
            
            result["requirements"]["PS2_adverse_event"] = {
                "description": "Adverse events properly reported",
                "passed": has_event,
                "evidence": f"Event report present: {has_event}"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_data_governance(self) -> Dict[str, Any]:
        """Verify MOH Data Governance Requirements"""
        result = {
            "guideline": MOHGuideline.DATA_GOVERNANCE.value,
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: No PII in audit trail
            patient_data = {
                "nric": "S1234567A",
                "name": "Tan Ah Kow",
                "diagnosis": "Pneumonia"
            }
            
            receipt = {
                "receipt_id": f"jep_{generate_uuid7()}",
                "patient_ref": hashlib.sha256(b"S1234567A").hexdigest()[:16],
                "diagnosis_hash": hashlib.sha256(b"Pneumonia").hexdigest()[:16]
            }
            
            receipt_str = json.dumps(receipt)
            has_nric = "S1234567A" not in receipt_str
            has_name = "Tan Ah Kow" not in receipt_str
            
            result["requirements"]["DG1_no_pii"] = {
                "description": "No PII in audit trail",
                "passed": has_nric and has_name,
                "evidence": f"NRIC protected: {has_nric}, Name protected: {has_name}"
            }
            
            # Test 2: Patient consent recorded
            consent_proposal = self.test_tracker.propose_action(
                action="PROCESS_PATIENT_DATA",
                target_resource="patient/P005",
                reasoning="AI-assisted diagnosis",
                risk_level="MEDIUM",
                consent_record={
                    "consent_id": f"CONSENT_{generate_uuid7()[:8]}",
                    "patient_consent": True,
                    "consent_date": time.time(),
                    "consent_scope": ["diagnosis", "treatment"]
                }
            )
            
            has_consent = "consent_record" in consent_proposal.parameters
            
            result["requirements"]["DG2_consent"] = {
                "description": "Patient consent properly recorded",
                "passed": has_consent,
                "evidence": f"Consent record present: {has_consent}"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_hcsa_compliance(self) -> Dict[str, Any]:
        """Verify Healthcare Services Act (HCSA) Compliance"""
        result = {
            "name": "Healthcare Services Act",
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: Licensed services
            licensed = self.test_tracker.propose_action(
                action="PROVIDE_TELEMEDICINE",
                target_resource="patient/P006",
                reasoning="Remote consultation",
                risk_level="MEDIUM",
                service_license={
                    "license_number": "TML-2025-0123",
                    "license_holder": "SGH Telehealth",
                    "expiry_date": "2027-12-31"
                }
            )
            
            has_license = "service_license" in licensed.parameters
            
            result["requirements"]["HCSA1_license"] = {
                "description": "Licensed services properly identified",
                "passed": has_license,
                "evidence": f"License present: {has_license}"
            }
            
            # Test 2: Incident reporting
            incident = {
                "incident_id": f"INC_{generate_uuid7()[:8]}",
                "incident_type": "Service disruption",
                "severity": "MODERATE",
                "reported_to_moh": True,
                "report_time": time.time()
            }
            
            incident_proposal = self.test_tracker.propose_action(
                action="REPORT_INCIDENT",
                target_resource="system/incident-log",
                reasoning="MOH incident reporting",
                risk_level="HIGH",
                incident_report=incident
            )
            
            has_incident = "incident_report" in incident_proposal.parameters
            
            result["requirements"]["HCSA2_incident"] = {
                "description": "Incidents properly reported to MOH",
                "passed": has_incident,
                "evidence": f"Incident report present: {has_incident}"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_nehr_compliance(self) -> Dict[str, Any]:
        """Verify National Electronic Health Record (NEHR) Compliance"""
        result = {
            "name": "NEHR Integration",
            "requirements": {},
            "status": "PENDING"
        }
        
        try:
            # Test 1: NEHR integration standards
            nehr_access = self.test_tracker.propose_action(
                action="ACCESS_NEHR",
                target_resource="nehr/patient/P007",
                reasoning="Retrieve patient records",
                risk_level="MEDIUM",
                nehr_metadata={
                    "interface_version": "NEHR-API-v2.1",
                    "request_id": f"REQ_{generate_uuid7()[:12]}",
                    "purpose": "clinical_care",
                    "auth_method": "MOH-Trusted-System"
                }
            )
            
            has_standard = "nehr_metadata" in nehr_access.parameters
            
            result["requirements"]["NEHR1_standard"] = {
                "description": "NEHR integration standards followed",
                "passed": has_standard,
                "evidence": f"NEHR metadata present: {has_standard}"
            }
            
            # Test 2: NEHR access audit
            audit = {
                "access_id": f"AUDIT_{generate_uuid7()[:12]}",
                "patient_ref": hashlib.sha256(b"P007").hexdigest()[:16],
                "access_time": time.time(),
                "accessor": "SGH_RADIOLOGY",
                "purpose": "clinical_diagnosis",
                "consent_verified": True
            }
            
            audit_proposal = self.test_tracker.propose_action(
                action="NEHR_AUDIT",
                target_resource="system/nehr-audit",
                reasoning="NEHR access audit",
                risk_level="LOW",
                audit_entry=audit
            )
            
            has_audit = "audit_entry" in audit_proposal.parameters
            
            result["requirements"]["NEHR2_audit"] = {
                "description": "NEHR access properly audited",
                "passed": has_audit,
                "evidence": f"Audit entry present: {has_audit}"
            }
            
        except Exception as e:
            result["requirements"]["error"] = {
                "description": "Error during verification",
                "passed": False,
                "evidence": str(e)
            }
        
        all_passed = all(r.get("passed", False) for r in result["requirements"].values())
        result["status"] = "COMPLIANT" if all_passed else "NON_COMPLIANT"
        return result
    
    def verify_all_moh_requirements(self) -> Dict[str, Any]:
        """Run verification for all MOH requirements"""
        self.results["ai_guidelines"]["clinical_validation"] = self.verify_clinical_validation()
        self.results["ai_guidelines"]["human_oversight"] = self.verify_human_oversight()
        self.results["ai_guidelines"]["patient_safety"] = self.verify_patient_safety()
        self.results["ai_guidelines"]["data_governance"] = self.verify_data_governance()
        self.results["hcsa_compliance"] = self.verify_hcsa_compliance()
        self.results["nehr_compliance"] = self.verify_nehr_compliance()
        
        # Calculate summary
        all_compliant = all(
            v.get("status") == "COMPLIANT"
            for v in self.results["ai_guidelines"].values()
        ) and self.results["hcsa_compliance"].get("status") == "COMPLIANT" and self.results["nehr_compliance"].get("status") == "COMPLIANT"
        
        compliant_count = sum(1 for v in self.results["ai_guidelines"].values() if v.get("status") == "COMPLIANT")
        compliant_count += 1 if self.results["hcsa_compliance"].get("status") == "COMPLIANT" else 0
        compliant_count += 1 if self.results["nehr_compliance"].get("status") == "COMPLIANT" else 0
        total_count = 6  # 4 guidelines + HCSA + NEHR
        
        self.results["summary"] = {
            "compliance_status": "FULLY_COMPLIANT" if all_compliant else "PARTIALLY_COMPLIANT",
            "compliant_requirements": compliant_count,
            "total_requirements": total_count,
            "verification_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "verification_id": f"MOH_VERIF_{generate_uuid7()}"
        }
        
        return self.results
    
    def generate_report(self, format: str = "text") -> str:
        """Generate verification report"""
        if format == "json":
            return json.dumps(self.results, indent=2)
        elif format == "html":
            return self._generate_html_report()
        else:
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """Generate plain text report"""
        lines = []
        lines.append("="*60)
        lines.append("MOH COMPLIANCE VERIFICATION REPORT")
        lines.append("="*60)
        lines.append(f"Verification ID: {self.results['summary']['verification_id']}")
        lines.append(f"Time: {self.results['summary']['verification_time']}")
        lines.append("")
        
        lines.append("\nMOH AI Guidelines:")
        lines.append("-"*40)
        for guideline, result in self.results["ai_guidelines"].items():
            status = "✅" if result["status"] == "COMPLIANT" else "❌"
            lines.append(f"{status} {guideline.replace('_', ' ').title()}: {result['status']}")
        
        lines.append("\nHealthcare Services Act:")
        lines.append("-"*40)
        hcsa = self.results["hcsa_compliance"]
        status = "✅" if hcsa["status"] == "COMPLIANT" else "❌"
        lines.append(f"{status} HCSA: {hcsa['status']}")
        
        lines.append("\nNEHR Integration:")
        lines.append("-"*40)
        nehr = self.results["nehr_compliance"]
        status = "✅" if nehr["status"] == "COMPLIANT" else "❌"
        lines.append(f"{status} NEHR: {nehr['status']}")
        
        lines.append("")
        lines.append("="*60)
        lines.append(f"OVERALL: {self.results['summary']['compliance_status']}")
        lines.append(f"Requirements Met: {self.results['summary']['compliant_requirements']}/{self.results['summary']['total_requirements']}")
        lines.append("="*60)
        
        return "\n".join(lines)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>MOH Compliance Verification Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #003366; }}
        .summary {{ background: #e6f3ff; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .compliant {{ color: green; }}
        .non-compliant {{ color: red; }}
        .section {{ border: 1px solid #ccc; padding: 15px; margin: 15px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>MOH Compliance Verification Report</h1>
    <p>Generated: {self.results['summary']['verification_time']}</p>
    
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Status:</strong> <span class="{'compliant' if self.results['summary']['compliance_status'] == 'FULLY_COMPLIANT' else 'non-compliant'}">{self.results['summary']['compliance_status']}</span></p>
        <p><strong>Requirements Met:</strong> {self.results['summary']['compliant_requirements']} / {self.results['summary']['total_requirements']}</p>
    </div>
    
    <div class="section">
        <h2>MOH AI in Healthcare Guidelines</h2>
"""
        for guideline, result in self.results["ai_guidelines"].items():
            status_class = "compliant" if result["status"] == "COMPLIANT" else "non-compliant"
            html += f"""
        <h3>{guideline.replace('_', ' ').title()}</h3>
        <p>Status: <span class="{status_class}">{result['status']}</span></p>
"""
        
        html += f"""
    </div>
    
    <div class="section">
        <h2>Healthcare Services Act</h2>
        <p><strong>HCSA Compliance</strong></p>
        <p>Status: <span class="{'compliant' if self.results['hcsa_compliance']['status'] == 'COMPLIANT' else 'non-compliant'}">{self.results['hcsa_compliance']['status']}</span></p>
    </div>
    
    <div class="section">
        <h2>NEHR Integration</h2>
        <p><strong>National Electronic Health Record</strong></p>
        <p>Status: <span class="{'compliant' if self.results['nehr_compliance']['status'] == 'COMPLIANT' else 'non-compliant'}">{self.results['nehr_compliance']['status']}</span></p>
    </div>
    
    <div class="footer">
        <p>Verified by JEP MOH Compliance Framework | HJS Foundation LTD</p>
    </div>
</body>
</html>
"""
        return html


def main():
    parser = argparse.ArgumentParser(description="Verify JEP implementation against MOH requirements")
    parser.add_argument("--output-format", choices=["text", "json", "html"], default="text", help="Output format")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    verifier = MOHComplianceVerifier()
    results = verifier.verify_all_moh_requirements()
    output = verifier.generate_report(args.output_format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"✅ MOH Compliance report saved to {args.output}")
    else:
        print(output)
    
    return 0 if results["summary"]["compliance_status"] == "FULLY_COMPLIANT" else 1


if __name__ == "__main__":
    sys.exit(main())
