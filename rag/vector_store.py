import json
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


def build_vector_store():
    """Build FAISS vector store from market_history.json with year metadata."""
    history_path = os.path.join(os.path.dirname(__file__), "market_history.json")

    try:
        with open(history_path, "r") as f:
            history = json.load(f)
        docs = [
            Document(
                page_content=item["event"],
                metadata={"year": item["year"]}
            )
            for item in history
        ]
    except Exception:
        # Fallback static docs
        docs = [
            Document(page_content="Apple stock rose 3% after earnings beat.", metadata={"year": 2023}),
            Document(page_content="Tesla announced new AI chips.", metadata={"year": 2023}),
            Document(page_content="Federal Reserve signals possible rate cuts.", metadata={"year": 2024}),
            Document(page_content="Nvidia expands data center operations.", metadata={"year": 2023}),
        ]

    # Local HuggingFace embeddings — no API key required, runs on CPU
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore