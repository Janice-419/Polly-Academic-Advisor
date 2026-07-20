from pypdf import PdfReader
import os

pdf_folder = "data/pdfs"

all_text = ""

for file in os.listdir(pdf_folder):

    if file.endswith(".pdf"):

        print("Reading:", file)

        path = os.path.join(pdf_folder, file)

        reader = PdfReader(path)

        for page in reader.pages:

            text = page.extract_text()

            if text:
                all_text += f"\n\n=== {file} ===\n"
                all_text += text

with open(
    "output/pdf_text.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(all_text)

print("PDF extraction completed!")