---
name: rag-ocr-llm
description: Multi-modal OCR parsing, bounding box extraction, FAISS vector indexing, SentenceTransformers embeddings, and grounded RAG with LLMs.
---

# RAG / OCR / LLM Skill

## 1. When Should I Use This?

Use this skill when:
* Building or maintaining document intelligence pipelines with **PaddleOCR**, **PyMuPDF**, or **Tesseract**.
* Creating Retrieval-Augmented Generation (RAG) workflows using **SentenceTransformers**, **FAISS**, or vector stores.
* Connecting to local LLMs (**Ollama**) or cloud providers (**OpenAI**, **Anthropic**) with structured prompt templates.
* Preventing LLM hallucinations through strict context grounding and source citation preservation.

---

## 2. What Should I Inspect First?

1. **Document Inputs**: File formats (PDF, scanned images, multi-column layouts, tables), page counts, and language requirements.
2. **OCR Engine & Hardware**: Check if PaddleOCR GPU or CPU is active, and confirm PyMuPDF (`fitz`) is installed.
3. **Embedding Model & Dimensions**: Check model identifier (e.g. `all-MiniLM-L6-v2` = 384 dimensions, `bge-small-en-v1.5` = 384 dimensions).
4. **LLM Provider & URL**: Check `OLLAMA_BASE_URL` (e.g. `http://localhost:11434`) or `OPENAI_API_KEY`.

---

## 3. What Workflow Should I Follow?

```text
Document Ingestion (PDF / Image)
            ↓
OCR Parsing & Layout Extraction (PaddleOCR / PyMuPDF with Bounding Boxes)
            ↓
Text Cleaning & Metadata-Preserving Chunking (Page #, Box coords, Section)
            ↓
Vector Embedding Generation (SentenceTransformers)
            ↓
FAISS Vector Indexing & Local Storage (IndexFlatIP with normalized vectors)
            ↓
Semantic Retrieval & Top-K Reranking (Cosine Similarity)
            ↓
Grounded Context Prompt Construction (Strict System Guardrails)
            ↓
LLM Generation + Verified Citation Formatting
```

### OCR Service with Bounding Box Preservation

```python
# app/services/ocr_service.py
import fitz  # PyMuPDF
from paddleocr import PaddleOCR
from dataclasses import dataclass

@dataclass
class OCRBox:
    text: str
    confidence: float
    bbox: list[list[float]] # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    page_num: int

class OCRService:
    def __init__(self, lang="en"):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)

    def extract_from_pdf_bytes(self, pdf_bytes: bytes, min_confidence=0.4) -> list[OCRBox]:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        all_boxes = []

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            
            result = self.ocr.ocr(img_bytes, cls=True)
            if not result or not result[0]:
                continue
                
            for line in result[0]:
                bbox, (text, conf) = line[0], line[1]
                if conf >= min_confidence and text.strip():
                    all_boxes.append(OCRBox(
                        text=text.strip(),
                        confidence=float(conf),
                        bbox=bbox,
                        page_num=page_idx + 1
                    ))
        return all_boxes
```

### FAISS Vector Indexing and Retrieval

```python
# app/services/rag_service.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.encoder = SentenceTransformer(model_name)
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        # Inner Product with normalized vectors = Cosine Similarity
        self.index = faiss.IndexFlatIP(self.dimension)
        self.chunks: list[dict] = []

    def add_documents(self, chunks: list[dict]):
        texts = [c["text"] for c in chunks]
        embeddings = self.encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        self.index.add(embeddings.astype(np.float32))
        self.chunks.extend(chunks)

    def search(self, query: str, top_k=4) -> list[dict]:
        query_vec = self.encoder.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        scores, indices = self.index.search(query_vec.astype(np.float32), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1 and idx < len(self.chunks):
                item = self.chunks[idx].copy()
                item["score"] = float(score)
                results.append(item)
        return results
```

### Grounded LLM Context Construction (Anti-Hallucination)

```python
# app/services/llm_service.py
import httpx

def generate_grounded_answer(query: str, context_chunks: list[dict], ollama_url="http://localhost:11434") -> str:
    # 1. Build strict context block
    context_str = "\n\n".join([
        f"[Source Doc (Page {c.get('page_num', 'Unknown')})]:\n{c['text']}"
        for c in context_chunks
    ])

    system_prompt = (
        "You are an expert document analysis assistant. "
        "Answer the user's question SOLELY based on the provided context below. "
        "If the information is not present in the context, explicitly state: 'The provided document does not contain this information.' "
        "Always cite page numbers for facts mentioned."
    )

    user_message = f"Context:\n{context_str}\n\nQuestion: {query}\n\nAnswer with page citations:"

    response = httpx.post(
        f"{ollama_url}/api/chat",
        json={
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "options": {"temperature": 0.1} # Low temperature for factual precision
        },
        timeout=60.0
    )
    return response.json()["message"]["content"]
```

---

## 4. What Decisions Should I Make?

| Strategy | Recommendation |
| :--- | :--- |
| **Chunking Strategy** | Use recursive character chunking (500-800 chars with 100 char overlap) or structural paragraph chunking. Never split mid-sentence. |
| **Embedding Normalization** | Always use `normalize_embeddings=True` with `faiss.IndexFlatIP` to calculate true cosine similarities in the $[-1, 1]$ range. |
| **LLM Temperature** | Set temperature to `0.0` - `0.2` for factual RAG to prevent creative hallucinations. |

---

## 5. What Should I Avoid?

* **NEVER throw away page numbers or bounding box metadata**: Source traceability is mandatory for citation validation.
* **NEVER dump the entire document into the prompt without retrieval**: Long irrelevant context degrades answer accuracy and inflates latency/costs.
* **NEVER omit fallback handling when FAISS returns low similarity (< 0.3)**: State that no relevant context was found.

---

## 6. How Should I Verify Success?

```bash
# 1. Test OCR text extraction on sample PDF
python -c "
from app.services.ocr_service import OCRService
ocr = OCRService()
print('OCR initialized successfully')
"

# 2. Test FAISS indexing and search accuracy
pytest tests/unit/test_rag_pipeline.py -v
```
