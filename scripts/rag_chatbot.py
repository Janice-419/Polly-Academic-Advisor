from ollama import chat

question = input("Question: ")

with open(
    "output/last_context.txt",
    "r",
    encoding="utf-8"
) as f:
    context = f.read()

prompt = f"""
You are a PolyU Academic Advisor.

Answer ONLY using the information in the context.

If the answer is not found in the context, say:
'I cannot find this information in the knowledge base.'

Context:
{context}

Question:
{question}
"""

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