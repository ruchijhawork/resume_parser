from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from parser import extract_skills

# Loads once when server starts (~90MB download, first time only)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list:
    return model.encode(text).tolist()

def match_resume(jd_text: str, resume_text: str) -> dict:
    jd_embedding = get_embedding(jd_text)
    resume_embedding = get_embedding(resume_text)

    score = cosine_similarity([jd_embedding], [resume_embedding])[0][0]
    score_100 = round(float(score) * 100, 2)

    jd_skills = set(extract_skills(jd_text))
    resume_skills = set(extract_skills(resume_text))
    matched = list(jd_skills & resume_skills)
    missing = list(jd_skills - resume_skills)

    if score_100 >= 70:
        strength = "Strong match! Candidate aligns well with the role."
    elif score_100 >= 45:
        strength = "Moderate match. Candidate meets some requirements."
    else:
        strength = "Weak match. Significant skill gaps detected."

    explanation = (
        f"The resume scores {score_100}% against the job description. "
        f"It matches {len(matched)} out of {len(jd_skills)} required skills. "
        f"{strength}"
    )

    return {
        "score": score_100,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": explanation
    }