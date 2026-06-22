# PileUp — Task List

Phase 1 only. No UI, no cloud, no auth, no conversation memory.
Each task is ~1–2 hours, self-contained, and testable independently.

---

## Group 1 — Project Setup

**Task 1 — Initialize project structure**
- Create the folder layout: `src/`, `data/raw/`, `data/processed/`, `tests/`
- Initialize the project with `uv init`
- Add a `.env.example` file with a placeholder for `ANTHROPIC_API_KEY`
- Add a `.gitignore` that excludes `.env`, `data/`, and ChromaDB storage
- No dependencies yet
- ✅ Done when: folders exist, `uv run python --version` works

**Task 2 — Add dependencies**
- Add to `pyproject.toml`: `chromadb`, `anthropic`, `python-dotenv`
- Install with `uv sync`
- ✅ Done when: `uv run python -c "import chromadb, anthropic"` runs without error

**Task 3 — Create a sample input file**
- Write a realistic `.txt` file and place it in `data/raw/`
- Should contain a few paragraphs of travel research (restaurants, tips, places)
- This will be the test data for every step
- ✅ Done when: `data/raw/sample.txt` exists with readable content

---

## Group 2 — Pipeline Step 1: Clean

**Task 4 — Write `src/clean.py`**
- Depends on: Task 1, Task 2
- Write a function `clean_text(raw: str) -> str`
- It should: strip leading/trailing whitespace, remove repeated blank lines, fix common encoding issues (e.g. `â€™` → `'`), remove lines that are only punctuation or symbols
- ✅ Done when: function returns a visibly cleaner version of messy text

**Task 5 — Write `tests/test_clean.py`**
- Depends on: Task 4
- Test with at least 3 cases: already-clean text, text with extra whitespace, text with encoding issues
- ✅ Done when: `uv run pytest tests/test_clean.py` passes

---

## Group 3 — Pipeline Step 2: Chunk

**Task 6 — Write `src/chunk.py`**
- Depends on: Task 4
- Write a function `chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]`
- Split text into chunks of ~500 words with ~50-word overlap between consecutive chunks
- ✅ Done when: a 2000-word input returns ~5 chunks, each around 500 words, with visible overlap at the boundaries

**Task 7 — Write `tests/test_chunk.py`**
- Depends on: Task 6
- Test: short text (less than one chunk), normal text, chunk size and overlap boundaries
- ✅ Done when: `uv run pytest tests/test_chunk.py` passes

---

## Group 4 — Pipeline Step 3: Embed

**Task 8 — Write `src/embed.py`**
- Depends on: Task 6
- Write a function `embed_chunks(chunks: list[str]) -> list[dict]`
- Use ChromaDB's built-in embedding model (`all-MiniLM-L6-v2`) to embed each chunk
- Return a list of dicts: `{"text": "...", "embedding": [...], "id": "chunk_0"}`
- ✅ Done when: function returns a list where each item has a non-empty `embedding` field (a list of floats)

**Task 9 — Write `tests/test_embed.py`**
- Depends on: Task 8
- Test: embedding 3 short chunks returns 3 items, each with an embedding of consistent length
- ✅ Done when: `uv run pytest tests/test_embed.py` passes

---

## Group 5 — Pipeline Step 4: Store

**Task 10 — Write `src/store.py`**
- Depends on: Task 8
- Write a function `store_chunks(embedded_chunks: list[dict], collection_name: str = "pileup") -> None`
- Initialize a local ChromaDB client (persisted to `data/chroma/`)
- Create or get a collection, then add all chunks with their embeddings and IDs
- ✅ Done when: after running the function, a `data/chroma/` folder exists and re-running does not crash (handles duplicate IDs)

**Task 11 — Write `tests/test_store.py`**
- Depends on: Task 10
- Use a temporary ChromaDB directory so tests don't pollute real data
- Test: store 3 chunks, then verify the collection count equals 3
- ✅ Done when: `uv run pytest tests/test_store.py` passes

---

## Group 6 — Pipeline Step 5: Retrieve

**Task 12 — Write `src/retrieve.py`**
- Depends on: Task 10
- Write a function `retrieve_chunks(query: str, collection_name: str = "pileup", top_k: int = 5) -> list[str]`
- Connect to the existing ChromaDB collection
- Run a similarity search with the query and return the top-K matching text chunks
- ✅ Done when: a question about the sample data returns chunks that visibly relate to the question

**Task 13 — Write `tests/test_retrieve.py`**
- Depends on: Task 12
- Store a few known chunks, then query with a related question and assert the most relevant chunk appears in the results
- ✅ Done when: `uv run pytest tests/test_retrieve.py` passes

---

## Group 7 — Pipeline Step 6: Answer

**Task 14 — Write `src/answer.py`**
- Depends on: Task 2 (Anthropic SDK), Task 12
- Write a function `answer_question(question: str, context_chunks: list[str]) -> str`
- Build a prompt that includes the question and the retrieved chunks as context
- Call the Claude API and return the response text
- The prompt must instruct Claude to answer only from the provided context, not general knowledge
- ✅ Done when: function returns a readable answer string when called with a real question and chunks

**Task 15 — Write `tests/test_answer.py`**
- Depends on: Task 14
- Mock the Anthropic API call (do not make real API calls in tests)
- Test: correct prompt structure is built, function returns the mocked response string
- ✅ Done when: `uv run pytest tests/test_answer.py` passes without hitting the API

---

## Group 8 — Orchestration

**Task 16 — Write `src/ingest.py`**
- Depends on: Tasks 4, 6, 8, 10
- Write a script that:
  1. Reads all `.txt` files from `data/raw/`
  2. For each file: clean → chunk → embed → store
  3. Prints progress to the terminal (e.g. "Processing sample.txt… done. 12 chunks stored.")
- ✅ Done when: `uv run python src/ingest.py` processes `data/raw/sample.txt` and populates ChromaDB

**Task 17 — Write `src/query.py`**
- Depends on: Tasks 12, 14
- Write a CLI script that:
  1. Accepts a question as a command-line argument
  2. Runs retrieve → answer
  3. Prints the answer to the terminal
- ✅ Done when: `uv run python src/query.py "What restaurants did I save?"` returns a relevant answer

---

## Group 9 — End-to-End Validation

**Task 18 — Full pipeline test**
- Depends on: Tasks 16, 17
- Run the complete flow from scratch:
  1. Delete `data/chroma/` to start clean
  2. Run `uv run python src/ingest.py`
  3. Run `uv run python src/query.py "..."` with 3 different questions
- Verify: answers are grounded in the sample file content, not generic
- ✅ Done when: all 3 questions return relevant, specific answers from the data
