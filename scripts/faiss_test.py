from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

sentences = [
    "Application for Graduation",
    "Work Integrated Education",
    "Subject Registration",
    "Academic Probation"
]

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(sentences)

index = faiss.IndexFlatL2(384)

index.add(np.array(embeddings))

question = "How do I graduate?"

query_embedding = model.encode([question])

distances, indices = index.search(
    np.array(query_embedding),
    k=1
)

print("Question:")
print(question)

print("\nMost Relevant:")
print(sentences[indices[0][0]])
