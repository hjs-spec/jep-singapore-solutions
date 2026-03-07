The **JEP AIM Toolkit Exporter** enables organizations to generate verifiable compliance evidence for the **AI Markets (AIM) Toolkit**, developed by the Competition and Consumer Commission of Singapore (CCS) in collaboration with IMDA.

This exporter helps businesses:
- **Self-assess** AI models against 49 process checks across 8 principles
- **Generate evidence** for competition and consumer protection compliance
- **Create audit trails** that can serve as mitigating factors in investigations
- **Export reports** in AIM Toolkit compatible format

## 🎯 Why This Matters

According to CCS, **"continuous and well-documented use of such tools could be taken into account as a mitigating factor"** in enforcement actions. JEP provides the cryptographic proof needed to demonstrate such "well-documented" compliance.

## 📊 AIM Toolkit 8 Principles

The AIM Toolkit covers 8 principles with 49 process checks:

| Principle | JEP Evidence | Export Format |
|-----------|--------------|---------------|
| **Accountability** | Complete responsibility chain with actor_id and signatures | `evidence.accountability` |
| **Transparency** | JSON-LD machine-readable metadata | `evidence.transparency` |
| **Accuracy** | Decision logs with model version and inputs | `evidence.accuracy` |
| **Fairness** | Extended fields for bias detection | `evidence.fairness` |
| **Pro-competitive Algorithms** | Algorithm change logs | `evidence.competition` |
| **Consumer Protection** | Consent and disclosure records | `evidence.consumer` |
| **Data Governance** | PII protection and consent tracking | `evidence.data_governance` |
| **Openness** | API documentation and access logs | `evidence.openness` |

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/hjs-spec/jep-singapore-solutions
cd jep-singapore-solutions/singapore/aim-toolkit

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from jep.aim_toolkit import AIMToolkitExporter

# Initialize exporter
exporter = AIMToolkitExporter(
    company_name="DBS Bank",
    company_uen="12345678A",
    contact_email="compliance@dbs.com"
)

# Generate AIM Toolkit submission
submission = exporter.generate_submission(
    start_date="2026-01-01",
    end_date="2026-03-01",
    principles=["accountability", "transparency", "fairness"],
    output_format="json"
)

# Save submission
submission.save("aim-toolkit-submission-q1-2026.json")
```

### One-Command Export

```bash
# Export all evidence for Q1 2026
python export-aim-report.py --period Q1-2026 --company "DBS Bank"

# Output saved to: aim-submission-dbs-q1-2026.json
```

## 🔍 49 Checks Mapping

The exporter maps JEP receipts to all 49 AIM Toolkit checks:

### Principle 1: Accountability (7 checks)

| Check ID | Description | JEP Evidence | Verification |
|----------|-------------|--------------|--------------|
| A1 | Clear allocation of responsibilities | `actor_id` in every receipt | [View mapping](49-checks-mapping.md#A1) |
| A2 | Governance framework documented | `governance` field in audit report | [View mapping](49-checks-mapping.md#A2) |
| A3 | Regular compliance reviews | `review_timestamp` in extended data | [View mapping](49-checks-mapping.md#A3) |
| A4 | ... (full list in mapping document) | ... | ... |

### Principle 2: Transparency (6 checks)

| Check ID | Description | JEP Evidence | Verification |
|----------|-------------|--------------|--------------|
| T1 | Clear disclosure of AI use | `is_ai_generated` field | [View mapping](49-checks-mapping.md#T1) |
| T2 | Explainable decisions | `reasoning` field | [View mapping](49-checks-mapping.md#T2) |
| T3 | ... | ... | ... |

## 📁 Report Format

```json
{
  "submission_id": "AIM-DBS-2026-Q1",
  "company": {
    "name": "DBS Bank",
    "uen": "12345678A",
    "contact": "compliance@dbs.com"
  },
  "period": {
    "start": "2026-01-01",
    "end": "2026-03-01"
  },
  "principles": [
    {
      "name": "Accountability",
      "checks": [
        {
          "id": "A1",
          "status": "COMPLIANT",
          "evidence": "100% of decisions have attributable actor_id",
          "receipts": ["jep_018e1234...", "jep_018e1235..."],
          "verification": "python verify-aim-check.py A1 --receipt-dir ./receipts/"
        }
      ],
      "overall": "COMPLIANT"
    }
  ],
  "mitigating_factors": [
    "Continuous audit trail maintained for all decisions",
    "Ed25519 signatures provide non-repudiable proof",
    "All high-risk decisions have human oversight"
  ],
  "signature": "ed25519:MCowBQYDK2VwAyEAv..."
}
```

## 🏛️ Legal Value: Mitigating Factor

According to CCS official guidance:

> "The use of AI governance tools, when properly documented and consistently applied, may be considered by CCS as a mitigating factor in assessing potential breaches of the Competition Act or Consumer Protection Act."

JEP provides:
- ✅ **Continuous documentation** - Every decision is recorded
- ✅ **Consistent application** - Same protocol applies to all decisions
- ✅ **Verifiable evidence** - Cryptographic signatures prove integrity
- ✅ **Independent audit** - Third parties can verify compliance

## 📚 Requirements

```
jep-protocol>=1.0.0
cryptography>=41.0.0
pydantic>=2.0.0
click>=8.0.0
pandas>=2.0.0
openpyxl>=3.1.0  # for Excel export
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](../../CONTRIBUTING.md).

## 📄 License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.

## 📬 Contact

- **Email**: singapore@humanjudgment.org
- **GitHub Issues**: [hjs-spec/jep-singapore-solutions/issues](https://github.com/hjs-spec/jep-singapore-solutions/issues)

---

*Part of the JEP Singapore Solutions 🇸🇬*
```
