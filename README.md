# CV-JD Match Score API

A FastAPI application that analyzes CV-Job Description compatibility using AI.

## 🚀 Features

- AI-powered CV-JD matching analysis
- Detailed compatibility scoring
- Requirement matching and gap analysis
- Production-ready FastAPI endpoints

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| POST | `/match` | CV-JD matching analysis |
| GET | `/docs` | Swagger UI documentation |

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📊 API Usage

### Request Format

```json
{
  "job_description": "Your job description text here",
  "cv": "Your CV/resume text here"
}
```

### Example Request

```bash
curl -X POST "http://localhost:8000/match" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Software Engineer with Python experience",
    "cv": "John Doe, Python developer with 3 years experience"
  }'
```

## 🔧 Development

The API is running on `http://localhost:8000`

- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## 📝 Response Format

Returns detailed analysis including:
- Matched requirements
- Missing requirements  
- Overall compatibility score
- Detailed breakdown by category
- Execution time
