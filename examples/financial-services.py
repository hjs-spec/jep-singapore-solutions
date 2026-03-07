#!/usr/bin/env python3
"""
JEP Financial Services Example - Singapore Banking Sector
===========================================================

This example demonstrates how a Singapore bank (e.g., DBS, OCBC, UOB)
can implement JEP to meet both MAS regulatory requirements and
IMDA's Agentic AI Framework.

Regulatory Compliance:
- MAS FEAT Principles (Fairness, Ethics, Accountability, Transparency)
- MAS Technology Risk Management Guidelines
- IMDA Agentic AI Framework (2026)
- PDPA (Personal Data Protection Act)

Scenario:
A customer service AI agent handling fund transfer requests with
human oversight for high-risk transactions.
"""

import json
import time
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

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


class SingaporeBankingAI:
    """
    Complete example of a Singapore bank's AI-powered customer service agent
    with full accountability and MAS compliance.
    """
    
    def __init__(self, bank_name: str, agent_id: str):
        """
        Initialize the banking AI agent.
        
        Args:
            bank_name: Name of the bank (e.g., "DBS Bank")
            agent_id: Unique identifier for this AI agent
        """
        self.bank_name = bank_name
        self.agent_id = agent_id
        
        # Initialize JEP accountability tracker
        self.tracker = AgenticAIAccountability(
            agent_id=agent_id,
            organization=bank_name
        )
        
        # Banking-specific configuration
        self.transaction_limits = {
            "LOW": 1000,      # SGD, no human approval needed
            "MEDIUM": 10000,   # SGD, manager approval
            "HIGH": 50000,     # SGD, senior manager approval
            "CRITICAL": 50001  # SGD, compliance officer + manager approval
        }
        
        # Audit log for internal use
        self.audit_log = []
        
        print(f"✅ {bank_name} AI Agent initialized: {agent_id}")
        print(f"   Transaction limits: {self.transaction_limits}")
    
    def process_transfer_request(
        self,
        customer_id: str,
        amount: float,
        currency: str,
        recipient_name: str,
        recipient_account: str,
        recipient_bank: str,
        customer_notes: str = ""
    ) -> Dict[str, Any]:
        """
        Process a customer fund transfer request with appropriate
        human oversight based on risk level.
        
        This demonstrates:
        - Risk-based decision making (MAS TRM Guidelines)
        - Human oversight for high-risk transactions (Agentic Framework)
        - Complete audit trail (MAS FEAT Accountability)
        """
        
        # Step 1: Determine risk level based on amount
        risk_level = self._determine_risk_level(amount)
        
        print(f"\n{'='*60}")
        print(f"💰 Transfer Request Received")
        print(f"{'='*60}")
        print(f"Customer: {customer_id}")
        print(f"Amount: {amount} {currency}")
        print(f"Recipient: {recipient_name} - {recipient_account} ({recipient_bank})")
        print(f"Risk Level: {risk_level}")
        print(f"Notes: {customer_notes or 'None'}")
        
        # Step 2: AI agent proposes the action
        proposal = self.tracker.propose_action(
            action="EXECUTE_FUND_TRANSFER",
            target_resource=f"customer_account/{customer_id}",
            reasoning=f"Customer {customer_id} requested transfer of {amount} {currency} to {recipient_name}",
            risk_level=risk_level,
            # Additional context for meaningful oversight
            amount=amount,
            currency=currency,
            recipient_name=recipient_name,
            recipient_account=recipient_account,
            recipient_bank=recipient_bank,
            customer_notes=customer_notes,
            customer_risk_score=self._get_customer_risk_score(customer_id),
            transaction_purpose=customer_notes or "Transfer",
            timestamp=time.time()
        )
        
        print(f"\n📝 AI Proposal Created: {proposal.id}")
        
        # Step 3: For low-risk transactions, auto-approve with rules
        if risk_level == RiskLevel.LOW and amount <= self.transaction_limits["LOW"]:
            return self._auto_approve_transaction(proposal)
        
        # Step 4: For medium/high risk, route to appropriate human approver
        else:
            return self._route_for_human_approval(proposal, risk_level)
    
    def _determine_risk_level(self, amount: float) -> RiskLevel:
        """
        Determine risk level based on transaction amount.
        
        MAS guidelines require enhanced due diligence for
        high-value transactions.
        """
        if amount <= self.transaction_limits["LOW"]:
            return RiskLevel.LOW
        elif amount <= self.transaction_limits["MEDIUM"]:
            return RiskLevel.MEDIUM
        elif amount <= self.transaction_limits["HIGH"]:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _get_customer_risk_score(self, customer_id: str) -> str:
        """
        Simulate retrieving customer risk score from bank's AML system.
        
        In production, this would connect to the bank's risk management system.
        """
        # Simplified for demo - in reality, would query AML/KYC system
        risk_scores = {
            "CUST001": "LOW",
            "CUST002": "MEDIUM",
            "CUST003": "HIGH",
            "CUST004": "LOW"
        }
        return risk_scores.get(customer_id, "MEDIUM")
    
    def _auto_approve_transaction(self, proposal: ActionProposal) -> Dict[str, Any]:
        """
        Auto-approve low-risk transactions based on predefined rules.
        
        MAS allows automated processing for low-risk transactions
        with proper audit trails.
        """
        print(f"\n🤖 Auto-approving low-risk transaction (rule-based)")
        
        # Record system approval (compliance with MAS audit requirements)
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver="SYSTEM_RULE_ENGINE",
            context_reviewed=True,
            notes=f"Auto-approved: Amount within LOW risk threshold ({self.transaction_limits['LOW']} SGD)"
        )
        
        # Execute the transaction
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Return complete result
        result = {
            "status": "APPROVED",
            "approval_type": "AUTO",
            "transaction_id": execution.get("receipt_id"),
            "amount": proposal.parameters.get("amount"),
            "currency": proposal.parameters.get("currency"),
            "recipient": proposal.parameters.get("recipient_name"),
            "timestamp": time.time(),
            "audit_receipt": execution
        }
        
        self._log_audit_event("TRANSACTION_COMPLETED", result)
        return result
    
    def _route_for_human_approval(
        self,
        proposal: ActionProposal,
        risk_level: RiskLevel
    ) -> Dict[str, Any]:
        """
        Route transaction to appropriate human approver based on risk level.
        
        MAS requires human oversight for medium/high risk transactions.
        """
        # Determine approver level based on risk
        if risk_level == RiskLevel.MEDIUM:
            approver = "branch_manager"
            approver_id = f"BM_{proposal.parameters.get('recipient_bank', 'DBS')}"
        elif risk_level == RiskLevel.HIGH:
            approver = "senior_manager"
            approver_id = f"SM_{proposal.parameters.get('recipient_bank', 'DBS')}"
        else:  # CRITICAL
            approver = "compliance_officer+senior_manager"
            approver_id = "COMPLIANCE_TEAM"
        
        print(f"\n👤 Routing for {approver} approval")
        print(f"   Approver: {approver_id}")
        
        # In a real system, this would send a notification to the approver
        # For this demo, we'll simulate the approval
        
        # Simulate human reviewing the context (meeting "meaningful oversight" requirement)
        print(f"\n   Context shown to approver:")
        print(f"   - Customer: {proposal.parameters.get('customer_id', 'Unknown')}")
        print(f"   - Amount: {proposal.parameters.get('amount')} {proposal.parameters.get('currency')}")
        print(f"   - Recipient: {proposal.parameters.get('recipient_name')}")
        print(f"   - Recipient Bank: {proposal.parameters.get('recipient_bank')}")
        print(f"   - Purpose: {proposal.parameters.get('transaction_purpose')}")
        print(f"   - Customer Risk Score: {proposal.parameters.get('customer_risk_score')}")
        print(f"   - AI Reasoning: {proposal.reasoning}")
        
        # Simulate human decision (in real system, would wait for input)
        # For demo, we'll simulate approval
        approval_decision = True
        approval_notes = "Verified customer identity via phone, transaction approved"
        
        if approval_decision:
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=approval_notes
            )
            
            print(f"\n✅ Human Approved - Receipt: {approval.receipt_id}")
            
            # Execute the transaction
            execution = self.tracker.execute_approved_action(proposal.id)
            
            result = {
                "status": "APPROVED",
                "approval_type": "HUMAN",
                "approver": approver_id,
                "transaction_id": execution.get("receipt_id"),
                "amount": proposal.parameters.get("amount"),
                "currency": proposal.parameters.get("currency"),
                "recipient": proposal.parameters.get("recipient_name"),
                "timestamp": time.time(),
                "audit_receipt": execution,
                "human_approval_receipt": approval.to_dict()
            }
        else:
            # Transaction denied by human
            denial = self.tracker.deny_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                reason="Transaction flagged for additional verification"
            )
            
            print(f"\n❌ Human Denied - Receipt: {denial.receipt_id}")
            
            result = {
                "status": "DENIED",
                "approval_type": "HUMAN",
                "approver": approver_id,
                "reason": denial.notes,
                "amount": proposal.parameters.get("amount"),
                "currency": proposal.parameters.get("currency"),
                "timestamp": time.time(),
                "human_approval_receipt": denial.to_dict()
            }
        
        self._log_audit_event("TRANSACTION_PROCESSED", result)
        return result
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal audit logging"""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    def generate_mas_report(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a report specifically formatted for MAS (Monetary Authority of Singapore)
        
        This report addresses:
        - MAS FEAT Principles (Fairness, Ethics, Accountability, Transparency)
        - MAS Technology Risk Management Guidelines
        - MAS Notice 658 (Cyber Hygiene)
        """
        
        # Convert string dates to timestamps if provided
        start_ts = None
        end_ts = None
        if start_date:
            start_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
        if end_date:
            end_ts = datetime.strptime(end_date, "%Y-%m-%d").timestamp() + 86400  # End of day
        
        # Get base audit report from tracker
        base_report = self.tracker.generate_audit_report(start_ts, end_ts)
        
        # Enhance with MAS-specific metrics
        mas_report = {
            "report_id": f"MAS_{generate_uuid7()}",
            "institution": self.bank_name,
            "agent_id": self.agent_id,
            "reporting_period": {
                "start": start_date or "N/A",
                "end": end_date or "N/A"
            },
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            
            # MAS FEAT Principles
            "feat_principles": {
                "fairness": self._assess_fairness(base_report),
                "ethics": self._assess_ethics(base_report),
                "accountability": self._assess_accountability(base_report),
                "transparency": self._assess_transparency(base_report)
            },
            
            # MAS Technology Risk Management
            "technology_risk": {
                "human_oversight_rate": self._calculate_human_oversight_rate(base_report),
                "audit_completeness": self._calculate_audit_completeness(base_report),
                "signature_validity": base_report.get("accountability_summary", {}).get("signature_validity", "UNKNOWN")
            },
            
            # Transaction Statistics
            "transaction_statistics": {
                "total": base_report.get("statistics", {}).get("total_proposals", 0),
                "approved": base_report.get("statistics", {}).get("approved", 0),
                "denied": base_report.get("statistics", {}).get("denied", 0),
                "by_risk_level": self._breakdown_by_risk(base_report)
            },
            
            # For auditors
            "audit_trail_reference": {
                "proposal_count": len(base_report.get("proposals", [])),
                "approval_count": len(base_report.get("approvals", [])),
                "earliest_transaction": self._get_earliest_transaction(base_report),
                "latest_transaction": self._get_latest_transaction(base_report)
            },
            
            # Cryptographic proof
            "report_signature": base_report.get("signature"),
            "verification_method": "Ed25519 (RFC 8032)"
        }
        
        return mas_report
    
    def _assess_fairness(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Assess MAS FEAT Fairness principle"""
        # In production, this would analyze decisions for bias
        # For demo, return a simplified assessment
        return {
            "status": "COMPLIANT",
            "notes": "All transactions processed with consistent risk-based rules"
        }
    
    def _assess_ethics(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Assess MAS FEAT Ethics principle"""
        return {
            "status": "COMPLIANT",
            "notes": "Human oversight maintained for all high-risk decisions"
        }
    
    def _assess_accountability(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Assess MAS FEAT Accountability principle"""
        # Check if all decisions have clear accountability chains
        all_approved = report.get("statistics", {}).get("approved", 0)
        proposals = report.get("proposals", [])
        
        if all_approved == 0:
            return {"status": "NO_DATA", "notes": "No approved transactions in period"}
        
        # In production, would verify each proposal has associated approval
        return {
            "status": "COMPLIANT",
            "notes": f"{all_approved} transactions have complete accountability chains"
        }
    
    def _assess_transparency(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Assess MAS FEAT Transparency principle"""
        return {
            "status": "COMPLIANT",
            "notes": "All decisions recorded with complete context in JSON-LD format"
        }
    
    def _calculate_human_oversight_rate(self, report: Dict[str, Any]) -> str:
        """Calculate percentage of transactions with human oversight"""
        total = report.get("statistics", {}).get("total_proposals", 0)
        if total == 0:
            return "0%"
        
        # This would be calculated from actual data
        # For demo, return a placeholder
        return "100% for HIGH/CRITICAL risk transactions"
    
    def _calculate_audit_completeness(self, report: Dict[str, Any]) -> str:
        """Check if audit trail is complete"""
        return "100%"
    
    def _breakdown_by_risk(self, report: Dict[str, Any]) -> Dict[str, int]:
        """Break down transactions by risk level"""
        # This would be calculated from actual proposals
        # For demo, return placeholder
        return {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0
        }
    
    def _get_earliest_transaction(self, report: Dict[str, Any]) -> Optional[str]:
        """Get timestamp of earliest transaction in report"""
        if report.get("proposals"):
            earliest = min((p.get("proposed_at", 0) for p in report["proposals"]), default=None)
            if earliest:
                return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(earliest))
        return None
    
    def _get_latest_transaction(self, report: Dict[str, Any]) -> Optional[str]:
        """Get timestamp of latest transaction in report"""
        if report.get("proposals"):
            latest = max((p.get("proposed_at", 0) for p in report["proposals"]), default=None)
            if latest:
                return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(latest))
        return None
    
    def submit_to_regulator(self, report: Dict[str, Any], output_file: str) -> None:
        """
        Simulate submitting the report to MAS.
        
        In production, this would send via MAS' prescribed channels.
        """
        print(f"\n{'='*60}")
        print(f"📤 Submitting Report to MAS")
        print(f"{'='*60}")
        print(f"Report ID: {report.get('report_id')}")
        print(f"Institution: {report.get('institution')}")
        print(f"Period: {report.get('reporting_period', {}).get('start')} to {report.get('reporting_period', {}).get('end')}")
        print(f"FEAT Status: {report.get('feat_principles', {}).get('accountability', {}).get('status')}")
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n✅ Report saved to: {output_file}")
        print(f"   This file can be submitted to MAS as evidence of compliance")


def simulate_banking_day(bank_ai: SingaporeBankingAI) -> None:
    """
    Simulate a day of banking operations with various transaction types.
    """
    
    # Sample customers
    customers = [
        {"id": "CUST001", "name": "John Tan", "risk": "LOW"},
        {"id": "CUST002", "name": "Mary Lim", "risk": "MEDIUM"},
        {"id": "CUST003", "name": "Ahmed Khan", "risk": "HIGH"},
        {"id": "CUST004", "name": "Sarah Chen", "risk": "LOW"}
    ]
    
    # Sample transactions
    transactions = [
        # Low-risk (auto-approve)
        {"amount": 500, "currency": "SGD", "recipient": "GrabPay", "bank": "Grab"},
        {"amount": 800, "currency": "SGD", "recipient": "Singtel", "bank": "Singtel"},
        
        # Medium-risk (branch manager approval)
        {"amount": 5000, "currency": "SGD", "recipient": "John Property", "bank": "OCBC"},
        {"amount": 7500, "currency": "SGD", "recipient": "Toyota Singapore", "bank": "UOB"},
        
        # High-risk (senior manager approval)
        {"amount": 25000, "currency": "SGD", "recipient": "BMW Asia", "bank": "DBS"},
        {"amount": 40000, "currency": "USD", "recipient": "Apple Inc", "bank": "Citibank"},
        
        # Critical (compliance team approval)
        {"amount": 100000, "currency": "SGD", "recipient": "Overseas Property", "bank": "HSBC"}
    ]
    
    print(f"\n{'#'*60}")
    print(f"🏦 Simulating Banking Day at {bank_ai.bank_name}")
    print(f"{'#'*60}")
    
    for i, customer in enumerate(customers):
        for j, tx in enumerate(transactions):
            # Use modulo to distribute transactions across customers
            if (i + j) % len(customers) == i:
                result = bank_ai.process_transfer_request(
                    customer_id=customer["id"],
                    amount=tx["amount"],
                    currency=tx["currency"],
                    recipient_name=tx["recipient"],
                    recipient_account=f"ACC{hash(tx['recipient']) % 1000000:06d}",
                    recipient_bank=tx["bank"],
                    customer_notes=f"Payment for {tx['recipient']} - {customer['name']}"
                )
                
                # Small delay to simulate real time
                time.sleep(0.5)


def main():
    """
    Run the complete banking AI example.
    """
    print(f"\n{'='*60}")
    print(f"🇸🇬 JEP Financial Services Example - Singapore Banking")
    print(f"{'='*60}")
    
    # Initialize the bank's AI agent
    dbs_ai = SingaporeBankingAI(
        bank_name="DBS Bank",
        agent_id="dbs-customer-service-v2"
    )
    
    # Simulate a day of operations
    simulate_banking_day(dbs_ai)
    
    # Generate MAS compliance report
    print(f"\n{'='*60}")
    print(f"📊 Generating MAS Compliance Report")
    print(f"{'='*60}")
    
    # Report for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    mas_report = dbs_ai.generate_mas_report(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d")
    )
    
    # Submit to regulator
    dbs_ai.submit_to_regulator(mas_report, "mas_compliance_report_q1_2026.json")
    
    # Show accountability chain for a specific transaction
    print(f"\n{'='*60}")
    print(f"🔍 Example Accountability Chain")
    print(f"{'='*60}")
    
    # Get the first proposal from the tracker
    proposals = list(dbs_ai.tracker.proposals.values())
    if proposals:
        chain = dbs_ai.tracker.get_accountability_chain(proposals[0].id)
        print(f"\nTransaction: {proposals[0].action}")
        print(f"Risk Level: {proposals[0].risk_level.value}")
        print(f"Agent: {chain['agent']['id']}")
        if chain.get('human_oversight'):
            print(f"Human Approver: {chain['human_oversight']['approver']}")
            print(f"Signature Valid: {chain['human_oversight']['signature_valid']}")
        print(f"Overall Verification: {chain['verification']['overall']}")
    
    print(f"\n{'='*60}")
    print(f"✅ Example Complete")
    print(f"   This demonstrates:")
    print(f"   - MAS FEAT Accountability Principle")
    print(f"   - Agentic AI Framework Human Oversight")
    print(f"   - Complete audit trail for regulator submission")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
