# AIM Toolkit 49 Checks - JEP Evidence Mapping

**Complete mapping between AIM Toolkit's 49 process checks and JEP evidence**

## 📋 Overview

This document provides a detailed mapping between the **AI Markets (AIM) Toolkit**'s 49 process checks and the evidence that can be generated from JEP receipts. Each check includes:

- **Check ID** and **Description** from AIM Toolkit
- **JEP Evidence** that demonstrates compliance
- **Verification Method** to validate the evidence
- **Sample Output** showing what the evidence looks like

---

## 🔷 Principle 1: Accountability (A1-A7)

### A1: Clear allocation of responsibilities

| Field | Value |
|-------|-------|
| **Check ID** | A1 |
| **Description** | Are responsibilities for AI system outcomes clearly allocated to specific individuals or roles? |
| **JEP Evidence** | `actor_id` field in every receipt identifies the responsible entity |
| **Verification** | Run `verify-aim-check.py A1 --receipt-dir ./receipts/` |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890ab",
  "compliance_binding": {
    "actor_id": "loan-agent-v2",
    "human_approver": "supervisor-456",
    "risk_level": "HIGH"
  }
}
```

---

### A2: Governance framework documented

| Field | Value |
|-------|-------|
| **Check ID** | A2 |
| **Description** | Is there a documented governance framework for AI systems? |
| **JEP Evidence** | `governance` field in audit reports documents the framework |
| **Verification** | Check audit report for governance documentation |

**Sample Evidence**:
```json
{
  "audit_report": {
    "governance": {
      "framework_version": "1.2",
      "last_review": "2026-02-15",
      "responsible_officer": "Chief Compliance Officer",
      "review_frequency": "Quarterly",
      "escalation_procedure": "Any HIGH risk decision requires manager approval"
    }
  }
}
```

---

### A3: Regular compliance reviews

| Field | Value |
|-------|-------|
| **Check ID** | A3 |
| **Description** | Are regular compliance reviews conducted for AI systems? |
| **JEP Evidence** | `review_timestamp` in audit report shows review frequency |
| **Verification** | Check audit report for review timestamps |

**Sample Evidence**:
```json
{
  "audit_report": {
    "reviews": [
      {"date": "2026-01-15", "reviewer": "compliance-team", "findings": "None"},
      {"date": "2026-02-15", "reviewer": "compliance-team", "findings": "None"},
      {"date": "2026-03-15", "reviewer": "compliance-team", "findings": "Minor issues"}
    ]
  }
}
```

---

### A4: Risk assessment documented

| Field | Value |
|-------|-------|
| **Check ID** | A4 |
| **Description** | Are risk assessments documented for AI systems? |
| **JEP Evidence** | `risk_level` field in every receipt records assessed risk |
| **Verification** | Run `verify-aim-check.py A4 --receipt-dir ./receipts/` |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890ac",
  "compliance_binding": {
    "risk_level": "CRITICAL",
    "risk_factors": ["Large transaction amount", "New recipient"],
    "risk_assessment_date": "2026-03-07T10:30:00Z"
  }
}
```

---

### A5: Incident response plan

| Field | Value |
|-------|-------|
| **Check ID** | A5 |
| **Description** | Is there an incident response plan for AI failures? |
| **JEP Evidence** | `incident_response` field in extended data documents incidents |
| **Verification** | Check for incident response records |

**Sample Evidence**:
```json
{
  "incident_response": {
    "incident_id": "INC-2026-03-05-001",
    "detection_time": "2026-03-05T14:30:00Z",
    "response_time": "2026-03-05T14:45:00Z",
    "resolution_time": "2026-03-05T16:20:00Z",
    "impact": "23 transactions delayed",
    "root_cause": "Model drift detected",
    "corrective_action": "Model retrained and redeployed"
  }
}
```

---

### A6: Third-party risk management

| Field | Value |
|-------|-------|
| **Check ID** | A6 |
| **Description** | Are third-party AI providers subject to risk management? |
| **JEP Evidence** | `provider_id` field identifies third-party providers |
| **Verification** | Check for third-party provider documentation |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890ad",
  "provider_id": "vendor-credit-scoring-inc",
  "provider_due_diligence": {
    "last_review": "2026-02-01",
    "review_status": "PASSED",
    "certifications": ["ISO 27001", "SOC2 Type II"]
  }
}
```

---

### A7: Board and management oversight

| Field | Value |
|-------|-------|
| **Check ID** | A7 |
| **Description** | Is there board and management oversight of AI systems? |
| **JEP Evidence** | `board_review` field in audit report documents oversight |
| **Verification** | Check audit report for board review records |

**Sample Evidence**:
```json
{
  "audit_report": {
    "board_reviews": [
      {"date": "2026-01-20", "presented_by": "CTO", "minutes_ref": "BOD-2026-01-20"},
      {"date": "2026-02-17", "presented_by": "CTO", "minutes_ref": "BOD-2026-02-17"},
      {"date": "2026-03-16", "presented_by": "CTO", "minutes_ref": "BOD-2026-03-16"}
    ]
  }
}
```

---

## 🔷 Principle 2: Transparency (T1-T6)

### T1: Clear disclosure of AI use

| Field | Value |
|-------|-------|
| **Check ID** | T1 |
| **Description** | Is AI use clearly disclosed to consumers? |
| **JEP Evidence** | `is_ai_generated` field in content provenance |
| **Verification** | Check content receipts for disclosure flag |

**Sample Evidence**:
```json
{
  "content_provenance": {
    "content_id": "jep_018e1234-5678-7000-8000-1234567890ae",
    "is_ai_generated": true,
    "disclosure_text": "This response was generated by our AI assistant",
    "human_reviewed": true
  }
}
```

---

### T2: Explainable decisions

| Field | Value |
|-------|-------|
| **Check ID** | T2 |
| **Description** | Are AI decisions explainable to consumers? |
| **JEP Evidence** | `reasoning` field provides decision explanation |
| **Verification** | Check receipts for reasoning field |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890af",
  "reasoning": "Loan declined due to credit score (650) below minimum threshold (700)",
  "explanation_factors": {
    "primary": "Credit score too low",
    "secondary": ["Limited credit history", "High DTI ratio"]
  }
}
```

---

### T3: Terms and conditions accessible

| Field | Value |
|-------|-------|
| **Check ID** | T3 |
| **Description** | Are terms and conditions easily accessible? |
| **JEP Evidence** | `terms_uri` field links to current terms |
| **Verification** | Check receipt for terms link |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890b0",
  "terms_uri": "https://dbs.com/ai-terms/v2.1",
  "terms_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4",
  "terms_acknowledged": true
}
```

---

### T4: Privacy policy accessible

| Field | Value |
|-------|-------|
| **Check ID** | T4 |
| **Description** | Is privacy policy easily accessible? |
| **JEP Evidence** | `privacy_uri` field links to privacy policy |
| **Verification** | Check receipt for privacy link |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890b1",
  "privacy_uri": "https://dbs.com/privacy/v3.0",
  "privacy_hash": "sha256:8f32c12e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c"
}
```

---

### T5: Consumer rights explained

| Field | Value |
|-------|-------|
| **Check ID** | T5 |
| **Description** | Are consumer rights clearly explained? |
| **JEP Evidence** | `rights_explanation` field documents rights disclosure |
| **Verification** | Check for rights documentation |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890b2",
  "rights_explanation": {
    "right_to_information": true,
    "right_to_correction": true,
    "right_to_withdraw_consent": true,
    "right_to_lodge_complaint": true,
    "explanation_provided": "2026-03-07T10:30:00Z"
  }
}
```

---

### T6: Complaint mechanism available

| Field | Value |
|-------|-------|
| **Check ID** | T6 |
| **Description** | Is a complaint mechanism available? |
| **JEP Evidence** | `complaint_uri` field links to complaint mechanism |
| **Verification** | Check for complaint mechanism documentation |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890b3",
  "complaint_uri": "https://dbs.com/complaint",
  "complaint_instructions": "Email complaint@dbs.com or call 1800-111-1111"
}
```

---

## 🔷 Principle 3: Accuracy (AC1-AC7)

### AC1: Accuracy metrics tracked

| Field | Value |
|-------|-------|
| **Check ID** | AC1 |
| **Description** | Are accuracy metrics tracked for AI systems? |
| **JEP Evidence** | `accuracy_metrics` in audit report |
| **Verification** | Check audit report for accuracy data |

**Sample Evidence**:
```json
{
  "audit_report": {
    "accuracy_metrics": {
      "overall_accuracy": 0.97,
      "precision": 0.96,
      "recall": 0.98,
      "f1_score": 0.97,
      "measurement_period": "30 days"
    }
  }
}
```

---

### AC2: Validation datasets documented

| Field | Value |
|-------|-------|
| **Check ID** | AC2 |
| **Description** | Are validation datasets documented? |
| **JEP Evidence** | `validation_data` field in model documentation |
| **Verification** | Check for validation dataset documentation |

**Sample Evidence**:
```json
{
  "model_documentation": {
    "validation_data": {
      "source": "Historical loan data 2023-2024",
      "size": 50000,
      "date_range": "2023-01-01 to 2024-12-31",
      "split_method": "80/20 random",
      "last_validation": "2026-02-15"
    }
  }
}
```

---

### AC3: Performance monitoring

| Field | Value |
|-------|-------|
| **Check ID** | AC3 |
| **Description** | Is performance continuously monitored? |
| **JEP Evidence** | `performance_alerts` in extended data |
| **Verification** | Check for performance monitoring records |

**Sample Evidence**:
```json
{
  "performance_alerts": [
    {
      "alert_id": "PERF-2026-03-05-001",
      "metric": "response_time",
      "threshold": 1000,
      "actual": 1200,
      "alert_time": "2026-03-05T14:30:00Z",
      "action_taken": "scaled_up_instances"
    }
  ]
}
```

---

### AC4: Model drift detection

| Field | Value |
|-------|-------|
| **Check ID** | AC4 |
| **Description** | Is model drift detected and addressed? |
| **JEP Evidence** | `drift_detection` in audit report |
| **Verification** | Check for drift detection records |

**Sample Evidence**:
```json
{
  "drift_detection": {
    "last_check": "2026-03-07",
    "drift_score": 0.12,
    "threshold": 0.15,
    "status": "NORMAL",
    "action_required": "None"
  }
}
```

---

### AC5: Retraining procedures

| Field | Value |
|-------|-------|
| **Check ID** | AC5 |
| **Description** | Are retraining procedures documented? |
| **JEP Evidence** | `retraining_log` in model documentation |
| **Verification** | Check for retraining records |

**Sample Evidence**:
```json
{
  "retraining_log": [
    {
      "retrain_date": "2026-02-01",
      "model_version": "2.1.0",
      "new_data_size": 10000,
      "performance_before": 0.95,
      "performance_after": 0.97,
      "trigger_reason": "Scheduled monthly retraining"
    },
    {
      "retrain_date": "2026-03-01",
      "model_version": "2.1.1",
      "new_data_size": 12000,
      "performance_before": 0.97,
      "performance_after": 0.97,
      "trigger_reason": "Scheduled monthly retraining"
    }
  ]
}
```

---

### AC6: Version control

| Field | Value |
|-------|-------|
| **Check ID** | AC6 |
| **Description** | Are AI models under version control? |
| **JEP Evidence** | `model_version` field in every receipt |
| **Verification** | Check receipts for version information |

**Sample Evidence**:
```json
{
  "receipt_id": "jep_018e1234-5678-7000-8000-1234567890b4",
  "model_version": "2.1.3",
  "model_hash": "sha256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

---

### AC7: Change management

| Field | Value |
|-------|-------|
| **Check ID** | AC7 |
| **Description** | Is there a change management process? |
| **JEP Evidence** | `change_log` in model documentation |
| **Verification** | Check for change management records |

**Sample Evidence**:
```json
{
  "change_log": [
    {
      "change_id": "CHG-2026-02-15-001",
      "description": "Update credit scoring algorithm",
      "approver": "model-governance-committee",
      "approval_date": "2026-02-15",
      "implementation_date": "2026-02-16",
      "rollback_plan": "Revert to version 2.1.2"
    }
  ]
}
```

---

## 🔷 Principle 4: Fairness (F1-F6)

### F1: Bias testing performed

| Field | Value |
|-------|-------|
| **Check ID** | F1 |
| **Description** | Is bias testing performed on AI systems? |
| **JEP Evidence** | `bias_test_results` in audit report |
| **Verification** | Check for bias testing records |

**Sample Evidence**:
```json
{
  "bias_test_results": {
    "test_date": "2026-02-28",
    "protected_attributes": ["age", "gender", "race"],
    "disparate_impact": 0.98,
    "status": "PASSED",
    "notes": "No significant bias detected"
  }
}
```

---

### F2: Demographic parity

| Field | Value |
|-------|-------|
| **Check ID** | F2 |
| **Description** | Is demographic parity monitored? |
| **JEP Evidence** | `demographic_metrics` in audit report |
| **Verification** | Check for demographic data |

**Sample Evidence**:
```json
{
  "demographic_metrics": {
    "age_20-30": {"approval_rate": 0.75, "sample_size": 1200},
    "age_31-40": {"approval_rate": 0.78, "sample_size": 1500},
    "age_41-50": {"approval_rate": 0.76, "sample_size": 1100},
    "age_51+": {"approval_rate": 0.73, "sample_size": 800}
  }
}
```

---

### F3: Fairness metrics tracked

| Field | Value |
|-------|-------|
| **Check ID** | F3 |
| **Description** | Are fairness metrics tracked over time? |
| **JEP Evidence** | `fairness_trends` in audit report |
| **Verification** | Check for fairness trend data |

**Sample Evidence**:
```json
{
  "fairness_trends": {
    "2026-01": 0.97,
    "2026-02": 0.96,
    "2026-03": 0.98,
    "trend": "STABLE"
  }
}
```

---

### F4: Disparate impact analysis

| Field | Value |
|-------|-------|
| **Check ID** | F4 |
| **Description** | Is disparate impact analyzed? |
| **JEP Evidence** | `disparate_impact` in audit report |
| **Verification** | Check for disparate impact analysis |

**Sample Evidence**:
```json
{
  "disparate_impact": {
    "analysis_date": "2026-02-28",
    "four_fifths_rule": "PASSED",
    "statistical_significance": "p=0.12",
    "action_required": "None"
  }
}
```

---

### F5: Mitigation strategies documented

| Field | Value |
|-------|-------|
| **Check ID** | F5 |
| **Description** | Are fairness mitigation strategies documented? |
| **JEP Evidence** | `fairness_mitigations` in audit report |
| **Verification** | Check for mitigation documentation |

**Sample Evidence**:
```json
{
  "fairness_mitigations": [
    {
      "bias_type": "age",
      "mitigation": "Balanced training data",
      "implementation_date": "2026-01-15",
      "effectiveness": "90% reduction in age bias"
    }
  ]
}
```

---

### F6: Regular fairness audits

| Field | Value |
|-------|-------|
| **Check ID** | F6 |
| **Description** | Are fairness audits conducted regularly? |
| **JEP Evidence** | `fairness_audits` in audit report |
| **Verification** | Check for audit records |

**Sample Evidence**:
```json
{
  "fairness_audits": [
    {"date": "2026-01-20", "auditor": "internal", "findings": "None"},
    {"date": "2026-02-20", "auditor": "internal", "findings": "Minor"},
    {"date": "2026-03-20", "auditor": "external", "findings": "None"}
  ]
}
```

---

## 🔷 Principle 5: Pro-competitive Algorithms (PC1-PC7)

### PC1: Algorithm change disclosure

| Field | Value |
|-------|-------|
| **Check ID** | PC1 |
| **Description** | Are algorithm changes disclosed? |
| **JEP Evidence** | `algorithm_changes` in audit report |
| **Verification** | Check for change disclosure records |

**Sample Evidence**:
```json
{
  "algorithm_changes": [
    {
      "change_date": "2026-02-01",
      "description": "Updated ranking algorithm",
      "disclosure_date": "2026-01-15",
      "disclosure_method": "Email to all customers"
    }
  ]
}
```

---

### PC2: Impact assessment

| Field | Value |
|-------|-------|
| **Check ID** | PC2 |
| **Description** | Is competition impact assessed? |
| **JEP Evidence** | `competition_impact` in audit report |
| **Verification** | Check for impact assessments |

**Sample Evidence**:
```json
{
  "competition_impact": {
    "assessment_date": "2026-01-15",
    "market_share": "15%",
    "competitors": ["OCBC", "UOB", "Maybank"],
    "impact_rating": "LOW",
    "recommendations": "None"
  }
}
```

---

### PC3: Non-discriminatory access

| Field | Value |
|-------|-------|
| **Check ID** | PC3 |
| **Description** | Is access non-discriminatory? |
| **JEP Evidence** | `access_logs` showing fair treatment |
| **Verification** | Check access patterns across user groups |

**Sample Evidence**:
```json
{
  "access_logs": {
    "total_requests": 10000,
    "approved_by_segment": {
      "existing_customers": {"requests": 6000, "approval_rate": 0.85},
      "new_customers": {"requests": 4000, "approval_rate": 0.83}
    }
  }
}
```

---

### PC4: Data portability

| Field | Value |
|-------|-------|
| **Check ID** | PC4 |
| **Description** | Is data portability supported? |
| **JEP Evidence** | `portability_logs` showing data exports |
| **Verification** | Check for portability requests |

**Sample Evidence**:
```json
{
  "portability_logs": [
    {
      "request_id": "PORT-2026-03-05-001",
      "user_hash": "a1b2c3d4e5f6g7h8",
      "request_date": "2026-03-05",
      "fulfillment_date": "2026-03-06",
      "data_format": "JSON"
    }
  ]
}
```

---

### PC5: Interoperability standards

| Field | Value |
|-------|-------|
| **Check ID** | PC5 |
| **Description** | Are interoperability standards followed? |
| **JEP Evidence** | `api_standards` documentation |
| **Verification** | Check API documentation |

**Sample Evidence**:
```json
{
  "api_standards": {
    "version": "2.1",
    "formats": ["JSON", "XML"],
    "authentication": "OAuth 2.0",
    "rate_limits": "1000/hour",
    "documentation_url": "https://api.dbs.com/docs"
  }
}
```

---

### PC6: Switching costs minimized

| Field | Value |
|-------|-------|
| **Check ID** | PC6 |
| **Description** | Are switching costs minimized? |
| **JEP Evidence** | `switching_guides` documentation |
| **Verification** | Check for customer guides |

**Sample Evidence**:
```json
{
  "switching_guides": {
    "available": true,
    "formats": ["PDF", "HTML"],
    "languages": ["EN", "ZH", "MS", "TA"],
    "last_updated": "2026-01-15"
  }
}
```

---

### PC7: Complaint handling for competition issues

| Field | Value |
|-------|-------|
| **Check ID** | PC7 |
| **Description** | Are competition complaints handled? |
| **JEP Evidence** | `competition_complaints` log |
| **Verification** | Check complaint records |

**Sample Evidence**:
```json
{
  "competition_complaints": [
    {
      "complaint_id": "COMP-2026-02-10-001",
      "date": "2026-02-10",
      "nature": "Algorithmic bias",
      "status": "RESOLVED",
      "resolution_date": "2026-02-28"
    }
  ]
}
```

---

## 🔷 Principle 6: Consumer Protection (C1-C7)

### C1: Consent obtained

| Field | Value |
|-------|-------|
| **Check ID** | C1 |
| **Description** | Is consent obtained for data use? |
| **JEP Evidence** | `consent_record` in extended data |
| **Verification** | Check for consent records |

**Sample Evidence**:
```json
{
  "consent_record": {
    "consent_id": "CONSENT-2026-03-07-001",
    "user_hash": "a1b2c3d4e5f6g7h8",
    "consent_date": "2026-03-07",
    "consent_type": "MARKETING",
    "channels": ["email", "sms"],
    "expiry_date": "2027-03-07"
  }
}
```

---

### C2: Consent withdrawal mechanism

| Field | Value |
|-------|-------|
| **Check ID** | C2 |
| **Description** | Can consumers withdraw consent? |
| **JEP Evidence** | `consent_withdrawal` logs |
| **Verification** | Check for withdrawal records |

**Sample Evidence**:
```json
{
  "consent_withdrawal": [
    {
      "withdrawal_id": "WITHDRAW-2026-03-06-001",
      "user_hash": "b2c3d4e5f6g7h8i9",
      "withdrawal_date": "2026-03-06",
      "consent_type": "MARKETING",
      "effective_date": "2026-03-06"
    }
  ]
}
```

---

### C3: Data minimization

| Field | Value |
|-------|-------|
| **Check ID** | C3 |
| **Description** | Is data minimization practiced? |
| **JEP Evidence** | JEP receipts contain only metadata, no PII |
| **Verification** | Check receipts for PII |

**Sample Evidence**:
```json
{
  "evidence_snapshot": {
    "中立性检查": "上下文未检测到个人身份信息",
    "comment": "仅包含用于法律责任的元数据"
  }
}
```

---

### C4: Data retention limits

| Field | Value |
|-------|-------|
| **Check ID** | C4 |
| **Description** | Are data retention limits enforced? |
| **JEP Evidence** | `retention_policy` and deletion logs |
| **Verification** | Check for data deletion records |

**Sample Evidence**:
```json
{
  "retention_policy": {
    "audit_logs": "7 years",
    "consent_records": "Duration of consent + 1 year",
    "transaction_data": "7 years",
    "deletion_schedule": "Monthly automated deletion"
  }
}
```

---

### C5: Data accuracy

| Field | Value |
|-------|-------|
| **Check ID** | C5 |
| **Description** | Is data accuracy maintained? |
| **JEP Evidence** | `data_correction` logs |
| **Verification** | Check for correction records |

**Sample Evidence**:
```json
{
  "data_correction": [
    {
      "correction_id": "CORR-2026-03-04-001",
      "user_hash": "c3d4e5f6g7h8i9j0",
      "correction_date": "2026-03-04",
      "field_corrected": "address",
      "old_value_hash": "hash123",
      "new_value_hash": "hash456"
    }
  ]
}
```

---

### C6: Security measures

| Field | Value |
|-------|-------|
| **Check ID** | C6 |
| **Description** | Are security measures implemented? |
| **JEP Evidence** | Ed25519 signatures, encryption metadata |
| **Verification** | Check for security controls |

**Sample Evidence**:
```json
{
  "security_measures": {
    "encryption_at_rest": "AES-256",
    "encryption_in_transit": "TLS 1.3",
    "signatures": "Ed25519 (RFC 8032)",
    "access_control": "RBAC",
    "last_security_audit": "2026-02-28"
  }
}
```

---

### C7: Breach notification

| Field | Value |
|-------|-------|
| **Check ID** | C7 |
| **Description** | Is there a breach notification process? |
| **JEP Evidence** | `breach_notification` logs |
| **Verification** | Check for breach notification records |

**Sample Evidence**:
```json
{
  "breach_notification": {
    "breach_id": "BREACH-2026-03-01-001",
    "detection_date": "2026-03-01",
    "notification_date": "2026-03-01",
    "affected_users": 150,
    "regulator_notified": "IMDA, CCS",
    "remediation": "Password reset for all affected users"
  }
}
```

---

## 🔷 Principle 7: Data Governance (D1-D5)

### D1: Data inventory maintained

| Field | Value |
|-------|-------|
| **Check ID** | D1 |
| **Description** | Is a data inventory maintained? |
| **JEP Evidence** | `data_inventory` in audit report |
| **Verification** | Check for data inventory |

**Sample Evidence**:
```json
{
  "data_inventory": {
    "personal_data": ["NRIC_hash", "name_hash", "address_hash"],
    "transaction_data": ["amount", "date", "product"],
    "derived_data": ["credit_score", "risk_profile"],
    "retention_periods": {
      "personal_data": "7 years",
      "transaction_data": "7 years",
      "derived_data": "3 years"
    }
  }
}
```

---

### D2: Data quality processes

| Field | Value |
|-------|-------|
| **Check ID** | D2 |
| **Description** | Are data quality processes in place? |
| **JEP Evidence** | `data_quality` metrics |
| **Verification** | Check for quality metrics |

**Sample Evidence**:
```json
{
  "data_quality": {
    "completeness": "99.8%",
    "accuracy": "99.5%",
    "timeliness": "Real-time",
    "last_quality_audit": "2026-02-28",
    "issues_found": 3,
    "issues_resolved": 3
  }
}
```

---

### D3: Data lineage documented

| Field | Value |
|-------|-------|
| **Check ID** | D3 |
| **Description** | Is data lineage documented? |
| **JEP Evidence** | `data_lineage` in audit report |
| **Verification** | Check for lineage documentation |

**Sample Evidence**:
```json
{
  "data_lineage": {
    "source_systems": ["Core Banking", "CRM", "Credit Bureau"],
    "transformations": ["Normalization", "Feature engineering"],
    "output_models": ["Loan approval", "Credit scoring"],
    "lineage_graph": "data-lineage-2026-03-07.dot"
  }
}
```

---

### D4: Data protection impact assessment

| Field | Value |
|-------|-------|
| **Check ID** | D4 |
| **Description** | Are DPIAs conducted? |
| **JEP Evidence** | `dpia` records |
| **Verification** | Check for DPIA documentation |

**Sample Evidence**:
```json
{
  "dpia": [
    {
      "dpia_id": "DPIA-2026-01-15-001",
      "system": "Loan approval AI",
      "date": "2026-01-15",
      "risks": ["Data accuracy", "Bias", "Security"],
      "mitigations": ["Regular retraining", "Bias testing", "Encryption"],
      "approver": "DPO",
      "next_review": "2027-01-15"
    }
  ]
}
```

---

### D5: Cross-border data transfers

| Field | Value |
|-------|-------|
| **Check ID** | D5 |
| **Description** | Are cross-border transfers managed? |
| **JEP Evidence** | `data_transfer` logs |
| **Verification** | Check for transfer records |

**Sample Evidence**:
```json
{
  "data_transfer": [
    {
      "transfer_id": "XFER-2026-03-02-001",
      "destination": "Malaysia",
      "legal_basis": "Binding Corporate Rules",
      "data_categories": ["transaction_data"],
      "date": "2026-03-02",
      "approver": "DPO"
    }
  ]
}
```

---

## 🔷 Principle 8: Openness (O1-O4)

### O1: API documentation public

| Field | Value |
|-------|-------|
| **Check ID** | O1 |
| **Description** | Is API documentation public? |
| **JEP Evidence** | `api_docs_url` |
| **Verification** | Check for public documentation |

**Sample Evidence**:
```json
{
  "api_docs_url": "https://developer.dbs.com/docs",
  "api_version": "2.1",
  "last_updated": "2026-02-15",
  "formats": ["OpenAPI 3.0", "HTML", "PDF"]
}
```

---

### O2: Developer portal

| Field | Value |
|-------|-------|
| **Check ID** | O2 |
| **Description** | Is there a developer portal? |
| **JEP Evidence** | `developer_portal_url` |
| **Verification** | Check for developer portal |

**Sample Evidence**:
```json
{
  "developer_portal_url": "https://developer.dbs.com",
  "registered_developers": 1500,
  "apis_available": 25,
  "support_channels": ["Email", "Forum", "Stack Overflow"]
}
```

---

### O3: Third-party access

| Field | Value |
|-------|-------|
| **Check ID** | O3 |
| **Description** | Is third-party access available? |
| **JEP Evidence** | `third_party_access` logs |
| **Verification** | Check for third-party access records |

**Sample Evidence**:
```json
{
  "third_party_access": {
    "total_partners": 45,
    "active_integrations": 23,
    "access_requests": 67,
    "approval_rate": "85%",
    "average_onboarding_days": 14
  }
}
```

---

### O4: Open standards compliance

| Field | Value |
|-------|-------|
| **Check ID** | O4 |
| **Description** | Are open standards followed? |
| **JEP Evidence** | `standards_compliance` |
| **Verification** | Check for standards documentation |

**Sample Evidence**:
```json
{
  "standards_compliance": {
    "UUIDv7": "RFC 9562",
    "Ed25519": "RFC 8032",
    "JSON-LD": "W3C Recommendation",
    "OAuth 2.0": "RFC 6749",
    "OpenAPI": "3.0"
  }
}
```

---

## ✅ Verification Script

```bash
# Verify all 49 checks
python verify-aim-all.py --receipt-dir ./receipts/ --output report.json

# Verify specific principle
python verify-aim-principle.py --principle Accountability --receipt-dir ./receipts/

# Verify specific check
python verify-aim-check.py --check A1 --receipt-dir ./receipts/
```

## 📚 References

- [AIM Toolkit Official Documentation](https://www.ccs.gov.sg/aim-toolkit)
- [CCS Guidance on AI and Competition](https://www.ccs.gov.sg/ai-competition)
- [IMDA AI Governance Framework](https://www.imda.gov.sg/ai-governance)
```
