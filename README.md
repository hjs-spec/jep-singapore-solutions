# 🇸🇬 JEP Singapore Solutions

**Turning Singapore's AI Governance Frameworks into Verifiable Code**

## 📋 Overview

This repository provides complete **Judgment Event Protocol (JEP)** implementations aligned with Singapore's three flagship AI governance frameworks. It helps organizations meet regulatory requirements with minimal technical overhead.

### 🎯 Covered Singapore Frameworks

| Framework | Issuer | JEP Solution |
|------|----------|-------------|
| **Model AI Governance Framework for Agentic AI (2026)** | IMDA | [Agentic AI Accountability Implementation →](/singapore/agentic-framework/README.md) |
| **AI Verify Testing Framework** | IMDA | [AI Verify Accountability Plugin →](/singapore/ai-verify/README.md) |
| **AIM Toolkit (Competition & Consumer Protection)** | CCS + IMDA | [AIM Toolkit Evidence Export →](/singapore/aim-toolkit/README.md) |

## 📚 Design Philosophy

Before diving into the technical details, we encourage you to read our **[Design Philosophy](docs/DESIGN_PHILOSOPHY.md)** — it explains the foundational choices behind JEP:

- **Four primitives** — Why `judge`/`delegate`/`terminate`/`verify` are the complete grammar of accountability
- **Cryptographic trust** — How Ed25519 + UUIDv7 make evidence tamper-proof and future-proof
- **Maximum compatibility** — How one language serves multiple models, jurisdictions, and frameworks
- **Neutral governance** — Why a non-profit foundation with 1/3 independent directors ensures long-term neutrality

[➡️ Read the Design Philosophy](docs/DESIGN_PHILOSOPHY.md)

## 🔍 Why JEP?

✅ **Singapore-born**: Stewarded by HJS Foundation LTD, a Singapore-registered non-profit CLG  
✅ **Cryptographic Guarantees**: Ed25519 signatures ensure non-repudiation and tamper-proof evidence  
✅ **Lightweight Integration**: 3 lines of code, <1ms performance impact  
✅ **Open Source**: Apache 2.0 license, community-driven  
✅ **Permanent Asset Lock**: Core assets (trademarks, domains, copyrights) cannot be sold or transferred  

## 🏢 Singapore Industry Use Cases

| Industry | Regulator | Example Scenario | Solution |
|------|----------|----------|----------|
| Financial Services | MAS | DBS Bank loan approval AI | [View →](https://github.com/hjs-spec/jep-singapore-solutions/blob/main/examples/financial-services.py) |
| Healthcare | MOH | Singapore General Hospital diagnostic AI | [View →](https://github.com/hjs-spec/jep-singapore-solutions/blob/main/framework-agentic/examples/healthcare.py) |
| Public Sector | GovTech | CPF advisory AI assistant | [View →](https://github.com/hjs-spec/jep-singapore-solutions/blob/main/framework-agentic/examples/public-sector.py) |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/hjs-spec/jep-singapore-solutions
cd jep-singapore-solutions

# Install JEP core library
pip install jep-protocol

# Run Singapore framework verification
python singapore/agentic-framework/tests/verify-all-pillars.py
```

## 🏛️ Governance

JEP is stewarded by **HJS Foundation LTD** (Singapore CLG), a non-profit organization with permanent asset lock. The foundation's constitution explicitly prohibits:

- Distribution of profits to members (Article 7B)
- Transfer or sale of core assets (trademarks, domains, copyrights) (Article 67A)
- Private distribution of assets upon dissolution (Article 68)

**Registered Address**: 101 Thomson Road #28-03A, United Square, Singapore 307591

## 📊 Framework Alignment Summary

| Framework | Core Requirement | JEP Feature | Verification |
|-----------|-----------------|-------------|--------------|
| **Agentic AI Framework** | Meaningful human oversight | `delegate()` primitive + Ed25519 signature | [verify-agentic.py](/singapore/agentic-framework/tests/verify-all-pillars.py) |
| **AI Verify** | Accountability principle | Four primitives + audit chain | [verify-ai-verify.py](/singapore/ai-verify/accountability-plugin.py) |
| **AIM Toolkit** | 49 accountability checks | Complete responsibility records | [verify-aim.py](/singapore/aim-toolkit/export-script.py) |

## 📬 Contact

- **Email**: singapore@humanjudgment.org
- **GitHub**: [hjs-spec/jep-singapore-solutions](https://github.com/hjs-spec/jep-singapore-solutions)
- **Foundation**: HJS Foundation LTD (Singapore CLG)

## 📁 Repository Structure

```
jep-singapore-solutions/
├── README.md                           # This file
├── singapore/                           # Singapore solutions root
│   ├── agentic-framework/                # Agentic AI Framework (2026)
│   │   ├── README.md                     # Solution overview
│   │   ├── mapping.md                     # Detailed mapping to framework
│   │   ├── implementation/                 # Core implementation
│   │   │   └── accountability.py          # Accountability implementation
│   │   ├── examples/                       # Industry use cases
│   │   │   ├── financial-services.py
│   │   │   ├── healthcare.py
│   │   │   ├── public-sector.py
│   │   │   ├── cpf-integration.py
│   │   │   ├── iras-integration.py
│   │   │   └── smart-nation-integration.py
│   │   └── tests/                          # Verification scripts
│   │       ├── verify-all-pillars.py
│   │       ├── verify-mas-compliance.py
│   │       ├── verify-moh-compliance.py
│   │       └── verify-govtech-compliance.py
│   ├── ai-verify/                         # AI Verify Framework
│   │   ├── README.md                      # Solution overview
│   │   ├── accountability-plugin.py        # AI Verify plugin
│   │   └── sample-report.json              # Report format
│   └── aim-toolkit/                       # AIM Toolkit
│       ├── README.md                       # Solution overview
│       ├── 49-checks-mapping.md             # 49 checks alignment
│       └── export-script.py                  # AIM report export
```

---

*Designed for Singapore 🇸🇬, for the world 🌏*
