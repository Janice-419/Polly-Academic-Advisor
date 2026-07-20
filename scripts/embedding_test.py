from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

sentences = [
    "How do I apply for graduation?",
    "Application for Graduation",
    "Work Integrated Education"
]

embeddings = model.encode(sentences)

print("Embedding shape:")
print(embeddings.shape)
