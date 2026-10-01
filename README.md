# Self-RAG

A Self-RAG system built from scratch using **LangGraph**, **Hybrid RAG**, and an **LLM-based grounding grader**.

The system retrieves relevant information from a document, generates an answer, checks whether the answer is supported by the retrieved context, and retries retrieval when the answer is not grounded.

---

## Architecture

```text
START
  │
  ▼
Retrieval
(Hybrid RAG)
  │
  ▼
LLM
(Answer Generation)
  │
  ▼
Grader
(Grounded?)
  │
  ├── True ──► END
  │
  └── False ─► Retrieval
                  │
                  └──► LLM
```

---

## Project Structure

```text
Self-RAG/
│
├── Code/
│   ├── backend.py
│   ├── RAG.py
│   ├── Graph.py
│   ├── grader.py
│   ├── State_connection.py
│   ├── LLM.py
│   └── texting.py
│
├── VectorDB/
│
├── economics_research_reference.pdf
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Components

### `backend.py`

Handles document processing and database setup.

* PDF loading
* Text splitting
* Chunk creation
* Metadata extraction
* Document IDs
* ChromaDB
* BM25 corpus

### `RAG.py`

Contains the Hybrid RAG retrieval system.

It combines:

* Dense retrieval using ChromaDB
* Keyword retrieval using BM25
* Reciprocal Rank Fusion (RRF)

The final retrieved documents are stored in:

```python
context: list[str]
```

### `State_connection.py`

Defines the LangGraph state.

```python
class State(TypedDict):
    query: str
    context: list[str]
    answer: str
    grounded: bool
```

### `LLM.py`

Contains the LLM configuration used for:

* Answer generation
* Grading

### `grader.py`

Checks whether the generated answer is supported by the retrieved context.

The grader uses structured output:

```python
class Grade(BaseModel):
    grounded: bool
```

The result controls the LangGraph routing.

```text
grounded = True
       ↓
      END

grounded = False
       ↓
   Retrieval
```

### `Graph.py`

Builds the LangGraph workflow.

Main nodes:

```text
retrieval
    ↓
llm
    ↓
grader
```

Conditional routing is used after the grader.

### `texting.py`

Used to run and test the complete Self-RAG graph.

---

## State Flow

The state moves through the graph like this:

```text
query
  ↓
context
  ↓
answer
  ↓
grounded
```

Example:

```python
{
    "query": "What is the main topic of the document?",
    "context": [...],
    "answer": "...",
    "grounded": True
}
```

---

## Retrieval

The retrieval system uses Hybrid RAG.

### Dense Retrieval

ChromaDB retrieves semantically similar chunks.

### Keyword Retrieval

BM25 retrieves documents based on keyword matching.

### RRF

The results from both retrieval methods are combined using Reciprocal Rank Fusion.

```text
Dense Results
      +
BM25 Results
      ↓
     RRF
      ↓
Top Documents
```

---

## Self-RAG Grading

After the LLM generates an answer, the grader evaluates whether the answer is supported by the retrieved context.

The structured result is:

```python
Grade(
    grounded=True
)
```

or:

```python
Grade(
    grounded=False
)
```

This value is stored in the LangGraph state.

---

## Technologies

* Python
* LangChain
* LangGraph
* LangChain Groq
* ChromaDB
* BM25
* Pydantic
* PyPDF
* Sentence Transformers

---

## Installation

Create a virtual environment:

```bash
uv venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Do not commit `.env` to Git.

---

## Running the Project

From the `Code` directory:

```bash
uv run texting.py
```

This runs the complete LangGraph Self-RAG workflow.

---

## Current Workflow

The current implementation performs:

1. Document retrieval
2. Hybrid retrieval
3. Answer generation
4. Answer grounding evaluation
5. Conditional routing
6. Retrieval retry when the answer is not grounded

---

## Future Improvements

* Add retry counter
* Prevent infinite retrieval loops
* Add retrieval-quality grading
* Add answer-quality grading
* Add retrieval decision/router
* Improve chunk retrieval
* Add evaluation metrics
* Add API layer
* Add UI

---

## Goal

The goal of this project is to understand and implement **Self-RAG from scratch**, rather than treating it as a black-box framework feature.

The project focuses on understanding:

* LangGraph State
* Hybrid Retrieval
* Generation
* Structured grading
* Conditional graph routing
* Self-correction loops
