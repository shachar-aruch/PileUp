# PileUp — Product Requirements Document

**Version:** 1.0  
**Author:** Shachar Aharon  
**Status:** Draft

---

## 1. The Problem

When planning a trip, a lot of valuable information gets collected from many
sources — Facebook posts, blog URLs, personal recommendations, notes. This
information ends up scattered in a "pile" (a WhatsApp group, a notes app, etc.).

When it's time to actually plan, the user can't remember everything they saved.
They go back and re-read everything — doing the same work twice. They already
decided this information was worth saving, so why read it again?

The current workaround is manually copying and pasting relevant pieces into
ChatGPT to ask questions. This works but is slow, manual, and messy —
the raw data has noise, duplicates, and unnecessary context.

---

## 2. The Solution

A local RAG (Retrieval-Augmented Generation) pipeline that:

1. Takes knowledge the user has already collected
2. Cleans and organizes it automatically
3. Answers questions using only that personal knowledge as context

The user provides their collected data. The system makes it queryable.

---

## 3. Who Is This For

- **Primary user:** Shachar — a person planning a trip who has already
  collected research and wants to query it naturally
- **Phase 1 scope:** Single user, local tool, no UI

---

## 4. How It Works (The Pipeline)

```
Input (.txt files)
      ↓
  Step 1 — Clean      Remove noise, fix encoding, strip irrelevant content
      ↓
  Step 2 — Chunk      Split text into small overlapping pieces (~500 words)
      ↓
  Step 3 — Embed      Convert each chunk into a vector (list of numbers
                      that represent meaning)
      ↓
  Step 4 — Store      Save vectors + original text into ChromaDB
      ↓
  User asks question
      ↓
  Step 5 — Retrieve   Find the most relevant chunks from ChromaDB
      ↓
  Step 6 — Answer     Send question + relevant chunks to Claude API
                      and return the answer
```

---

## 5. Inputs and Outputs

| | Description |
|---|---|
| **Input (Phase 1)** | `.txt` files placed in `data/raw/` |
| **Query** | A natural language question typed by the user |
| **Output** | A plain text answer grounded in the collected knowledge |

---

## 6. Technical Decisions

| Decision | Choice | Why |
|---|---|---|
| Language | Python 3.11 | Standard for data/AI work |
| Package manager | uv | Faster than pip, modern standard |
| LLM | Claude API (Anthropic) | Large context window, clean SDK, already in use |
| Vector DB | ChromaDB | Runs locally, zero infrastructure, good for learning |
| Embeddings | ChromaDB built-in (`all-MiniLM-L6-v2`) | No extra setup needed for Phase 1 |

---

## 7. What Is Out of Scope (Phase 1)

- No web UI or chat interface
- No ingestion from URLs, PDFs, or WhatsApp exports (Phase 2+)
- No user authentication
- No cloud deployment
- No conversation memory (each question is independent)

---

## 8. Future Phases (Do Not Build Now)

- **Phase 2:** Accept more input types — URLs, PDFs, WhatsApp exports
- **Phase 3:** Simple chat UI (web or CLI with history)
- **Phase 4:** Swap ChromaDB for pgvector on Postgres for production scale

---

## 9. Success Criteria for Phase 1

- [ ] A `.txt` file placed in `data/raw/` gets processed end-to-end
- [ ] The user can type a question and get a relevant answer
- [ ] The answer is grounded only in the provided data (no hallucination
      from general knowledge)
- [ ] Each step of the pipeline can be run and tested independently