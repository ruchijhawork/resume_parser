from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from matcher import match_resume
from parser import extract_text_from_pdf, extract_text_from_string
import tempfile
import os

load_dotenv()

app = FastAPI(
    title="Smart Resume Screener",
    description="AI-powered resume screening using HuggingFace embeddings",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Smart Resume Screener API is running!"}

@app.post("/screen")
async def screen_resumes(
    job_description: str = Form(..., description="Paste the job description here"),
    resumes: list[UploadFile] = File(..., description="Upload one or more resume PDFs")
):
    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")

    if len(resumes) == 0:
        raise HTTPException(status_code=400, detail="Please upload at least one resume")

    results = []

    for resume in resumes:
        # Validate file type
        if not resume.filename.endswith(".pdf"):
            results.append({
                "filename": resume.filename,
                "error": "Only PDF files are supported"
            })
            continue

        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await resume.read())
                tmp_path = tmp.name

            # Extract text
            resume_text = extract_text_from_pdf(tmp_path)
            os.unlink(tmp_path)  # cleanup temp file

            if not resume_text.strip():
                results.append({
                    "filename": resume.filename,
                    "error": "Could not extract text from PDF"
                })
                continue

            # Match against JD
            result = match_resume(job_description, resume_text)
            result["filename"] = resume.filename
            results.append(result)

        except Exception as e:
            results.append({
                "filename": resume.filename,
                "error": str(e)
            })

    # Sort successful results by score
    successful = [r for r in results if "score" in r]
    failed = [r for r in results if "error" in r]
    successful.sort(key=lambda x: x["score"], reverse=True)

    return JSONResponse(content={
        "total_resumes": len(resumes),
        "results": successful + failed
    })
