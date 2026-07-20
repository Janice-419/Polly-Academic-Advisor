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

with open(
    "output/chunks.txt",
    "w",
    encoding="utf-8"
) as f:

    for i, chunk in enumerate(chunks):

        f.write(f"\n\n===== CHUNK {i} =====\n")
        f.write(chunk)

print("Chunks saved!")