from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

with open(
    "output/polyu_kb.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

chunk_size = 2000

chunks = [
    text[i:i+chunk_size]
    for i in range(0, len(text), chunk_size)
]

print("Chunks:", len(chunks))

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

index = faiss.IndexFlatL2(384)

index.add(
    np.array(embeddings).astype("float32")
)

faiss.write_index(
    index,
    "vector_db/polyu.index"
)

print("FAISS index saved!")
