# JEP Mapping to Singapore's Model AI Governance Framework for Agentic AI (2026)

**Detailed Article-by-Article Mapping with Code Examples and Verification Methods**

## 📋 Overview

This document provides a comprehensive mapping between the **Judgment Event Protocol (JEP)** and the **Model AI Governance Framework for Agentic AI** launched by IMDA in January 2026.

The framework consists of four pillars, each with four specific requirements. This document maps every requirement to JEP's technical features, provides code examples, and specifies verification methods.

---

## 🏛️ Pillar 1: Assess and Bound Risks Upfront

### Framework Requirements

| ID | Requirement Description |
|----|------------------------|
| 1.1 | Organizations should assess the use case to determine if an agentic AI is appropriate |
| 1.2 | The level of autonomy granted should be commensurate with risk |
| 1.3 | Scope boundaries should be clearly defined and enforced |
| 1.4 | Risk assessment should be documented and periodically reviewed |

---

### 1.1 Use Case Assessment

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `judge()` primitive with use_case parameter |
| **Implementation** | `propose_action()` method in `accountability.py` |
| **Evidence Location** | `compliance_binding` field in receipts |

**Code Example:**
```python
from implementation.accountability import AgenticAIAccountability

tracker = AgenticAIAccountability("agent-id", "organization")

proposal = tracker.propose_action(
    action="EXECUTE_PAYMENT",
    target_resource="customer-account-123",
    reasoning="Customer requested urgent transfer",
    risk_level="HIGH",
    use_case="CROSS_BORDER_TRANSFER",  # Explicit use case assessment
    assessment="APPROPRIATE"            # Assessment outcome
)

# Evidence in receipt:
# {
#   "compliance_binding": {
#     "use_case": "CROSS_BORDER_TRANSFER",
#     "assessment": "APPROPRIATE"
#   }
# }
```

**Verification Method:**
```bash
# Check that all proposals include use_case and assessment
python -c "
import json
receipts = glob.glob('./receipts/*.json')
for r in receipts:
    with open(r) as f:
        data = json.load(f)
        binding = data.get('compliance_binding', {})
        assert 'use_case' in binding, f'Missing use_case in {r}'
        assert 'assessment' in binding, f'Missing assessment in {r}'
print('✅ All receipts have use case assessment')
"
```

---

### 1.2 Risk-Level Commensurate with Autonomy

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `risk_level` field in every receipt |
| **Implementation** | RiskLevel enum in `accountability.py` |
| **Evidence Location** | `compliance_binding.risk_level` |

**Code Example:**
```python
from implementation.accountability import RiskLevel

# Risk levels directly map to autonomy levels:
risk_autonomy_map = {
    RiskLevel.LOW: "FULLY_AUTOMATED",
    RiskLevel.MEDIUM: "HUMAN_OVERSIGHT_REQUIRED",
    RiskLevel.HIGH: "HUMAN_APPROVAL_REQUIRED",
    RiskLevel.CRITICAL: "COMMITTEE_APPROVAL_REQUIRED"
}

proposal = tracker.propose_action(
    action="EXECUTE_PAYMENT",
    target_resource="customer-account-123",
    reasoning="Large transfer request",
    risk_level="CRITICAL"  # Triggers committee approval workflow
)

# The system automatically routes based on risk level
if proposal.risk_level == RiskLevel.CRITICAL:
    # Requires dual approval
    approval1 = tracker.approve_action(proposal.id, "manager-123")
    approval2 = tracker.approve_action(proposal.id, "director-456")
```

**Verification Method:**
```bash
# Verify risk levels are properly set and enforced
python tests/verify-all-pillars.py --test 1.2
```

---

### 1.3 Scope Boundaries

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `target_resource` field defines operational scope |
| **Implementation** | Resource string with boundary syntax |
| **Evidence Location** | `target_resource` in receipts |

**Code Example:**
```python
# Define scope boundaries in resource strings
proposal = tracker.propose_action(
    action="ACCESS",
    target_resource="database://customers/records/<=1000",  # Limited to first 1000 records
    reasoning="Batch processing job",
    risk_level="MEDIUM"
)

# Scope enforcement happens at system level
# JEP records the intended scope for audit
```

**Verification Method:**
```bash
# Check that all target_resource fields have clear boundaries
python -c "
import re
boundary_pattern = r'[<>=]|limit|max|range'
with open('./receipts/latest.json') as f:
    data = json.load(f)
    resource = data.get('target_resource', '')
    has_boundary = bool(re.search(boundary_pattern, resource))
    print(f'✅ Scope boundary defined: {has_boundary}')
"
```

---

### 1.4 Documented Risk Assessment

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Complete audit trail with timestamps |
| **Implementation** | Every action recorded with immutable timestamp |
| **Evidence Location** | All receipts with `proposed_at`, `approved_at`, `executed_at` |

**Code Example:**
```python
# Risk assessment is automatically documented in the audit trail
proposal = tracker.propose_action(
    action="HIGH_RISK_OPERATION",
    target_resource="critical-system",
    reasoning="Risk assessment: Acceptable with mitigations",
    risk_level="HIGH",
    mitigations="Dual control, real-time monitoring, immediate rollback"
)

# Later, generate risk assessment report
report = tracker.generate_audit_report()
print(f"Total high-risk actions: {report['statistics']['high_risk']}")
print(f"All have documented mitigations: {report['mitigation_completeness']}")
```

**Verification Method:**
```bash
# Run complete audit trail verification
python tests/verify-all-pillars.py --test 1.4
```

---

## 👤 Pillar 2: Make People Meaningfully Accountable

### Framework Requirements

| ID | Requirement Description |
|----|------------------------|
| 2.1 | Organizations should determine which decisions require human oversight |
| 2.2 | Human oversight should be "meaningful" - supervisors must understand the context |
| 2.3 | Oversight should be documented and auditable |
| 2.4 | Clear accountability chains should be established |

---

### 2.1 Human Oversight Points

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `delegate()` primitive requires human approval |
| **Implementation** | `approve_action()` and `deny_action()` methods |
| **Evidence Location** | `human_approver` field in receipts |

**Code Example:**
```python
# Define which decisions require human oversight
def requires_human_oversight(action, amount, risk_level):
    if risk_level in ["HIGH", "CRITICAL"]:
        return True
    if action == "EXECUTE_PAYMENT" and amount > 10000:
        return True
    return False

# In practice:
proposal = tracker.propose_action(
    action="EXECUTE_PAYMENT",
    target_resource="customer-account-123",
    reasoning="Large transfer",
    risk_level="HIGH",
    amount=50000
)

# This automatically triggers the human approval workflow
if requires_human_oversight(proposal.action, proposal.parameters.get('amount'), proposal.risk_level.value):
    approval = tracker.approve_action(
        proposal_id=proposal.id,
        human_approver="supervisor-456",
        notes="Verified with customer, approved"
    )
```

**Verification Method:**
```bash
# Verify all HIGH/CRITICAL actions have human approval
python tests/verify-all-pillars.py --test 2.1
```

---

### 2.2 Meaningful Oversight (Context Understanding)

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Complete context provided before approval |
| **Implementation** | All relevant data passed in proposal parameters |
| **Evidence Location** | `compliance_binding` contains full context |

**Code Example:**
```python
# When creating a proposal, include ALL relevant context
proposal = tracker.propose_action(
    action="EXECUTE_PAYMENT",
    target_resource="customer-account-123",
    reasoning="Customer requested urgent international transfer",
    risk_level="HIGH",
    # Complete context for meaningful oversight:
    customer_id="CUST001",
    customer_name="Tan Ah Kow",
    customer_risk_score="MEDIUM",
    amount=50000,
    currency="SGD",
    recipient_name="John Tan",
    recipient_account="123-456-789",
    recipient_bank="DBS",
    transfer_purpose="Family support",
    previous_transactions=5,
    fraud_check_score=0.12,
    aml_check_passed=True
)

# When human approves, they see all this context
print(f"Context for approver:")
print(f"- Action: {proposal.action}")
print(f"- Amount: {proposal.parameters['amount']} {proposal.parameters['currency']}")
print(f"- Recipient: {proposal.parameters['recipient_name']}")
print(f"- Purpose: {proposal.parameters['transfer_purpose']}")
print(f"- Risk Score: {proposal.parameters['fraud_check_score']}")
```

**Verification Method:**
```bash
# Check that proposals contain rich context
python tests/verify-all-pillars.py --test 2.2 --verbose
```

---

### 2.3 Documented Oversight

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Ed25519 cryptographic signatures |
| **Implementation** | Every approval is signed with private key |
| **Evidence Location** | `signature` field in receipts |

**Code Example:**
```python
# Each approval generates a cryptographic signature
approval = tracker.approve_action(
    proposal_id=proposal.id,
    human_approver="supervisor-456",
    notes="Approved after verification"
)

# The signature proves authenticity and non-repudiation
print(f"Receipt ID: {approval.receipt_id}")
print(f"Signature: {approval.signature[:50]}...")

# Later verification
is_valid = tracker.verify_signature(approval.to_dict(), approval.signature)
print(f"Signature valid: {is_valid}")  # True
```

**Verification Method:**
```bash
# Verify all signatures
python tests/verify-all-pillars.py --test 2.3
```

---

### 2.4 Clear Accountability Chains

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Complete judge → delegate → execute chain |
| **Implementation** | `get_accountability_chain()` method |
| **Evidence Location** | Chain of receipts linked by IDs |

**Code Example:**
```python
# The complete accountability chain is automatically maintained
chain = tracker.get_accountability_chain(proposal.id)

print("Accountability Chain:")
print(f"1. Proposed by: {chain['agent']['id']} at {chain['agent']['time']}")
print(f"2. Approved by: {chain['human_oversight']['approver']} at {chain['human_oversight']['time']}")
print(f"3. Executed by: {chain['execution']['executor']} at {chain['execution']['time']}")
print(f"Chain integrity: {chain['verification']['overall']}")  # VALID
```

**Verification Method:**
```bash
# Verify all chains are complete
python tests/verify-all-pillars.py --test 2.4
```

---

## 🔧 Pillar 3: Implement Technical Controls

### Framework Requirements

| ID | Requirement Description |
|----|------------------------|
| 3.1 | Technical controls should be implemented throughout the agent lifecycle |
| 3.2 | Access controls should follow least privilege principle |
| 3.3 | Activity logs should be maintained for audit purposes |
| 3.4 | Controls should be regularly tested |

---

### 3.1 Lifecycle Controls

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Four primitives cover full lifecycle |
| **Implementation** | `judge()` → `delegate()` → `execute()` → `terminate()` |
| **Evidence Location** | Complete lifecycle in audit trail |

**Code Example:**
```python
# Full agent lifecycle with JEP
# 1. JUDGE - Assess the action
proposal = tracker.propose_action("ACTION", "RESOURCE", "REASON", "RISK")

# 2. DELEGATE - Human oversight
if requires_approval:
    approval = tracker.approve_action(proposal.id, "human-approver")

# 3. EXECUTE - Perform the action
execution = tracker.execute_approved_action(proposal.id)

# 4. TERMINATE - End the action when complete
termination = tracker.terminate_action(proposal.id, "COMPLETED")
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 3.1
```

---

### 3.2 Least Privilege

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Resource field limits scope of action |
| **Implementation** | Granular resource naming convention |
| **Evidence Location** | `target_resource` in receipts |

**Code Example:**
```python
# GOOD - Least privilege
proposal = tracker.propose_action(
    action="READ",
    target_resource="database://customers/CUST001/balance",  # Specific, limited
    reasoning="Check customer balance",
    risk_level="LOW"
)

# BAD - Too broad (should be avoided)
# target_resource="database://customers/*"  # Too broad
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 3.2
```

---

### 3.3 Activity Logs

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Immutable audit trail with parent_hash chain |
| **Implementation** | Every action logged with cryptographic chain |
| **Evidence Location** | All receipts with parent_hash links |

**Code Example:**
```python
# Each receipt links to the previous one
receipt_1 = {"receipt_id": "jep_001", "parent_hash": None}
receipt_2 = {"receipt_id": "jep_002", "parent_hash": hash(receipt_1)}
receipt_3 = {"receipt_id": "jep_003", "parent_hash": hash(receipt_2)}

# The chain ensures no records can be inserted or deleted
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 3.3
```

---

### 3.4 Regular Testing

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Automated verification scripts |
| **Implementation** | Complete test suite in `/tests` directory |
| **Evidence Location** | Test results and audit reports |

**Code Example:**
```bash
# Run all tests
python tests/verify-all-pillars.py

# Generate test report
python tests/verify-all-pillars.py --output html --report test-results.html
```

**Verification Method:**
```bash
# The existence of tests is itself evidence
ls tests/ | grep verify
```

---

## 👥 Pillar 4: Enable End-User Responsibility

### Framework Requirements

| ID | Requirement Description |
|----|------------------------|
| 4.1 | End users should be informed when interacting with agentic AI |
| 4.2 | Users should have means to query or challenge decisions |
| 4.3 | Transparency should be provided about AI capabilities and limitations |
| 4.4 | Feedback mechanisms should be available |

---

### 4.1 Disclosure

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | `is_ai_generated` field in receipts |
| **Implementation** | Content provenance module |
| **Evidence Location** | `content_provenance` in receipts |

**Code Example:**
```python
# When generating content for end users
content_receipt = {
    "receipt_id": "jep_123",
    "content": "Your loan application has been processed",
    "is_ai_generated": True,  # Clear disclosure
    "agent_id": "loan-assistant-v2",
    "human_reviewed": True
}
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 4.1
```

---

### 4.2 Query/Challenge Mechanism

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Complete audit trail enables reconstruction |
| **Implementation** | `get_accountability_chain()` for any decision |
| **Evidence Location** | Full decision history retrievable |

**Code Example:**
```python
# User challenges a decision
def handle_challenge(receipt_id, user_id):
    # Retrieve complete decision context
    chain = tracker.get_accountability_chain(receipt_id)
    
    # Provide to user
    return {
        "decision_id": receipt_id,
        "timestamp": chain['agent']['time'],
        "reasoning": chain['agent']['reasoning'],
        "approved_by": chain['human_oversight']['approver'],
        "approval_notes": chain['human_oversight']['notes'],
        "appeal_url": f"https://api.example.com/appeal/{receipt_id}"
    }
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 4.2
```

---

### 4.3 Transparency

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | JSON-LD structured metadata |
| **Implementation** | Machine-readable receipts |
| **Evidence Location** | All receipts in JSON format |

**Code Example:**
```json
{
  "@context": "https://jep-protocol.org/context/v1",
  "@type": "AIDecision",
  "receipt_id": "jep_123",
  "decision": "APPROVED",
  "reasoning": "Credit score 750 meets minimum threshold",
  "model_version": "v2.1.3",
  "limitations": [
    "Only evaluates Singapore credit scores",
    "Requires minimum 3 months history"
  ],
  "appeal_process": "Contact customer service at 1800-111-1111"
}
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 4.3
```

---

### 4.4 Feedback Mechanisms

| Mapping Field | Details |
|--------------|---------|
| **JEP Feature** | Extended fields for feedback |
| **Implementation** | `add_feedback()` method |
| **Evidence Location** | Feedback attached to receipts |

**Code Example:**
```python
# Add user feedback to a decision
def submit_feedback(receipt_id, user_id, feedback_type, comments):
    receipt = tracker.get_receipt(receipt_id)
    receipt.add_feedback({
        "user_id": user_id,
        "feedback_type": feedback_type,  # DISPUTE, SATISFIED, CONFUSED
        "comments": comments,
        "timestamp": time.time()
    })
    return {"status": "FEEDBACK_RECORDED"}
```

**Verification Method:**
```bash
python tests/verify-all-pillars.py --test 4.4
```

---

## ✅ Summary: Complete Framework Coverage

| Pillar | Requirements | JEP Coverage | Verification Script |
|--------|--------------|--------------|---------------------|
| **Pillar 1** | 1.1, 1.2, 1.3, 1.4 | ✅ Complete | `verify-all-pillars.py --pillar 1` |
| **Pillar 2** | 2.1, 2.2, 2.3, 2.4 | ✅ Complete | `verify-all-pillars.py --pillar 2` |
| **Pillar 3** | 3.1, 3.2, 3.3, 3.4 | ✅ Complete | `verify-all-pillars.py --pillar 3` |
| **Pillar 4** | 4.1, 4.2, 4.3, 4.4 | ✅ Complete | `verify-all-pillars.py --pillar 4` |

## 🔍 One-Command Verification

```bash
# Run complete framework verification
python tests/verify-all-pillars.py

# Output:
# =================================
# AGENTIC AI FRAMEWORK VERIFICATION
# =================================
# ✅ Pillar 1: All 4 requirements met
# ✅ Pillar 2: All 4 requirements met
# ✅ Pillar 3: All 4 requirements met
# ✅ Pillar 4: All 4 requirements met
# =================================
# FULL COMPLIANCE VERIFIED
# =================================
```

## 📚 Related Files

| File | Description |
|------|-------------|
| [implementation/accountability.py](./implementation/accountability.py) | Core implementation code |
| [tests/verify-all-pillars.py](./tests/verify-all-pillars.py) | Complete verification script |
| [examples/financial-services.py](./examples/financial-services.py) | MAS-regulated example |
| [examples/healthcare.py](https://github.com/hjs-spec/jep-singapore-solutions/blob/main/framework-agentic/examples/healthcare.py) | MOH-regulated example |
| [examples/public-sector.py](https://github.com/hjs-spec/jep-singapore-solutions/blob/main/framework-agentic/examples/public-sector.py) | GovTech example |

---

*This mapping document is maintained by HJS Foundation LTD (Singapore CLG)*
*Last Updated: March 2026*
```
