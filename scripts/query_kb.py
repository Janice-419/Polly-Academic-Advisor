from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

with open(
    "output/polyu_kb.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

chunk_size = 1000

chunks = [
    text[i:i+chunk_size]
    for i in range(0, len(text), chunk_size)
]

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "vector_db/polyu.index"
)
print("FAISS loaded")

question = input("Ask a question: ")
print("Question received")
print(question)

query_embedding = model.encode(
    [question]
)
print("Embedding created")

distances, indices = index.search(
    np.array(query_embedding).astype("float32"),
    k=3
)

context=""

for idx in indices[0]:
    context += chunks[idx]
    context += "\n\n"
print("Context Length:", len(context))

with open(
    "output/last_context.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(context)

print("Search completed")
print(indices)

print("Number of chunks:", len(chunks))
print("FAISS vectors:", index.ntotal)

print("\nTop Results:\n")

print("\nQuestion:", question)
print("\nTop Results:\n")

for rank, idx in enumerate(indices[0], start=1):
    print("=" * 60)
    print("Result", rank)
    print("Chunk ID:", idx)
    print()
    print(chunks[idx][:1000])
    print()
