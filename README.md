# AI Release Risk Assistant

**An evidence-grounded AI engineering prototype for software release risk analysis and governance.**

## Overview

The AI Release Risk Assistant explores how Generative AI and retrieval techniques can help Quality Engineering teams analyze release documentation, identify documented risks, retrieve supporting evidence, and surface potential governance conflicts.

Rather than allowing an LLM to make the release decision independently, the prototype combines AI-assisted evidence processing with deterministic rules for risk and governance assessment.

> **Project status:** Engineering prototype for learning, experimentation, and demonstration. It is not a production release-approval system.

## Problem Statement

Release decisions may depend on information distributed across production reports, security findings, incident records, recommendations, and approval statements.

Finding and correlating this information manually can be time-consuming. An AI-assisted system can help users ask targeted questions and retrieve relevant information from release documents.

## Key Capabilities

- **Question-driven analysis:** Ask questions about a specific release or information across indexed releases.
- **Semantic retrieval:** Search release evidence using vector representations.
- **Parent-child retrieval:** Retrieve relevant smaller chunks and use their parent documents to restore context.
- **Semantic reranking:** Use a ready-made Cross-Encoder to rerank retrieved candidates.
- **Evidence extraction:** Use an LLM to extract factual statements from retrieved context.
- **Evidence validation:** Check extracted statements against their source text.
- **Evidence classification:** Categorize evidence, including risks, impacts, recommendations, resolutions, and approvals.
- **Deterministic governance rules:** Assess documented risks, recommendations, approvals, and conflicting evidence.
- **Structured reporting:** Present answers, supporting evidence, risk status, governance status, and evidence gaps.
- **Retrieval evaluation:** Compare retrieval approaches using a golden dataset and retrieval metrics.

## Architecture

```text
Release Documents
       |
       v
Document Chunking
       |
       v
Nomic Embeddings
       |
       v
ChromaDB Vector Retrieval
       |
       v
Parent-Child Context Retrieval
       |
       v
Cross-Encoder Reranking
       |
       v
Qwen Evidence Extraction
       |
       v
Evidence Validation
       |
       v
Evidence Classification
       |
       v
Deterministic Risk and
Governance Assessment
       |
       v
Grounded Answer and Report
       |
       v
Human Review and Sign-off
```

## Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming language | Python | Application orchestration and business rules |
| Local LLM runtime | Ollama | Running the language model locally |
| Language model | Qwen 2.5 1.5B | Evidence extraction |
| Embedding model | Nomic Embed Text | Generating semantic embeddings |
| Vector database | ChromaDB | Persistent vector storage and retrieval |
| Reranking | Cross-Encoder | Reranking retrieved candidates |
| Evaluation | Python and a golden dataset | Measuring retrieval performance |

## Design Principles

### 1. Evidence before conclusions

Answers should be grounded in retrieved source material. Unsupported claims should not be treated as established facts.

### 2. AI-assisted analysis, deterministic governance

AI supports semantic retrieval, reranking, and evidence extraction. Deterministic application rules assess the evidence and derive the prototype's risk and governance statuses.

### 3. Conflicts must remain visible

A documented deployment approval does not erase a documented security recommendation to block deployment. Conflicting evidence should be surfaced for human review.

### 4. Evaluate, do not assume

Retrieval methods must be evaluated against known expected evidence. Adding more retrieval components does not guarantee better results.

### 5. Human oversight

The prototype supports analysis; it does not replace accountable release-management or security approval.

## Example Scenario

Consider a release report containing these statements:

- A critical authentication vulnerability was identified.
- Security recommended blocking deployment.
- The Release Manager approved deployment.

The assistant can extract these statements and the deterministic governance rules can identify the conflict between the documented approval and the security recommendation.

The purpose is to make the evidence and conflict visible—not to treat an LLM-generated opinion as the final release decision.

## Evaluation

The project includes a retrieval evaluation dataset at `data/golden_dataset.json`.

Initial experimental results:

| Retrieval approach | Precision@3 | Recall@3 | MRR |
|---|---:|---:|---:|
| Chroma baseline | 0.33 | 0.80 | 0.40 |
| Hybrid retrieval | 0.33 | 0.80 | 0.40 |
| Hybrid + Cross-Encoder | 0.33 | 0.80 | 0.43 |

These are results from the current small evaluation dataset, not general performance guarantees. The experiments show that adding retrieval components does not necessarily improve every metric.

## Project Structure

```text
AI-Release-Risk-Assistant/
├── data/
│   ├── golden_dataset.json
│   ├── release_527.txt
│   ├── release_528.txt
│   ├── release_529.txt
│   └── release_530.txt
├── src/
│   ├── release_risk_analysis.py
│   ├── chroma_search.py
│   ├── parent_child_retrieval.py
│   ├── reranker.py
│   ├── evidence_extractor.py
│   ├── evidence_validator.py
│   ├── evidence_classifier.py
│   ├── evidence_selector.py
│   ├── release_readiness.py
│   ├── answer_formatter.py
│   └── final_report.py
└── README.md
```

## Current Limitations

- This is a prototype, not a production-grade release governance platform.
- Retrieval quality depends on document content, chunking, embeddings, and ranking.
- The evaluation dataset is small and needs to grow to cover more question types and edge cases.
- Evidence extraction and validation require further testing against incomplete, ambiguous, and contradictory source material.
- Cross-release historical questions must be kept separate from release-specific readiness decisions.
- Human review remains necessary for consequential release decisions.

## Future Improvements

- Expand the golden evaluation dataset and automate regression evaluation.
- Improve cross-release question handling and evidence attribution.
- Add stronger evidence completeness and source-traceability controls.
- Evaluate retrieval and answer faithfulness across more release scenarios.
- Add a demonstration interface and audit-friendly evidence views.
- Strengthen test coverage for missing documents, empty documents, and conflicting evidence.

## Author

**Shyam Vittal**  
Quality Engineering | Software Testing | AI-assisted Quality Engineering

---

*Built as a hands-on exploration of how AI engineering and Quality Engineering principles can work together to support evidence-based release analysis.*