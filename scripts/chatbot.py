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

while True:
    question = input("\nAsk a question: ")

    if question.lower() == "exit":
        break

    found = False

    for chunk in chunks:
        if any(
            word.lower() in chunk.lower()
            for word in question.split()
        ):
            print("\nRelevant Information:")
            print(chunk[:1000])
            found = True
            break

    if not found:
        print("No relevant information found.")