# 🧠 Smart Resume Screener

An AI-powered resume screening API that uses HuggingFace sentence embeddings to match resumes against job descriptions.

## Features

- 📄 Upload multiple PDF resumes at once
- 🔍 Semantic similarity scoring via HuggingFace `all-MiniLM-L6-v2` (Runs completely locally!)
- 🛠 Skill extraction from a predefined skills database
- 📊 Results ranked by match score with matched/missing skills breakdown
- ⚡ Built with FastAPI for high performance

## Project Structure

```text
smart-resume-screener/
├── main.py           # FastAPI app & /screen endpoint
├── matcher.py        # Embedding + cosine similarity matching logic
├── parser.py         # PDF text extraction & skill parsing
├── requirements.txt  # Python dependencies
├── .gitignore
└── README.md
```

## Setup

**Prerequisites:** Python 3.9+

### 1. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

> **Note:** The first time you run the application and make a request, it will download the `all-MiniLM-L6-v2` model (~90MB) locally. Subsequent requests will be much faster.

The API will be available at: `http://127.0.0.1:8000`

## API Usage

### `GET /`
Health check — returns a status message.

### `POST /screen`
Screen one or more resumes against a job description.

**Constraints:**
- The `job_description` field cannot be empty.
- Only `.pdf` files are supported.

**Form fields:**
| Field | Type | Description |
|---|---|---|
| `job_description` | `string` | The full job description text |
| `resumes` | `file(s)` | One or more PDF resume files |

**Example with `curl`:**
```bash
curl -X POST "http://127.0.0.1:8000/screen" \
  -F "job_description=We are looking for a Python developer with experience in FastAPI, Docker, and AWS." \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.pdf"
```

**Example Response:**
```json
{
  "total_resumes": 2,
  "results": [
    {
      "filename": "resume1.pdf",
      "score": 82.45,
      "matched_skills": ["python", "fastapi", "docker", "aws"],
      "missing_skills": [],
      "explanation": "The resume scores 82.45% against the job description. It matches 4 out of 4 required skills. Strong match! Candidate aligns well with the role."
    },
    {
      "filename": "resume2.pdf",
      "score": 41.10,
      "matched_skills": ["python"],
      "missing_skills": ["fastapi", "docker", "aws"],
      "explanation": "The resume scores 41.10% against the job description. It matches 1 out of 4 required skills. Weak match. Significant skill gaps detected."
    }
  ]
}
```

## Score Interpretation

| Score | Meaning |
|---|---|
| ≥ 70% | ✅ Strong match |
| 45–69% | ⚠️ Moderate match |
| < 45% | ❌ Weak match |

## Interactive API Docs

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
