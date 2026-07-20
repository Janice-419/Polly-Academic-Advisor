from sentence_transformers import SentenceTransformer
from ollama import chat
import faiss
import numpy as np

# Load Knowledge Base
with open(
    "output/polyu_kb.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

# Create chunks
chunk_size = 1000

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Load FAISS index
index = faiss.read_index(
    "vector_db/polyu.index"
)

# Ask question
question = input("Ask a question: ")

# Convert question to embedding
query_embedding = model.encode(
    [question]
)

# Search top 3 chunks
distances, indices = index.search(
    np.array(query_embedding).astype("float32"),
    k=3
)

# Build context
context = ""

for idx in indices[0]:
    context += chunks[idx]
    context += "\n\n"

# Create prompt
prompt = f"""
You are a PolyU Academic Advisor.

Answer the student's question using ONLY the information below.

If the answer cannot be found in the context,
say that the information is unavailable.

Context:
{context}

Question:
{question}
"""

# Send to Phi-4
response = chat(
    model="phi4",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAnswer:\n")
print(response["message"]["content"])