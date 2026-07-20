with open(
    "output/student_handbook.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

chunk_size = 1000

chunks = [
    text[i:i+chunk_size]
    for i in range(0, len(text), chunk_size)
]

keyword = input("Enter a keyword: ")

for i, chunk in enumerate(chunks):
    if keyword.lower() in chunk.lower():
        print("\nFound in chunk", i)
        print(chunk)
        break