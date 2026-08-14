from app.rag import LocalVectorStore

def test_vector_store_retrieval():
    store = LocalVectorStore()
    store.add_texts(["FastAPI documentation", "PostgreSQL database guide", "Machine learning overview"])
    results = store.search("How to build APIs", top_k=1)
    assert len(results) == 1
    assert "FastAPI" in results[0]
