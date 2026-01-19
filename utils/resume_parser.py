from PyPDF2 import PdfReader
import docx

def extract_text(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if file_name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text

    if file_name.endswith(".docx"):
        d = docx.Document(uploaded_file)
        return "\n".join([p.text for p in d.paragraphs])

    return ""
