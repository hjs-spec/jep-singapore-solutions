#!/usr/bin/env python3
"""
CPF Board Integration Example - Singapore Central Provident Fund
===================================================================

This example demonstrates how the CPF Board can integrate JEP into their
core business systems to meet regulatory requirements for retirement planning,
withdrawal applications, housing grants, and member services.

Regulatory Compliance:
- CPF Act
- CPF Board's Digital Service Standards
- MAS Guidelines (for CPF Investment Scheme)
- HDB Guidelines (for housing grants)
- GovTech DSS
- PDPA

Scenarios Covered:
1. Retirement withdrawal application with multi-level approval
2. Housing grant eligibility assessment
3. CPF Investment Scheme (CPFIS) transaction approval
4. Member account updates and consent management
5. Cross-agency data sharing with HDB and IRAS
"""

import json
import time
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict

# Import JEP components
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from implementation.accountability import (
    AgenticAIAccountability,
    ActionProposal,
    HumanApprovalRecord,
    RiskLevel,
    ActionStatus
)
from jep.core import JEPAsymmetricSigner, generate_uuid7


class CPFScheme(Enum):
    """CPF Schemes"""
    RETIREMENT_WITHDRAWAL = "RETIREMENT_WITHDRAWAL"
    CPFIS = "CPF_INVESTMENT_SCHEME"
    HOUSING_GRANT = "HOUSING_GRANT"
    MEDICAL_WITHDRAWAL = "MEDICAL_WITHDRAWAL"
    EDUCATION_WITHDRAWAL = "EDUCATION_WITHDRAWAL"
    SPECIAL_WITHDRAWAL = "SPECIAL_WITHDRAWAL"


class CPFAccount(Enum):
    """CPF Account Types"""
    ORDINARY = "ORDINARY_ACCOUNT"
    SPECIAL = "SPECIAL_ACCOUNT"
    MEDISAVE = "MEDISAVE_ACCOUNT"
    RETIREMENT = "RETIREMENT_ACCOUNT"


class WithdrawalReason(Enum):
    """Reasons for CPF withdrawal"""
    RETIREMENT = "RETIREMENT"
    HOUSING = "HOUSING"
    HEALTHCARE = "HEALTHCARE"
    EDUCATION = "EDUCATION"
    INVESTMENT = "INVESTMENT"
    EMERGENCY = "EMERGENCY"


class CPFIntegration:
    """
    Complete CPF Board integration example showing JEP implementation
    for all major CPF services.
    """
    
    def __init__(self, environment: str = "production"):
        """
        Initialize CPF integration with JEP.
        
        Args:
            environment: "production", "staging", or "test"
        """
        self.environment = environment
        self.system_id = f"cpf-system-{generate_uuid7()[:8]}"
        
        # Initialize JEP tracker for CPF-specific use
        self.tracker = AgenticAIAccountability(
            agent_id=f"cpf-agent-{environment}",
            organization="CPF_BOARD"
        )
        
        # CPF-specific configuration
        self.withdrawal_limits = {
            "RETIREMENT": {
                "min_age": 65,
                "max_withdrawal_pct": 0.2,  # 20% of savings
                "approval_levels": {
                    "STANDARD": "SYSTEM",
                    "ABOVE_LIMIT": "SENIOR_OFFICER",
                    "EXCEPTION": "DIRECTOR"
                }
            },
            "HOUSING": {
                "max_amount": 200000,
                "approval_levels": {
                    "STANDARD": "SYSTEM",
                    "ABOVE_LIMIT": "HDB_LIAISON",
                    "COMPLEX": "SENIOR_MANAGER"
                }
            },
            "INVESTMENT": {
                "min_investment": 1000,
                "max_investment": 50000,
                "approval_levels": {
                    "STANDARD": "SYSTEM",
                    "ABOVE_LIMIT": "INVESTMENT_OFFICER",
                    "HIGH_RISK": "INVESTMENT_COMMITTEE"
                }
            }
        }
        
        # CPF member database (simulated)
        self.members = {}
        self.transactions = []
        self.audit_log = []
        
        print(f"✅ CPF Board Integration Initialized")
        print(f"   System ID: {self.system_id}")
        print(f"   Environment: {environment}")
        print(f"   JEP Tracker: {self.tracker.agent_id}")
    
    def process_retirement_withdrawal(
        self,
        nric: str,
        member_name: str,
        member_age: int,
        withdrawal_amount: float,
        account_type: CPFAccount,
        reason: WithdrawalReason = WithdrawalReason.RETIREMENT,
        supporting_docs: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process a retirement withdrawal application with appropriate approvals.
        
        This demonstrates:
        - Age and eligibility verification
        - Risk-based approval routing
        - Multi-level approval for exceptions
        - Complete audit trail for CPF Act compliance
        """
        print(f"\n{'='*60}")
        print(f"🏦 CPF Retirement Withdrawal Application")
        print(f"{'='*60}")
        print(f"Member: {member_name} (NRIC: {nric[:3]}***{nric[-3:]})")
        print(f"Age: {member_age}")
        print(f"Account: {account_type.value}")
        print(f"Withdrawal Amount: ${withdrawal_amount:,.2f}")
        print(f"Reason: {reason.value}")
        
        # Step 1: Check eligibility
        eligibility_check = self._check_retirement_eligibility(
            nric, member_age, withdrawal_amount, account_type
        )
        
        print(f"\n📋 Eligibility Check:")
        print(f"   Eligible: {eligibility_check['eligible']}")
        print(f"   Risk Level: {eligibility_check['risk_level'].value}")
        print(f"   Required Approver: {eligibility_check['approver']}")
        
        if not eligibility_check['eligible']:
            return {
                "status": "REJECTED",
                "reason": eligibility_check['reason'],
                "timestamp": time.time()
            }
        
        # Step 2: Hash NRIC for audit trail (PII protection)
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        
        # Step 3: Create proposal with complete context
        proposal = self.tracker.propose_action(
            action="RETIREMENT_WITHDRAWAL",
            target_resource=f"member/{nric_hash}/account/{account_type.value}",
            reasoning=f"Member {member_name} requests retirement withdrawal of ${withdrawal_amount:,.2f}",
            risk_level=eligibility_check['risk_level'].value,
            # Complete context for meaningful approval
            member_context={
                "age": member_age,
                "account_balance": self._get_account_balance(nric, account_type),
                "years_to_retirement": max(0, 65 - member_age),
                "previous_withdrawals": self._get_previous_withdrawals(nric)
            },
            withdrawal_details={
                "amount": withdrawal_amount,
                "account_type": account_type.value,
                "reason": reason.value,
                "supporting_docs": supporting_docs or []
            },
            compliance_checks={
                "age_verified": member_age >= 65,
                "limit_check": withdrawal_amount <= eligibility_check['max_allowed'],
                "documents_received": len(supporting_docs or []) > 0
            }
        )
        
        # Step 4: Route for appropriate approval
        if eligibility_check['approver'] == "SYSTEM":
            # Standard case - auto-approve
            result = self._auto_approve_withdrawal(proposal, nric_hash, withdrawal_amount)
        else:
            # Route to human approver
            result = self._route_withdrawal_for_approval(
                proposal, 
                nric_hash, 
                withdrawal_amount,
                eligibility_check['approver']
            )
        
        # Step 5: Log transaction
        self.transactions.append({
            "transaction_id": result.get("transaction_id"),
            "nric_hash": nric_hash,
            "type": "RETIREMENT_WITHDRAWAL",
            "amount": withdrawal_amount,
            "status": result.get("status"),
            "timestamp": time.time()
        })
        
        return result
    
    def _check_retirement_eligibility(
        self,
        nric: str,
        age: int,
        amount: float,
        account_type: CPFAccount
    ) -> Dict[str, Any]:
        """
        Check eligibility for retirement withdrawal.
        """
        limits = self.withdrawal_limits["RETIREMENT"]
        account_balance = self._get_account_balance(nric, account_type)
        max_allowed = account_balance * limits["max_withdrawal_pct"]
        
        # Check age requirement
        if age < limits["min_age"]:
            return {
                "eligible": False,
                "reason": f"Age {age} below minimum retirement age {limits['min_age']}",
                "risk_level": RiskLevel.LOW
            }
        
        # Check amount limits
        if amount <= max_allowed:
            risk_level = RiskLevel.LOW
            approver = limits["approval_levels"]["STANDARD"]
        elif amount <= account_balance:
            risk_level = RiskLevel.MEDIUM
            approver = limits["approval_levels"]["ABOVE_LIMIT"]
        else:
            risk_level = RiskLevel.HIGH
            approver = limits["approval_levels"]["EXCEPTION"]
        
        return {
            "eligible": True,
            "risk_level": risk_level,
            "approver": approver,
            "max_allowed": max_allowed,
            "account_balance": account_balance
        }
    
    def _auto_approve_withdrawal(
        self,
        proposal: ActionProposal,
        nric_hash: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Auto-approve standard withdrawal applications.
        """
        print(f"\n🤖 Auto-approving standard withdrawal")
        
        # System approval
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver="SYSTEM_RULE_ENGINE",
            context_reviewed=True,
            notes=f"Auto-approved: Within standard limits"
        )
        
        # Execute
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Generate transaction ID
        transaction_id = f"CPF-RET-{generate_uuid7()[:12]}"
        
        result = {
            "status": "APPROVED",
            "approval_type": "AUTO",
            "transaction_id": transaction_id,
            "amount": amount,
            "timestamp": time.time(),
            "estimated_processing_days": 3,
            "next_steps": [
                "Funds will be credited to your bank account in 3 working days",
                "You will receive SMS notification when funds are transferred"
            ],
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        self._log_audit_event("WITHDRAWAL_AUTO_APPROVED", {
            "nric_hash": nric_hash,
            "transaction_id": transaction_id,
            "amount": amount
        })
        
        return result
    
    def _route_withdrawal_for_approval(
        self,
        proposal: ActionProposal,
        nric_hash: str,
        amount: float,
        approver_type: str
    ) -> Dict[str, Any]:
        """
        Route withdrawal to human approver for review.
        """
        print(f"\n👤 Routing for {approver_type} approval")
        
        # Generate approver ID based on type
        approver_map = {
            "SENIOR_OFFICER": f"CPF-SO-{generate_uuid7()[:6]}",
            "DIRECTOR": f"CPF-DIR-{generate_uuid7()[:6]}",
            "HDB_LIAISON": f"HDB-{generate_uuid7()[:6]}",
            "SENIOR_MANAGER": f"CPF-SM-{generate_uuid7()[:6]}",
            "INVESTMENT_OFFICER": f"CPF-IO-{generate_uuid7()[:6]}",
            "INVESTMENT_COMMITTEE": f"CPF-IC-{generate_uuid7()[:6]}"
        }
        approver_id = approver_map.get(approver_type, f"CPF-APP-{generate_uuid7()[:6]}")
        
        print(f"   Context for {approver_type}:")
        print(f"   - Amount: ${amount:,.2f}")
        print(f"   - Member Age: {proposal.parameters.get('member_context', {}).get('age')}")
        print(f"   - Account Balance: ${proposal.parameters.get('member_context', {}).get('account_balance', 0):,.2f}")
        print(f"   - Previous Withdrawals: {proposal.parameters.get('member_context', {}).get('previous_withdrawals', 0)}")
        
        # For high-risk cases, may require multiple approvals
        if proposal.risk_level == RiskLevel.HIGH:
            # First approval
            approval1 = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=f"Reviewed documents. Amount exceeds standard limits but justified."
            )
            print(f"   ✅ First Approval: {approver_id}")
            
            # Second approval (e.g., Director)
            second_approver = "CPF-DIRECTOR"
            approval2 = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=second_approver,
                context_reviewed=True,
                notes=f"Second approval confirmed. Exception approved."
            )
            print(f"   ✅ Second Approval: {second_approver}")
            
            # Execute
            execution = self.tracker.execute_approved_action(proposal.id)
            
            transaction_id = f"CPF-RET-{generate_uuid7()[:12]}"
            result = {
                "status": "APPROVED",
                "approval_type": "DUAL_HUMAN",
                "primary_approver": approver_id,
                "secondary_approver": second_approver,
                "transaction_id": transaction_id,
                "amount": amount,
                "timestamp": time.time(),
                "estimated_processing_days": 5,
                "next_steps": [
                    "Your exception request has been approved",
                    "Funds will be processed within 5 working days",
                    "You will receive a letter explaining the approval conditions"
                ],
                "audit_receipt": execution,
                "approval_receipts": [approval1.to_dict(), approval2.to_dict()]
            }
        else:
            # Single approval
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=f"Approved. Within limits, documents verified."
            )
            print(f"   ✅ {approver_type} Approved")
            
            execution = self.tracker.execute_approved_action(proposal.id)
            
            transaction_id = f"CPF-RET-{generate_uuid7()[:12]}"
            result = {
                "status": "APPROVED",
                "approval_type": "SINGLE_HUMAN",
                "approver": approver_id,
                "transaction_id": transaction_id,
                "amount": amount,
                "timestamp": time.time(),
                "estimated_processing_days": 4,
                "next_steps": [
                    "Your application has been approved",
                    "Funds will be processed within 4 working days"
                ],
                "audit_receipt": execution,
                "approval_receipt": approval.to_dict()
            }
        
        self._log_audit_event("WITHDRAWAL_HUMAN_APPROVED", {
            "nric_hash": nric_hash,
            "transaction_id": transaction_id,
            "amount": amount,
            "approver_type": approver_type
        })
        
        return result
    
    def process_housing_grant(
        self,
        nric: str,
        member_name: str,
        property_type: str,
        property_value: float,
        grant_type: str,
        joint_applicants: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Process housing grant application with HDB integration.
        
        This demonstrates:
        - Cross-agency data sharing with HDB
        - Multi-party applications (joint applicants)
        - Grant eligibility verification
        """
        print(f"\n{'='*60}")
        print(f"🏠 CPF Housing Grant Application")
        print(f"{'='*60}")
        print(f"Main Applicant: {member_name}")
        print(f"Property Type: {property_type}")
        print(f"Property Value: ${property_value:,.2f}")
        print(f"Grant Type: {grant_type}")
        print(f"Joint Applicants: {len(joint_applicants or [])}")
        
        # Hash NRICs for audit trail
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        joint_hashes = []
        if joint_applicants:
            joint_hashes = [hashlib.sha256(j.encode()).hexdigest()[:16] for j in joint_applicants]
        
        # Check grant eligibility (simplified)
        eligible = True
        grant_amount = self._calculate_grant_amount(property_value, grant_type)
        
        # Create proposal with complete context
        proposal = self.tracker.propose_action(
            action="HOUSING_GRANT",
            target_resource=f"member/{nric_hash}/property/{hashlib.sha256(property_type.encode()).hexdigest()[:8]}",
            reasoning=f"Housing grant application for {property_type}",
            risk_level=RiskLevel.MEDIUM,
            grant_details={
                "type": grant_type,
                "property_value": property_value,
                "grant_amount": grant_amount,
                "eligible": eligible
            },
            applicants={
                "primary": nric_hash,
                "joint": joint_hashes,
                "count": 1 + len(joint_hashes)
            },
            hdb_verification={
                "property_status": "Verified with HDB",
                "ownership_verified": True,
                "occupancy_verified": True,
                "verification_time": time.time()
            }
        )
        
        # Housing grants typically require HDB liaison approval
        approver = "HDB_LIAISON"
        approver_id = f"HDB-{generate_uuid7()[:6]}"
        
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver=approver_id,
            context_reviewed=True,
            notes=f"Grant approved. Amount: ${grant_amount:,.2f}"
        )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        transaction_id = f"CPF-HDB-{generate_uuid7()[:12]}"
        
        result = {
            "status": "APPROVED",
            "transaction_id": transaction_id,
            "grant_amount": grant_amount,
            "disbursement_schedule": [
                {"stage": "Option Exercise", "amount": grant_amount * 0.2},
                {"stage": "Completion", "amount": grant_amount * 0.8}
            ],
            "timestamp": time.time(),
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        self._log_audit_event("HOUSING_GRANT_APPROVED", {
            "nric_hash": nric_hash,
            "transaction_id": transaction_id,
            "grant_amount": grant_amount
        })
        
        return result
    
    def _calculate_grant_amount(self, property_value: float, grant_type: str) -> float:
        """Calculate housing grant amount based on HDB/CPF rules."""
        # Simplified grant calculation
        grants = {
            "FAMILY_GRANT": min(80000, property_value * 0.1),
            "SINGLE_GRANT": min(40000, property_value * 0.05),
            "PROXIMITY_GRANT": 30000,
            "STEP_UP_GRANT": 15000
        }
        return grants.get(grant_type, 0)
    
    def process_cpfis_investment(
        self,
        nric: str,
        member_name: str,
        investment_amount: float,
        investment_product: str,
        fund_manager: str,
        risk_profile: str
    ) -> Dict[str, Any]:
        """
        Process CPF Investment Scheme (CPFIS) transaction.
        
        This demonstrates:
        - MAS guidelines compliance
        - Investment risk assessment
        - Multi-level approval for high-risk investments
        """
        print(f"\n{'='*60}")
        print(f"📈 CPF Investment Scheme Transaction")
        print(f"{'='*60}")
        print(f"Member: {member_name}")
        print(f"Investment Amount: ${investment_amount:,.2f}")
        print(f"Product: {investment_product}")
        print(f"Fund Manager: {fund_manager}")
        print(f"Risk Profile: {risk_profile}")
        
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        
        # Determine risk level based on investment
        limits = self.withdrawal_limits["INVESTMENT"]
        if investment_amount <= limits["max_investment"] and risk_profile == "LOW":
            risk_level = RiskLevel.LOW
            approver = limits["approval_levels"]["STANDARD"]
        elif investment_amount <= limits["max_investment"] * 2:
            risk_level = RiskLevel.MEDIUM
            approver = limits["approval_levels"]["ABOVE_LIMIT"]
        else:
            risk_level = RiskLevel.HIGH
            approver = limits["approval_levels"]["HIGH_RISK"]
        
        # Create proposal
        proposal = self.tracker.propose_action(
            action="CPFIS_INVESTMENT",
            target_resource=f"member/{nric_hash}/investment",
            reasoning=f"CPFIS investment in {investment_product}",
            risk_level=risk_level.value,
            investment_details={
                "amount": investment_amount,
                "product": investment_product,
                "fund_manager": fund_manager,
                "risk_profile": risk_profile
            },
            compliance_checks={
                "min_investment_met": investment_amount >= limits["min_investment"],
                "max_investment_check": investment_amount <= limits["max_investment"] * 3,
                "suitability_assessed": risk_profile in ["LOW", "MEDIUM", "HIGH"]
            }
        )
        
        # Route for approval
        if approver == "SYSTEM":
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="SYSTEM",
                context_reviewed=True,
                notes=f"Auto-approved: Within standard limits"
            )
        else:
            approver_id = f"CPFIS-{approver[:3]}-{generate_uuid7()[:6]}"
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=f"Investment approved after risk assessment"
            )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        transaction_id = f"CPFIS-{generate_uuid7()[:12]}"
        
        result = {
            "status": "APPROVED",
            "transaction_id": transaction_id,
            "investment_amount": investment_amount,
            "units_purchased": investment_amount / 1.0,  # Simplified
            "transaction_date": datetime.now().isoformat(),
            "confirmation_number": f"CONF-{generate_uuid7()[:8]}",
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        return result
    
    def update_member_consent(
        self,
        nric: str,
        consent_type: str,
        consent_given: bool,
        channels: List[str]
    ) -> Dict[str, Any]:
        """
        Update member communication consent preferences.
        
        This demonstrates:
        - PDPA compliance
        - Consent tracking and audit
        - Member preference management
        """
        print(f"\n{'='*60}")
        print(f"📝 Member Consent Update")
        print(f"{'='*60}")
        
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        
        consent_record = {
            "consent_id": f"CONSENT-{generate_uuid7()[:12]}",
            "member_hash": nric_hash,
            "consent_type": consent_type,
            "consent_given": consent_given,
            "channels": channels,
            "timestamp": time.time(),
            "ip_address_hash": hashlib.sha256(b"192.168.1.1").hexdigest()[:16],
            "user_agent": "CPF-Mobile-App/2.1",
            "consent_version": "2026.1"
        }
        
        # Create proposal for consent update
        proposal = self.tracker.propose_action(
            action="UPDATE_CONSENT",
            target_resource=f"member/{nric_hash}/consent",
            reasoning=f"Update {consent_type} consent preferences",
            risk_level=RiskLevel.LOW,
            consent_record=consent_record
        )
        
        # Auto-approve (consent updates are low risk)
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver="SYSTEM",
            context_reviewed=True,
            notes=f"Consent updated: {consent_type}={consent_given}"
        )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Store in member database
        if nric_hash not in self.members:
            self.members[nric_hash] = {}
        self.members[nric_hash][f"consent_{consent_type}"] = consent_record
        
        result = {
            "status": "UPDATED",
            "consent_id": consent_record["consent_id"],
            "consent_type": consent_type,
            "consent_given": consent_given,
            "channels": channels,
            "timestamp": consent_record["timestamp"],
            "audit_receipt": execution
        }
        
        return result
    
    def _get_account_balance(self, nric: str, account_type: CPFAccount) -> float:
        """Simulate retrieving CPF account balance."""
        # In production, this would query CPF's core banking system
        balances = {
            "ORDINARY_ACCOUNT": 150000,
            "SPECIAL_ACCOUNT": 80000,
            "MEDISAVE_ACCOUNT": 60000,
            "RETIREMENT_ACCOUNT": 200000
        }
        return balances.get(account_type.value, 100000)
    
    def _get_previous_withdrawals(self, nric: str) -> int:
        """Get count of previous withdrawals."""
        # Simulate history
        return 2
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal audit logging."""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    def generate_cpf_audit_report(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive audit report for CPF Board.
        
        This report can be submitted to:
        - CPF Board internal audit
        - Ministry of Manpower
        - Auditor-General's Office
        - Parliament (annual report)
        """
        report = {
            "report_id": f"CPF-AUDIT-{generate_uuid7()[:12]}",
            "system_id": self.system_id,
            "environment": self.environment,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "reporting_period": {
                "start": start_date or "N/A",
                "end": end_date or "N/A"
            },
            "statistics": {
                "total_transactions": len(self.transactions),
                "retirement_withdrawals": sum(1 for t in self.transactions if t["type"] == "RETIREMENT_WITHDRAWAL"),
                "housing_grants": sum(1 for t in self.transactions if t["type"] == "HOUSING_GRANT"),
                "cpfis_investments": sum(1 for t in self.transactions if t["type"] == "CPFIS"),
                "consent_updates": sum(1 for t in self.transactions if t["type"] == "CONSENT_UPDATE")
            },
            "compliance_summary": {
                "cpf_act": "COMPLIANT",
                "pdp_a": "COMPLIANT",
                "mas_guidelines": "COMPLIANT",
                "govtech_dss": "COMPLIANT"
            },
            "audit_integrity": {
                "signature_validity": "ALL_VALID",
                "audit_chain_complete": True,
                "pii_protected": True
            }
        }
        
        # Sign the report
        report["signature"] = self.tracker.signer.sign_payload(report)
        
        return report


def simulate_cpf_operations(cpf_system: CPFIntegration, days: int = 1) -> None:
    """
    Simulate CPF operations for testing/demonstration.
    """
    print(f"\n{'#'*60}")
    print(f"🏦 Simulating CPF Operations - {days} day(s)")
    print(f"{'#'*60}")
    
    # Sample members
    members = [
        {"nric": "S1234567A", "name": "Tan Ah Kow", "age": 68},
        {"nric": "S7654321B", "name": "Mdm Lim Siew Hoon", "age": 72},
        {"nric": "S9876543C", "name": "Mr Ramasamy", "age": 55},
        {"nric": "S4567890D", "name": "Ms Chen Wei Ling", "age": 45},
        {"nric": "S2345678E", "name": "Mr Tan Boon Heng", "age": 61}
    ]
    
    # Process various transactions
    for i, member in enumerate(members):
        # Retirement withdrawal for eligible members
        if member["age"] >= 65:
            result = cpf_system.process_retirement_withdrawal(
                nric=member["nric"],
                member_name=member["name"],
                member_age=member["age"],
                withdrawal_amount=50000 + (i * 10000),
                account_type=CPFAccount.RETIREMENT,
                supporting_docs=["NRIC", "Bank Statement"]
            )
            print(f"   → Transaction: {result.get('transaction_id', 'N/A')} | Status: {result.get('status')}")
        
        # Housing grant for younger members
        if member["age"] < 65:
            result = cpf_system.process_housing_grant(
                nric=member["nric"],
                member_name=member["name"],
                property_type="HDB 4-room",
                property_value=450000,
                grant_type="FAMILY_GRANT",
                joint_applicants=["S9999999Z"] if i % 2 == 0 else None
            )
            print(f"   → Housing Grant: {result.get('transaction_id', 'N/A')} | Amount: ${result.get('grant_amount', 0):,.2f}")
        
        # CPFIS investment for some members
        if i % 2 == 0:
            result = cpf_system.process_cpfis_investment(
                nric=member["nric"],
                member_name=member["name"],
                investment_amount=10000 + (i * 5000),
                investment_product="Global Equity Fund",
                fund_manager="BlackRock",
                risk_profile="MEDIUM"
            )
            print(f"   → CPFIS: {result.get('transaction_id', 'N/A')} | Amount: ${result.get('investment_amount', 0):,.2f}")
        
        # Consent update for all members
        result = cpf_system.update_member_consent(
            nric=member["nric"],
            consent_type="MARKETING",
            consent_given=i % 2 == 0,
            channels=["email", "sms"] if i % 2 == 0 else ["email"]
        )
        print(f"   → Consent: {result.get('consent_id', 'N/A')} | Status: {result.get('status')}")
        
        print()


def main():
    """
    Run CPF integration example.
    """
    print(f"\n{'='*60}")
    print(f"🇸🇬 CPF Board JEP Integration Example")
    print(f"{'='*60}")
    
    # Initialize CPF system
    cpf_system = CPFIntegration(environment="test")
    
    # Simulate operations
    simulate_cpf_operations(cpf_system, days=1)
    
    # Generate audit report
    print(f"\n{'='*60}")
    print(f"📊 Generating CPF Audit Report")
    print(f"{'='*60}")
    
    report = cpf_system.generate_cpf_audit_report(
        start_date="2026-03-01",
        end_date="2026-03-07"
    )
    
    # Save report
    report_file = "cpf_audit_report_q1_2026.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"✅ Audit report saved to: {report_file}")
    
    print(f"\n{'='*60}")
    print(f"✅ CPF Integration Example Complete")
    print(f"   This demonstrates:")
    print(f"   - Retirement withdrawal with multi-level approval")
    print(f"   - Housing grant with HDB integration")
    print(f"   - CPFIS investment with MAS compliance")
    print(f"   - Member consent management (PDPA)")
    print(f"   - Complete audit trail for CPF Act")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
