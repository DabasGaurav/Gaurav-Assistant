import os
from pypdf import PdfReader
from docx import Document

ONE_DRIVE_PATH = "/Users/gauravdabas/Library/CloudStorage/OneDrive-IndianSchoolofBusiness"

def read_pdf(path):

```
text = ""

try:

    reader = PdfReader(path)

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

except:
    pass

return text
```

def read_docx(path):

```
text = ""

try:

    doc = Document(path)

    for para in doc.paragraphs:
        text += para.text + "\n"

except:
    pass

return text
```

def search_knowledge(query):

```
results = []

for root, dirs, files in os.walk(ONE_DRIVE_PATH):

    for file in files:

        full_path = os.path.join(root, file)

        content = ""

        if file.endswith(".pdf"):
            content = read_pdf(full_path)

        elif file.endswith(".docx"):
            content = read_docx(full_path)

        if query.lower() in content.lower():

            results.append({
                "file": file,
                "content": content[:3000]
            })

return results
```
