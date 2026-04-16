import pdfplumber
import pandas as pd
from docx import Document


# 📄 PDF
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text


# 📊 EXCEL
def read_excel(file):
    df = pd.read_excel(file)

    table = df.to_dict(orient="records")

    insights = {}

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):

            insights[col] = {
                "max": float(df[col].max()),
                "min": float(df[col].min()),
                "avg": float(df[col].mean())
            }

    return table, insights


# 📝 DOCX
def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


# 🔥 MAIN (FIXED)
def read_file(file):
    filename = file.filename.lower()

    # ✅ Excel → return 2 values
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        return read_excel(file)

    # ✅ Other files → force same structure
    elif filename.endswith(".pdf"):
        return read_pdf(file), {}

    elif filename.endswith(".docx"):
        return read_docx(file), {}

    else:
        raise ValueError("Unsupported file format")