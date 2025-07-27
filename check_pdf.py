from PyPDF2 import PdfReader
import os

input_dir = "input"
pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]

for pdf_file in pdf_files:
    path = os.path.join(input_dir, pdf_file)
    try:
        with open(path, 'rb') as f:
            reader = PdfReader(f)
            print(f"\nFile: {pdf_file}")
            print(f"Pages: {len(reader.pages)}")
            print(f"Has outlines: {'Yes' if reader.outline else 'No'}")
            print(f"Metadata: {reader.metadata}")
    except Exception as e:
        print(f"\nError processing {pdf_file}: {str(e)}")