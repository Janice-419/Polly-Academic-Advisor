with open(
    "output/polyu_kb.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

chunk_size = 2000

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

print("Number of chunks:", len(chunks))

for chunk in chunks:
    if chunk.strip():
        print("\nFIRST CHUNK:\n")
        print(chunk[:1000])
        break