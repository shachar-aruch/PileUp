# PileUp

A local RAG (Retrieval-Augmented Generation) pipeline that lets the user query their personally collected research using natural language. The user drops `.txt` files into `data/raw/`, runs the pipeline, then asks questions — the system answers using only the provided data.

## Learning Goal

This project is primarily a learning project. The goal is not just to ship working code — it is to deeply understand every part of the system, end to end, well enough to explain it to a coworker and rebuild it independently.

**How to approach every conversation:**
- Explain what we are building before writing code, not after
- When introducing a concept (RAG, embeddings, vector search, chunking, etc.), explain it in plain terms first — using analogies to data pipelines and ETL when helpful
- After writing code, walk through what it does and why each design decision was made
- Encourage questions — if something is unclear, slow down and go deeper
- Prefer building incrementally: one step at a time, test it, understand it, then move on
- Do not abstract or over-engineer — keep code readable and explicit so it is easier to learn from

**User background:**
- Junior software developer, CS degree
- 1.5 years as a Data Engineer — Python, SQL, ETL pipelines, ingestion, databases
- Comfortable with data flow and pipeline thinking
- New to AI/ML systems — this project is the entry point
- Goal: grow toward building AI backend systems

## Stack

- Python 3.11
- Package manager: `uv`
- LLM: Claude API (Anthropic)
- Vector DB: ChromaDB (local, no infrastructure)
- Embeddings: ChromaDB built-in (`all-MiniLM-L6-v2`)

## Commands

- Install deps: `uv sync`
- Run pipeline (ingest): `uv run python src/ingest.py`
- Ask a question: `uv run python src/query.py "your question here"`
- Run tests: `uv run pytest`

## Project Structure

```
data/
  raw/          ← user drops .txt files here
  processed/    ← cleaned output (generated)
src/
  clean.py      ← Step 1: remove noise, fix encoding
  chunk.py      ← Step 2: split into ~500-word overlapping chunks
  embed.py      ← Step 3: embed chunks into vectors
  store.py      ← Step 4: persist to ChromaDB
  retrieve.py   ← Step 5: find relevant chunks for a query
  query.py      ← Step 6: send question + chunks to Claude, return answer
  ingest.py     ← orchestrates Steps 1–4
```

## Pipeline

```
Input (.txt files in data/raw/)
  → Clean → Chunk → Embed → Store (ChromaDB)
  → User question → Retrieve → Answer via Claude API
```

Each step can be run and tested independently.

## Conventions

- Each pipeline step lives in its own module (`clean.py`, `chunk.py`, etc.)
- Functions should be pure where possible — take input, return output, no side effects
- The answer must be grounded in the provided data only — never supplement with general knowledge from Claude
- Chunk size: ~500 words with overlap

## Phase 1 Constraints — Do Not Add

- No web UI or chat interface
- No URL, PDF, or WhatsApp ingestion
- No conversation memory (each question is independent)
- No user auth
- No cloud deployment
