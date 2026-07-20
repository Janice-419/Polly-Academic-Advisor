from pypdf import PdfReader

reader = PdfReader(
    "data/pdfs/Student_Handbook_2025-26_English.pdf"
)

all_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        all_text += text + "\n"

with open(
    "output/student_handbook.txt",
    "w",
    encoding="utf-8"
) as f:
    f.write(all_text)

print("Text extraction completed!")