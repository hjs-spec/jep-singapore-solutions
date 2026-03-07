# JEP for AI Verify - Accountability Testing Plugin

**A plugin for IMDA's AI Verify testing framework to automate accountability assessment**

## 📋 Overview

The **JEP Accountability Plugin** integrates the Judgment Event Protocol with IMDA's AI Verify testing framework, providing automated testing for the **Accountability** principle across all 11 AI governance principles.

This plugin enables:
- **Automated accountability testing** for AI models
- **Ed25519 signature verification** for non-repudiation
- **Human oversight checkpoint validation**
- **Audit trail completeness checks**
- **Compliance report generation** in AI Verify format

## 🎯 Why This Plugin?

AI Verify provides a comprehensive testing framework for 11 governance principles, but organizations need tools to implement and test **Accountability** in practice. This plugin fills that gap by:

| Challenge | Solution |
|-----------|----------|
| How to prove decisions are attributable? | JEP receipts with actor_id and signatures |
| How to verify human oversight? | `delegate()` primitive records human approvers |
| How to ensure audit trail completeness? | parent_hash chain creates immutable records |
| How to generate compliance evidence? | One-click report in AI Verify format |

## 🔧 Installation

### Prerequisites

- Python 3.8+
- AI Verify testing framework (v2.0+)
- JEP core library

### Install from Source

```bash
# Clone the repository
git clone https://github.com/hjs-spec/jep-singapore-solutions
cd jep-singapore-solutions/singapore/ai-verify

# Install dependencies
pip install -r requirements.txt
```

### Install via pip (coming soon)

```bash
pip install jep-ai-verify-plugin
```

## 🚀 Quick Start

### Step 1: Initialize the Plugin

```python
from jep.ai_verify import JEPAccountabilityPlugin

# Initialize with your AI Verify configuration
plugin = JEPAccountabilityPlugin(
    config_path="path/to/ai-verify-config.json",
    output_dir="./test-results"
)
```

### Step 2: Run Accountability Tests

```python
# Load your model and test dataset
model = load_your_model()
test_cases = load_test_cases()

# Run the accountability tests
results = plugin.run_tests(
    model=model,
    test_cases=test_cases,
    human_oversight_logs="./audit-logs/",
    include_signature_verification=True,
    include_chain_validation=True
)
```

### Step 3: Generate Report

```python
# Generate report in AI Verify format
report = plugin.generate_report(
    results=results,
    format="ai-verify",  # Options: ai-verify, json, html
    output_file="accountability-report.json"
)

print(f"Accountability Score: {report['score']}")
print(f"Compliance Status: {report['status']}")
```

## 📊 Test Coverage

The plugin tests the following accountability requirements:

| Test ID | Requirement | Method | Pass Condition |
|---------|-------------|--------|----------------|
| **ACC-01** | Decision Attribution | `test_attribution()` | Every decision has actor_id |
| **ACC-02** | Human Oversight | `test_human_oversight()` | High-risk decisions have human approver |
| **ACC-03** | Signature Validity | `test_signatures()` | All signatures verify with Ed25519 |
| **ACC-04** | Audit Trail | `test_audit_trail()` | Complete parent_hash chain |
| **ACC-05** | Non-Repudiation | `test_non_repudiation()` | Tampered receipts fail verification |
| **ACC-06** | Responsibility Chain | `test_responsibility_chain()` | Clear judge→delegate→execute flow |

## 🔍 Sample Output

```json
{
  "plugin": "JEP Accountability Plugin",
  "version": "1.0.0",
  "timestamp": "2026-03-07T10:30:00Z",
  "model_id": "dbs-loan-approval-v2",
  "overall_score": 0.98,
  "status": "COMPLIANT",
  "test_results": [
    {
      "test_id": "ACC-01",
      "name": "Decision Attribution",
      "passed": 100,
      "total": 100,
      "score": 1.0,
      "details": "All 100 decisions have valid actor_id"
    },
    {
      "test_id": "ACC-02",
      "name": "Human Oversight",
      "passed": 15,
      "total": 15,
      "score": 1.0,
      "details": "All 15 high-risk decisions have human approval"
    },
    {
      "test_id": "ACC-03",
      "name": "Signature Validity",
      "passed": 98,
      "total": 100,
      "score": 0.98,
      "details": "98/100 signatures verified correctly"
    }
  ],
  "evidence": {
    "receipts": ["jep_018e1234...", "jep_018e1235..."],
    "audit_chain": "complete",
    "verification_script": "verify_accountability.py"
  },
  "recommendations": [
    "Review the 2 failed signatures (possible data tampering)",
    "Ensure all future high-risk decisions include human approval"
  ]
}
```

## 🔗 Integration with AI Verify

### Running as Standalone Plugin

```bash
# Command line interface
python -m jep.ai_verify.run_tests \
    --model-path ./models/loan-model.pkl \
    --test-cases ./data/test-cases.json \
    --output ./reports/
```

### Integration with AI Verify Pipeline

```python
# In your AI Verify pipeline configuration
{
  "plugins": [
    {
      "name": "jep-accountability",
      "module": "jep.ai_verify",
      "config": {
        "verify_signatures": true,
        "require_human_oversight": true,
        "risk_threshold": "HIGH"
      }
    }
  ]
}
```

## 📁 Plugin Structure

```
jep-ai-verify-plugin/
├── __init__.py              # Plugin initialization
├── core/
│   ├── accountability.py    # Core test logic
│   ├── signature.py         # Ed25519 verification
│   └── chain.py             # Audit chain validation
├── adapters/
│   ├── ai_verify.py         # AI Verify integration
│   └── models.py            # Model adapters
├── reports/
│   ├── generator.py         # Report generation
│   └── templates/           # Report templates
├── tests/                   # Unit tests
└── examples/                # Usage examples
```

## 📚 Requirements

```
jep-protocol>=1.0.0
cryptography>=41.0.0
pydantic>=2.0.0
click>=8.0.0  # for CLI
pandas>=2.0.0 # for data handling
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
