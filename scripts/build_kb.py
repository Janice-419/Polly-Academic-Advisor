pdf_text = ""
web_text = ""

with open(
    "output/pdf_text.txt",
    "r",
    encoding="utf-8"
) as f:
    pdf_text = f.read()

with open(
    "output/web_text.txt",
    "r",
    encoding="utf-8"
) as f:
    web_text = f.read()

combined = pdf_text + "\n\n" + web_text

with open(
    "output/polyu_kb.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(combined)

print("PolyU Knowledge Base created!")