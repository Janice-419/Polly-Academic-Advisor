from sentence_transformers import SentenceTransformer

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

print("Total chunks:", len(chunks))

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

print("Embedding shape:")
print(embeddings.shape)