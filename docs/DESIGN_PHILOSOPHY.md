# Design Philosophy: JEP as a Structured Language for Accountability

**Version 1.0 | 2026-03-08**

JEP is not another AI governance tool. It is a **structured language** designed from first principles to enable any AI system, in any jurisdiction, under any regulatory framework, to answer one question: **Who is responsible?**

This document explains the foundational choices that make this possible.

---

## 1. The Four Primitives — The Complete Grammar

Every human language has verbs to express action. JEP has four verbs to express responsibility:

| Primitive | Function | Human Analogy | Legal Analogy |
|-----------|----------|---------------|---------------|
| **`judge`** | Establish initial accountability | "I take responsibility" | Original jurisdiction |
| **`delegate`** | Transfer responsibility to another agent | "I authorize you to act on my behalf" | Agency law, delegation |
| **`terminate`** | Conclude accountability | "My responsibility ends here" | Statute of limitations |
| **`verify`** | Independently attest to the record | "Let me check the signature" | Notarization, audit |

### Why These Four?

These four primitives cover the **complete lifecycle of responsibility**:

```mermaid
graph LR
    A[Judge: Begin] --> B[Delegate: Transfer]
    B --> C[Delegate: Transfer]
    C --> D[Terminate: End]
    D --> E[Verify: Prove]
```

- **Judge** creates responsibility
- **Delegate** moves it across systems or agents
- **Terminate** ends it
- **Verify** proves the entire chain

No more, no less. Any accountability scenario — from a simple AI decision to a complex multi-agent workflow — can be expressed using these four verbs.

### Example: Cross-Border Loan Approval

```
judge(DeutscheBankAI, {version: "2.1", authority: "loan-approval"})
    → delegate(AxaAI, {purpose: "credit-check"})
    → delegate(EquifaxAPI, {purpose: "data-retrieval"})
    → terminate(ItalianOfficer, {decision: "deny"})
```

This single chain tells the complete story:
- **Who started it**: Deutsche Bank AI
- **Who it passed through**: Axa AI → Equifax
- **Who ended it**: Italian compliance officer

---

## 2. Cryptographic Trust — The Ink of the Language

A language is useless if its words can be forged. JEP uses two cryptographic primitives to ensure every "sentence" is authentic and tamper-proof.

### 2.1 Ed25519 Signatures — Non-Repudiation

Every judgment event is signed with **Ed25519 (RFC 8032)** — the same algorithm used in modern secure systems like SSH, Tor, and blockchain.

This provides:
- **Authenticity**: You know exactly who issued the judgment
- **Non-repudiation**: The signer cannot deny having issued it
- **Integrity**: Any modification breaks the signature

```python
# Any tampering is immediately detectable
original = {"status": "APPROVED", "receipt_id": "jep_..."}
signature = ed25519.sign(original)

tampered = {"status": "DENIED", "receipt_id": "jep_..."}
assert ed25519.verify(tampered, signature) == False  # Fails immediately
```

### 2.2 UUIDv7 — Temporal Order

Every receipt includes a **UUIDv7 (RFC 9562)**, which encodes both:

```
jep_0195f6d8-1234-7123-8abc-9def01234567
           └─┬──┘
         version 7 = timestamp-based
```

- **Uniqueness**: No two receipts are the same
- **Temporal order**: The timestamp is built into the ID

This enables:
- **Millisecond-level sorting** without separate indexes
- **Billion-scale audit retrieval** in real time
- **No central clock synchronization needed**

### 2.3 Future-Proof by Design

Critically, JEP's cryptographic design is **algorithm-agnostic**:

```json
{
  "receipt_id": "jep_0195f6d8-1234-7123-8abc-9def01234567",
  "alg": "Ed25519",        // Algorithm explicitly identified
  "signature": "0x7a8b9c...",
  "payload": {...}
}
```

The `alg` field allows the protocol to evolve with technology:

| Era | Algorithm | JEP Support |
|-----|-----------|--------------|
| Today | Ed25519 | ✅ Native |
| Near future | Post-quantum candidates | ✅ Via `alg` field |
| Any future | New national standards | ✅ Algorithm identifier ready |

**The same principle applies to hash algorithms and protocol versions.** JEP is designed to evolve with technology, not be locked into today's choices.

---

## 3. Structured for Maximum Compatibility

Because JEP is a **language** (not a platform), it achieves maximum compatibility through structured design.

### 3.1 Model-Agnostic

JEP operates as a **transparent proxy** between AI applications and their users. It requires **zero modification** to any AI model:

| Model | Support | Modification Required |
|-------|---------|----------------------|
| GPT-4 / GPT-5 | ✅ | None |
| Llama 3 / Llama 4 | ✅ | None |
| Claude | ✅ | None |
| Mistral | ✅ | None |
| Custom models | ✅ | None |

### 3.2 Jurisdiction-Agnostic

JEP's **sidecar architecture** can be deployed anywhere:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Model      │     │   JEP Sidecar   │     │   Audit Layer   │
│  (any cloud)    │ ←→ │ (local/sovereign)│ ←→ │  (public hashes)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

- ✅ On-premises
- ✅ Sovereign cloud
- ✅ Hybrid
- ✅ Air-gapped environments

### 3.3 Framework-Agnostic

The same structured output maps to any regulatory framework:

| Framework | JEP Implementation |
|-----------|-------------------|

|  **Singapore Agentic Framework** | [`jep-singapore-solutions`](https://github.com/hjs-spec/jep-singapore-solutions) |
|  **Asean Agentic Framework** | [`jep-Asean-solutions`](https://github.com/hjs-spec/jep-asean-solutions) |
|  **Korea AI Basic Act** | [`jep-kr-solutions`](https://github.com/hjs-spec/jep-kr-solutions-) |

**Proof**: The same protocol serves three完全不同 frameworks without modification.

---

## 4. Governed for Neutrality

A language cannot be owned by any single company. JEP is governed by:

### HJS Foundation LTD (Singapore) — Non-profit CLG

| Governance Feature | Implementation |
|-------------------|----------------|
| **Legal Form** | Company Limited by Guarantee (non-profit) |
| **Shareholders** | ❌ None |
| **Profit Distribution** | ❌ Prohibited by constitution |
| **Asset Lock** | ✅ Core IP cannot be sold or transferred |
| **Independent Directors** | ✅ 1/3 from academic/policy/industry |

### Multi-Stakeholder Representation

The foundation's governance includes voices from:

- **Technical experts** — Ensure protocol integrity
- **Privacy advocates** — Protect individual rights
- **Legal scholars** — Maintain regulatory alignment
- **Industry representatives** — Ensure practical utility

See full details: [`GOVERNANCE_CHARTER.md`](GOVERNANCE_CHARTER.md)

---

## 5. Summary: The Complete Picture

| Design Choice | What It Enables |
|---------------|-----------------|
| **Four primitives** | Complete grammar for any accountability scenario |
| **Ed25519 signatures** | Non-repudiation, tamper-proof evidence |
| **UUIDv7** | Temporal ordering, billion-scale audit |
| **Algorithm-agnostic** | Future-proof, quantum-resistant |
| **Model-agnostic** | Zero modification to existing AI |
| **Jurisdiction-agnostic** | Deploy anywhere, sovereignty respected |
| **Framework-agnostic** | One language, multiple regulations |
| **Non-profit governance** | Neutral, public-interest steward |

---

## 6. References

- [JEP IETF Draft](https://datatracker.ietf.org/doc/draft-wang-hjs-judgment-event/)
- [RFC 8032: Ed25519](https://datatracker.ietf.org/doc/html/rfc8032)
- [RFC 9562: UUIDv7](https://datatracker.ietf.org/doc/html/rfc9562)
- [JSON-LD W3C Standard](https://www.w3.org/TR/json-ld11/)

---

**Document History**
- 2026-03-08: Initial version for EUSAiR submission

*This design philosophy is implemented in all JEP code and documentation. Every design choice is reflected in the protocol.*
```

---

## 📄 在 `README.md` 增加入口

在合适位置（比如在“1. Regulatory Compliance Matrix”之前）增加：

```markdown
## 📚 Design Philosophy

Before diving into the technical details, we encourage you to read our **[Design Philosophy](docs/DESIGN_PHILOSOPHY.md)** — it explains the foundational choices behind JEP:

- **Four primitives** — Why `judge`/`delegate`/`terminate`/`verify` are the complete grammar of accountability
- **Cryptographic trust** — How Ed25519 + UUIDv7 make evidence tamper-proof and future-proof
- **Maximum compatibility** — How one language serves multiple models, jurisdictions, and frameworks
- **Neutral governance** — Why a non-profit foundation with 1/3 independent directors ensures long-term neutrality

[➡️ Read the Design Philosophy](docs/DESIGN_PHILOSOPHY.md)
```
