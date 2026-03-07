"""
JEP Accountability Implementation for Singapore's Agentic AI Framework (2026)
=====================================================================

This module provides a complete implementation of Pillar 2 
"Make People Meaningfully Accountable" from Singapore's Model AI 
Governance Framework for Agentic AI.

Key Features:
- Human approval checkpoints with cryptographic proof
- Complete context for meaningful oversight
- Non-repudiable audit trails
- Clear accountability chains

Framework Requirements Covered:
- 2.1: Determine which decisions require human oversight
- 2.2: Ensure oversight is "meaningful" (supervisors understand context)
- 2.3: Document oversight in auditable format
- 2.4: Establish clear accountability chains

Usage:
    from accountability import AgenticAIAccountability
    
    tracker = AgenticAIAccountability(
        agent_id="customer-support-v2",
        organization="dbs-bank"
    )
    
    # Propose an action requiring human approval
    proposal = tracker.propose_action(
        action="EXECUTE_PAYMENT",
        amount=50000,
        currency="SGD",
        recipient="C001234",
        reasoning="Customer requested urgent transfer"
    )
    
    # Human approves (or denies)
    receipt = tracker.approve_action(
        proposal_id=proposal.id,
        human_approver="supervisor-456",
        notes="Verified customer identity via phone"
    )
"""

import json
import time
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum

# Import JEP core (would be installed via pip)
from jep.core import JEPAsymmetricSigner, generate_uuid7


class RiskLevel(Enum):
    """Risk levels defined in Agentic AI Framework"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionStatus(Enum):
    """Status of an action throughout its lifecycle"""
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    EXECUTED = "EXECUTED"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"


@dataclass
class ActionProposal:
    """
    Represents a proposed action that requires human oversight.
    
    Framework Requirement 2.1: Organizations should determine which
    decisions require human oversight. This class represents those
    decisions that have been flagged for human review.
    """
    id: str
    action: str
    target_resource: str
    parameters: Dict[str, Any]
    reasoning: str
    risk_level: RiskLevel
    proposed_by: str
    proposed_at: float
    status: ActionStatus = ActionStatus.PROPOSED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "action": self.action,
            "target_resource": self.target_resource,
            "parameters": self.parameters,
            "reasoning": self.reasoning,
            "risk_level": self.risk_level.value,
            "proposed_by": self.proposed_by,
            "proposed_at": self.proposed_at,
            "status": self.status.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ActionProposal':
        """Create from dictionary"""
        return cls(
            id=data["id"],
            action=data["action"],
            target_resource=data["target_resource"],
            parameters=data.get("parameters", {}),
            reasoning=data["reasoning"],
            risk_level=RiskLevel(data["risk_level"]),
            proposed_by=data["proposed_by"],
            proposed_at=data["proposed_at"],
            status=ActionStatus(data.get("status", "PROPOSED"))
        )


@dataclass
class HumanApprovalRecord:
    """
    Records a human approval decision with cryptographic proof.
    
    Framework Requirement 2.3: Oversight should be documented and auditable.
    This class creates the immutable record of human decisions.
    """
    proposal_id: str
    human_approver: str
    decision: ActionStatus  # APPROVED or DENIED
    approval_time: float
    context_reviewed: bool  # Requirement 2.2: Meaningful oversight
    notes: Optional[str] = None
    receipt_id: str = field(default_factory=generate_uuid7)
    signature: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for signing and storage"""
        return {
            "receipt_id": self.receipt_id,
            "proposal_id": self.proposal_id,
            "human_approver": self.human_approver,
            "decision": self.decision.value,
            "approval_time": self.approval_time,
            "context_reviewed": self.context_reviewed,
            "notes": self.notes,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.approval_time))
        }
    
    def sign(self, signer: JEPAsymmetricSigner) -> None:
        """Sign the record to ensure non-repudiation"""
        data = self.to_dict()
        self.signature = signer.sign_payload(data)
    
    def verify(self, signer: JEPAsymmetricSigner) -> bool:
        """Verify the signature"""
        if not self.signature:
            return False
        data = self.to_dict()
        return signer.verify_payload(data, self.signature)


class AgenticAIAccountability:
    """
    Complete implementation of Pillar 2: Make People Meaningfully Accountable.
    
    This class provides all the functionality needed to implement
    human accountability requirements for agentic AI systems.
    """
    
    def __init__(
        self,
        agent_id: str,
        organization: str,
        private_key_hex: Optional[str] = None
    ):
        """
        Initialize the accountability tracker.
        
        Args:
            agent_id: Unique identifier for this AI agent
            organization: Organization responsible for this agent
            private_key_hex: Optional private key for signing
        """
        self.agent_id = agent_id
        self.organization = organization
        self.signer = JEPAsymmetricSigner(private_key_hex)
        self.proposals: Dict[str, ActionProposal] = {}
        self.approval_records: List[HumanApprovalRecord] = []
        self.audit_log: List[Dict[str, Any]] = []
    
    def propose_action(
        self,
        action: str,
        target_resource: str,
        reasoning: str,
        risk_level: str,
        **parameters
    ) -> ActionProposal:
        """
        Propose an action that requires human oversight.
        
        Framework Requirement 2.1: Organizations should determine which
        decisions require human oversight. This method creates a proposal
        for those decisions.
        
        Framework Requirement 2.2: Meaningful oversight - the proposal
        includes full context (reasoning, parameters, risk level) so the
        human can make an informed decision.
        
        Args:
            action: The action to be performed
            target_resource: The resource the action will affect
            reasoning: Explanation of why this action is needed
            risk_level: Risk level (LOW/MEDIUM/HIGH/CRITICAL)
            **parameters: Additional parameters specific to the action
        
        Returns:
            ActionProposal object with unique ID
        """
        # Create proposal with complete context
        proposal = ActionProposal(
            id=f"prop_{generate_uuid7()}",
            action=action,
            target_resource=target_resource,
            parameters=parameters,
            reasoning=reasoning,
            risk_level=RiskLevel(risk_level.upper()),
            proposed_by=self.agent_id,
            proposed_at=time.time()
        )
        
        # Store proposal
        self.proposals[proposal.id] = proposal
        
        # Log to audit trail
        self._log_audit_event("PROPOSED", proposal.to_dict())
        
        return proposal
    
    def approve_action(
        self,
        proposal_id: str,
        human_approver: str,
        notes: Optional[str] = None,
        context_reviewed: bool = True
    ) -> HumanApprovalRecord:
        """
        Approve a proposed action.
        
        Framework Requirement 2.3: Document oversight - this creates
        a cryptographically signed record of the approval.
        
        Framework Requirement 2.4: Accountability chains - this links
        the human approver to the AI's proposed action.
        
        Args:
            proposal_id: ID of the proposal to approve
            human_approver: ID of the human making the decision
            notes: Optional notes from the human reviewer
            context_reviewed: Whether the human confirmed they reviewed context
        
        Returns:
            HumanApprovalRecord with cryptographic signature
        
        Raises:
            ValueError: If proposal not found or already processed
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ActionStatus.PROPOSED:
            raise ValueError(f"Proposal already {proposal.status.value}")
        
        # Create approval record
        approval = HumanApprovalRecord(
            proposal_id=proposal_id,
            human_approver=human_approver,
            decision=ActionStatus.APPROVED,
            approval_time=time.time(),
            context_reviewed=context_reviewed,
            notes=notes
        )
        
        # Sign the record (non-repudiation)
        approval.sign(self.signer)
        
        # Update proposal status
        proposal.status = ActionStatus.APPROVED
        
        # Store record
        self.approval_records.append(approval)
        
        # Log to audit trail
        self._log_audit_event("APPROVED", approval.to_dict())
        
        return approval
    
    def deny_action(
        self,
        proposal_id: str,
        human_approver: str,
        reason: str,
        context_reviewed: bool = True
    ) -> HumanApprovalRecord:
        """
        Deny a proposed action.
        
        Framework Requirement 2.3: Document oversight - denials are
        also recorded with cryptographic proof.
        
        Args:
            proposal_id: ID of the proposal to deny
            human_approver: ID of the human making the decision
            reason: Reason for denial
            context_reviewed: Whether the human confirmed they reviewed context
        
        Returns:
            HumanApprovalRecord with cryptographic signature
        
        Raises:
            ValueError: If proposal not found or already processed
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ActionStatus.PROPOSED:
            raise ValueError(f"Proposal already {proposal.status.value}")
        
        # Create denial record
        denial = HumanApprovalRecord(
            proposal_id=proposal_id,
            human_approver=human_approver,
            decision=ActionStatus.DENIED,
            approval_time=time.time(),
            context_reviewed=context_reviewed,
            notes=f"DENIED: {reason}"
        )
        
        # Sign the record
        denial.sign(self.signer)
        
        # Update proposal status
        proposal.status = ActionStatus.DENIED
        
        # Store record
        self.approval_records.append(denial)
        
        # Log to audit trail
        self._log_audit_event("DENIED", denial.to_dict())
        
        return denial
    
    def execute_approved_action(self, proposal_id: str) -> Dict[str, Any]:
        """
        Execute a previously approved action.
        
        This completes the accountability chain: proposal → approval → execution.
        
        Args:
            proposal_id: ID of the approved proposal
        
        Returns:
            Execution receipt
        
        Raises:
            ValueError: If proposal not found or not approved
        """
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal = self.proposals[proposal_id]
        
        if proposal.status != ActionStatus.APPROVED:
            raise ValueError(f"Proposal must be APPROVED, not {proposal.status.value}")
        
        # Find the approval record
        approval = next(
            (a for a in self.approval_records if a.proposal_id == proposal_id),
            None
        )
        
        if not approval:
            raise ValueError(f"No approval record found for {proposal_id}")
        
        # Create execution receipt
        execution_receipt = {
            "receipt_id": f"exec_{generate_uuid7()}",
            "proposal_id": proposal_id,
            "approval_id": approval.receipt_id,
            "action": proposal.action,
            "target_resource": proposal.target_resource,
            "parameters": proposal.parameters,
            "executed_by": proposal.proposed_by,
            "executed_at": time.time(),
            "approval_chain": {
                "proposed_at": proposal.proposed_at,
                "approved_at": approval.approval_time,
                "approved_by": approval.human_approver,
                "approval_signature": approval.signature
            }
        }
        
        # Sign the execution receipt
        execution_receipt["signature"] = self.signer.sign_payload(execution_receipt)
        
        # Update proposal status
        proposal.status = ActionStatus.EXECUTED
        
        # Log to audit trail
        self._log_audit_event("EXECUTED", execution_receipt)
        
        return execution_receipt
    
    def get_accountability_chain(self, proposal_id: str) -> Dict[str, Any]:
        """
        Get the complete accountability chain for a proposal.
        
        Framework Requirement 2.4: Clear accountability chains.
        This method reconstructs the entire chain of responsibility.
        
        Args:
            proposal_id: ID of the proposal
        
        Returns:
            Complete accountability chain with verification status
        """
        if proposal_id not in self.proposals:
            return {"error": "Proposal not found"}
        
        proposal = self.proposals[proposal_id]
        
        # Find approval record
        approval = next(
            (a for a in self.approval_records if a.proposal_id == proposal_id),
            None
        )
        
        chain = {
            "proposal_id": proposal_id,
            "agent": {
                "id": proposal.proposed_by,
                "action": proposal.action,
                "time": proposal.proposed_at,
                "risk_level": proposal.risk_level.value
            },
            "human_oversight": None,
            "execution": None,
            "verification": {}
        }
        
        # Add human oversight if exists
        if approval:
            # Verify the approval signature
            is_signature_valid = approval.verify(self.signer)
            
            chain["human_oversight"] = {
                "approver": approval.human_approver,
                "decision": approval.decision.value,
                "time": approval.approval_time,
                "context_reviewed": approval.context_reviewed,
                "notes": approval.notes,
                "receipt_id": approval.receipt_id,
                "signature_valid": is_signature_valid
            }
            
            chain["verification"]["human_oversight"] = "VALID" if is_signature_valid else "INVALID"
        
        # Add execution if exists
        if proposal.status == ActionStatus.EXECUTED:
            chain["execution"] = {
                "status": "EXECUTED",
                "time": proposal.executed_at if hasattr(proposal, 'executed_at') else None
            }
        
        # Overall verification
        all_valid = all(
            v == "VALID" for v in chain["verification"].values()
        ) if chain["verification"] else False
        
        chain["verification"]["overall"] = "VALID" if all_valid else "PENDING"
        
        return chain
    
    def generate_audit_report(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete audit report for regulatory submission.
        
        Args:
            start_time: Optional start time filter
            end_time: Optional end time filter
        
        Returns:
            Complete audit report with all accountability records
        """
        # Filter proposals by time
        proposals = self.proposals.values()
        if start_time:
            proposals = [p for p in proposals if p.proposed_at >= start_time]
        if end_time:
            proposals = [p for p in proposals if p.proposed_at <= end_time]
        
        # Filter approvals by time
        approvals = self.approval_records
        if start_time:
            approvals = [a for a in approvals if a.approval_time >= start_time]
        if end_time:
            approvals = [a for a in approvals if a.approval_time <= end_time]
        
        # Compile report
        report = {
            "report_id": f"audit_{generate_uuid7()}",
            "generated_at": time.time(),
            "organization": self.organization,
            "agent_id": self.agent_id,
            "time_range": {
                "start": start_time,
                "end": end_time
            },
            "statistics": {
                "total_proposals": len(proposals),
                "approved": len([p for p in proposals if p.status == ActionStatus.APPROVED]),
                "denied": len([p for p in proposals if p.status == ActionStatus.DENIED]),
                "executed": len([p for p in proposals if p.status == ActionStatus.EXECUTED]),
                "pending": len([p for p in proposals if p.status == ActionStatus.PROPOSED])
            },
            "accountability_summary": {
                "total_human_decisions": len(approvals),
                "avg_approval_time": self._calculate_avg_approval_time(proposals, approvals),
                "signature_validity": self._check_all_signatures(approvals)
            },
            "proposals": [p.to_dict() for p in proposals],
            "approvals": [a.to_dict() for a in approvals]
        }
        
        # Sign the report
        report["signature"] = self.signer.sign_payload(report)
        
        return report
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal method to log audit events"""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    def _calculate_avg_approval_time(
        self,
        proposals: List[ActionProposal],
        approvals: List[HumanApprovalRecord]
    ) -> Optional[float]:
        """Calculate average time between proposal and approval"""
        if not approvals:
            return None
        
        times = []
        for approval in approvals:
            proposal = self.proposals.get(approval.proposal_id)
            if proposal:
                times.append(approval.approval_time - proposal.proposed_at)
        
        return sum(times) / len(times) if times else None
    
    def _check_all_signatures(self, approvals: List[HumanApprovalRecord]) -> str:
        """Check validity of all signatures"""
        if not approvals:
            return "NO_APPROVALS"
        
        all_valid = all(a.verify(self.signer) for a in approvals)
        return "ALL_VALID" if all_valid else "SOME_INVALID"


# Example usage
if __name__ == "__main__":
    # Initialize tracker for a bank's customer service agent
    tracker = AgenticAIAccountability(
        agent_id="customer-support-v2",
        organization="dbs-bank"
    )
    
    print("="*60)
    print("JEP Accountability Implementation Demo")
    print("Singapore Agentic AI Framework - Pillar 2")
    print("="*60)
    
    # Step 1: Agent proposes an action requiring human approval
    print("\n1. Agent proposes high-risk action...")
    proposal = tracker.propose_action(
        action="EXECUTE_PAYMENT",
        target_resource="customer_account/C001234",
        reasoning="Customer requested urgent international transfer",
        risk_level="HIGH",
        amount=50000,
        currency="SGD",
        recipient_name="John Tan"
    )
    print(f"   Proposal ID: {proposal.id}")
    print(f"   Action: {proposal.action}")
    print(f"   Risk Level: {proposal.risk_level.value}")
    
    # Step 2: Human supervisor reviews and approves
    print("\n2. Human supervisor reviews with full context...")
    print(f"   Context shown to human:")
    print(f"   - Action: {proposal.action}")
    print(f"   - Amount: {proposal.parameters.get('amount')} {proposal.parameters.get('currency')}")
    print(f"   - Recipient: {proposal.parameters.get('recipient_name')}")
    print(f"   - Reasoning: {proposal.reasoning}")
    
    approval = tracker.approve_action(
        proposal_id=proposal.id,
        human_approver="supervisor-456",
        notes="Verified customer identity via phone, transfer approved"
    )
    print(f"\n   Approval Record:")
    print(f"   - Approver: {approval.human_approver}")
    print(f"   - Decision: {approval.decision.value}")
    print(f"   - Receipt ID: {approval.receipt_id}")
    print(f"   - Signature: {approval.signature[:50]}...")
    
    # Step 3: Execute the approved action
    print("\n3. Executing approved action...")
    execution = tracker.execute_approved_action(proposal.id)
    print(f"   Execution Receipt: {execution['receipt_id']}")
    
    # Step 4: Get complete accountability chain
    print("\n4. Complete accountability chain:")
    chain = tracker.get_accountability_chain(proposal.id)
    print(f"   Agent: {chain['agent']['id']}")
    print(f"   Human: {chain['human_oversight']['approver']}")
    print(f"   Signature Valid: {chain['human_oversight']['signature_valid']}")
    print(f"   Overall: {chain['verification']['overall']}")
    
    # Step 5: Generate audit report
    print("\n5. Generating audit report for MAS...")
    report = tracker.generate_audit_report()
    print(f"   Report ID: {report['report_id']}")
    print(f"   Total Proposals: {report['statistics']['total_proposals']}")
    print(f"   Signature Status: {report['accountability_summary']['signature_validity']}")
    
    print("\n" + "="*60)
    print("✅ Implementation successfully demonstrates:")
    print("   - Human oversight points (Req 2.1)")
    print("   - Meaningful context review (Req 2.2)")
    print("   - Documented, auditable decisions (Req 2.3)")
    print("   - Clear accountability chains (Req 2.4)")
    print("="*60)
