from pdfminer.high_level import extract_text

SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "keras", "scikit-learn",
    "react", "node", "angular", "vue", "fastapi", "django", "flask",
    "aws", "gcp", "azure", "docker", "kubernetes", "ci/cd",
    "data analysis", "pandas", "numpy", "matplotlib", "excel",
    "git", "linux", "rest api", "graphql"
]

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        return extract_text(pdf_path)
    except Exception as e:
        return ""

def extract_text_from_string(text: str) -> str:
    return text.strip()

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    return [skill for skill in SKILLS_DB if skill in text_lower]
