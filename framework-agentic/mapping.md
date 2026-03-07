# JEP Alignment with Singapore's Model AI Governance Framework for Agentic AI (2026)

**Detailed Article-by-Article Mapping**

## 📋 Overview

This document provides a comprehensive mapping between the **Judgment Event Protocol (JEP)** and the **Model AI Governance Framework for Agentic AI** launched by IMDA in January 2026.

The framework consists of four pillars. For each pillar, we map JEP's technical features to the specific requirements and provide verifiable evidence.

---

## 🏛️ Pillar 1: Assess and Bound Risks Upfront

### Framework Requirements

| Requirement ID | Description |
|----------------|-------------|
| 1.1 | Organizations should assess the use case to determine if an agentic AI is appropriate |
| 1.2 | The level of autonomy granted should be commensurate with risk |
| 1.3 | Scope boundaries should be clearly defined and enforced |
| 1.4 | Risk assessment should be documented and periodically reviewed |

### JEP Implementation

| Requirement | JEP Feature | Implementation | Verification |
|-------------|-------------|----------------|--------------|
| 1.1 (Use case assessment) | judge() primitive records the assessment outcome | proposal = tracker.judge_action(action="EXECUTE_PAYMENT", use_case="CROSS_BORDER_TRANSFER", assessment="APPROPRIATE", risk_level="HIGH") | Check use_case and assessment fields in receipt |
| 1.2 (Autonomy vs risk) | Risk level field in every receipt | receipt.compliance_binding.risk_level | Verify risk level is set (LOW/MEDIUM/HIGH/CRITICAL) |
| 1.3 (Scope boundaries) | resource field defines the target scope | receipt = tracker.log_decision(resource="payment://international/<=10000", ...) | Verify operation is within defined resource boundary |
| 1.4 (Documentation) | Complete audit trail with timestamps | All receipts are stored with immutable timestamps | Run verify-audit-chain.py |

### Evidence Files

- [implementation/risk-assessment.py](implementation/risk-assessment.py) - Risk assessment implementation
- [examples/financial-services.py](examples/financial-services.py) - Real-world example with risk assessment
- [tests/verify-pillar1.py](tests/verify-pillar1.py) - Automated verification for Pillar 1

---

## 👤 Pillar 2: Make People Meaningfully Accountable

### Framework Requirements

| Requirement ID | Description |
|----------------|-------------|
| 2.1 | Organizations should determine which decisions require human oversight |
| 2.2 | Human oversight should be "meaningful" - supervisors must understand the context |
| 2.3 | Oversight should be documented and auditable |
| 2.4 | Clear accountability chains should be established |

### JEP Implementation

| Requirement | JEP Feature | Implementation | Verification |
|-------------|-------------|----------------|--------------|
| 2.1 (Human oversight points) | delegate() primitive requires human approval | receipt = tracker.delegate_action(proposal_id=prop.id, human_approver="supervisor-456", approval_time=timestamp, understanding_confirmed=True) | Check human_approver field exists |
| 2.2 (Meaningful oversight) | Full context provided to human before approval | print(f"Action: {proposal.action}") print(f"Amount: {proposal.amount} {proposal.currency}") print(f"Risk: {proposal.risk_level}") print(f"Reasoning: {proposal.reasoning}") | Verify receipt contains complete compliance_binding context |
| 2.3 (Documented oversight) | Ed25519 signature provides non-repudiable proof | receipt.signature field | Run verify-signature.py |
| 2.4 (Accountability chains) | Complete chain from judge → delegate → terminate | {"chain": [{"action": "judge", "actor": "agent-123", "time": "t1"}, {"action": "delegate", "actor": "human-456", "time": "t2"}, {"action": "execute", "actor": "agent-123", "time": "t3"}]} | Run verify-accountability-chain.py |

### Evidence Files

- [implementation/accountability.py](implementation/accountability.py) - Core accountability implementation
- [examples/healthcare.py](examples/healthcare.py) - Healthcare example with human oversight
- [tests/verify-pillar2.py](tests/verify-pillar2.py) - Automated verification for Pillar 2

---

## 🔧 Pillar 3: Implement Technical Controls

### Framework Requirements

| Requirement ID | Description |
|----------------|-------------|
| 3.1 | Technical controls should be implemented throughout the agent lifecycle |
| 3.2 | Access controls should follow least privilege principle |
| 3.3 | Activity logs should be maintained for audit purposes |
| 3.4 | Controls should be regularly tested |

### JEP Implementation

| Requirement | JEP Feature | Implementation | Verification |
|-------------|-------------|----------------|--------------|
| 3.1 (Lifecycle controls) | Four primitives cover full lifecycle | judge() | delegate() | execute() | terminate() | Run verify-lifecycle.py |
| 3.2 (Least privilege) | Resource field limits scope of action | resource defines exactly what can be accessed | Verify resource strings match intended scope |
| 3.3 (Audit logs) | Complete immutable audit trail | All receipts stored with parent_hash chain | Run verify-audit-integrity.py |
| 3.4 (Regular testing) | Automated verification scripts | python tests/verify-all-controls.py | Script runs all control tests and generates report |

### Evidence Files

- [implementation/technical-controls.py](implementation/technical-controls.py) - Technical controls implementation
- [examples/public-sector.py](examples/public-sector.py) - Public sector example with strict controls
- [tests/verify-pillar3.py](tests/verify-pillar3.py) - Automated verification for Pillar 3

---

## 👥 Pillar 4: Enable End-User Responsibility

### Framework Requirements

| Requirement ID | Description |
|----------------|-------------|
| 4.1 | End users should be informed when interacting with agentic AI |
| 4.2 | Users should have means to query or challenge decisions |
| 4.3 | Transparency should be provided about AI capabilities and limitations |
| 4.4 | Feedback mechanisms should be available |

### JEP Implementation

| Requirement | JEP Feature | Implementation | Verification |
|-------------|-------------|----------------|--------------|
| 4.1 (Disclosure) | Machine-readable metadata enables automated disclosure | {"is_ai_generated": true, "agent_id": "customer-support-v2"} | Check is_ai_generated field in content provenance |
| 4.2 (Challenge mechanism) | Complete audit trail enables reconstruction | All decisions can be reconstructed from receipts | Run verify-reconstruct.py [receipt_id] |
| 4.3 (Transparency) | JSON-LD provides structured, parseable context | {"operation": "APPROVE_LOAN", "reasoning": "Credit score > 700, DTI < 40%", "model_version": "v2.1.3"} | Parse receipt fields for human-readable explanations |
| 4.4 (Feedback) | Extended fields support feedback integration | receipt.add_feedback(user_id="customer-789", feedback_type="DISPUTE", timestamp=time.time()) | Check feedback fields in extended metadata |

### Evidence Files

- [implementation/transparency.py](implementation/transparency.py) - Transparency implementation
- [examples/financial-services.py](examples/financial-services.py) - Customer-facing example
- [tests/verify-pillar4.py](tests/verify-pillar4.py) - Automated verification for Pillar 4

---

## ✅ Summary: Full Framework Coverage

| Pillar | Requirements Covered | Verification Method | Status |
|--------|---------------------|---------------------|--------|
| 1: Assess Risk | 1.1, 1.2, 1.3, 1.4 | verify-pillar1.py | ✅ Complete |
| 2: Human Accountability | 2.1, 2.2, 2.3, 2.4 | verify-pillar2.py | ✅ Complete |
| 3: Technical Controls | 3.1, 3.2, 3.3, 3.4 | verify-pillar3.py | ✅ Complete |
| 4: End-User Responsibility | 4.1, 4.2, 4.3, 4.4 | verify-pillar4.py | ✅ Complete |

## 🔍 One-Command Verification

Run the complete framework verification:

```bash
# Install verification tools
pip install jep-verification

# Run all pillar tests
python tests/verify-all-pillars.py

# Output
================================
AGENTIC AI FRAMEWORK VERIFICATION
================================
✅ Pillar 1: All 4 requirements met
✅ Pillar 2: All 4 requirements met
✅ Pillar 3: All 4 requirements met
✅ Pillar 4: All 4 requirements met
================================
FULL COMPLIANCE VERIFIED
================================
```

## 📬 Contact

For questions about this mapping or to request additional verification:

- **Email**: singapore@humanjudgment.org
- **GitHub**: [hjs-spec/jep-singapore-solutions](https://github.com/hjs-spec/jep-singapore-solutions)

---

*Last Updated: March 2026*
```
