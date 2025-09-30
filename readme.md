# CV Matching System

A comprehensive AI-powered system that analyzes CVs against job descriptions to provide detailed matching insights and compatibility scores across all professional domains.

## Features

- **Universal Domain Support**: Works across all professional fields without domain-specific constraints
- **Comprehensive Analysis**: Evaluates education, experience, projects, skills, tools, frameworks, and other relevant attributes
- **Detailed Matching Report**: Provides both matched and missing requirements
- **Accurate Scoring System**: Returns precise compatibility percentage
- **LinkedIn JD Integration**: Processes job descriptions from LinkedIn and other sources
- **AI-Powered Intelligence**: Uses OpenAI LLM for nuanced understanding and analysis

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- uv package manager

### Installation

1. **Clone and setup the project:**
   ```bash
   cd "CV Matching"
   uv sync
   ```

2. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the API server:**
   ```bash
   uv run python -m cv_matching.main
   ```

4. **Access the API documentation:**
   Open http://localhost:8000/docs in your browser

## Usage

### API Endpoints

#### 1. Match CV to Job Description
```bash
POST /match
```

**Request Body:**
```json
{
  "cv_data": {
    "personal_info": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "education": [
      {
        "degree": "Master of Science",
        "field": "Computer Science",
        "institution": "Stanford University",
        "year": "2020"
      }
    ],
    "experience": [
      {
        "title": "Senior AI Engineer",
        "company": "TechCorp",
        "duration": "2022 - Present",
        "description": "Led ML model development..."
      }
    ],
    "skills": ["Python", "Machine Learning", "PyTorch", "AWS"],
    "projects": [
      {
        "name": "AI Recommendation System",
        "description": "Built recommendation engine...",
        "technologies": ["Python", "PyTorch"]
      }
    ]
  },
  "job_description": {
    "title": "Senior AI Engineer",
    "company": "InnovateTech",
    "description": "We are seeking a Senior AI Engineer...",
    "requirements": [
      "Master's degree in Computer Science",
      "5+ years ML experience",
      "Strong Python skills"
    ],
    "preferred_qualifications": [
      "PhD in Computer Science",
      "Experience with deep learning"
    ]
  }
}
```

**Response:**
```json
{
  "analysis": {
    "matched_requirements": [
      {
        "requirement": "Master's degree in Computer Science",
        "cv_evidence": "Master of Science in Computer Science from Stanford University",
        "match_strength": "high",
        "relevance_score": 10
      }
    ],
    "missing_requirements": [
      {
        "requirement": "5+ years ML experience",
        "importance": "critical",
        "alternative_skills": ["2+ years ML experience"]
      }
    ],
    "overall_analysis": {
      "compatibility_score": 85,
      "strengths": ["Strong educational background", "Relevant technical skills"],
      "gaps": ["Limited years of experience"],
      "recommendations": ["Gain more hands-on ML experience"]
    },
    "detailed_breakdown": {
      "education_match": 100,
      "skills_match": 90,
      "experience_match": 70,
      "tools_frameworks_match": 85
    }
  },
  "processing_time": 3.45,
  "model_used": "gpt-4"
}
```

#### 2. Get Matching Summary
```bash
POST /match/summary
```

Returns a condensed summary of the matching analysis.

#### 3. Health Check
```bash
GET /health
```

### Testing

#### Test with Sample Data
```bash
# Run the CLI test
uv run python examples/cli_test.py

# Run API tests (requires server to be running)
uv run python examples/test_api.py
```

#### Test API with curl
```bash
# Start the server first
uv run python -m cv_matching.main

# In another terminal, test the API
curl -X POST "http://localhost:8000/match" \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json
```

## Project Structure

```
CV Matching/
├── src/cv_matching/          # Main package
│   ├── __init__.py
│   ├── models.py            # Pydantic models
│   ├── config.py            # Configuration management
│   ├── openai_service.py    # OpenAI integration
│   ├── matcher.py           # Core matching logic
│   ├── api.py               # FastAPI application
│   └── main.py              # Entry point
├── examples/                # Example scripts and data
│   ├── sample_cv_data.py    # Sample data for testing
│   ├── test_api.py          # API testing script
│   └── cli_test.py          # CLI testing script
├── tests/                   # Unit tests
├── pyproject.toml           # Project configuration
├── env.example              # Environment variables template
└── README.md               # This file
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=4000

# Application Configuration
APP_NAME=CV Matching API
DEBUG=false

# API Configuration
HOST=0.0.0.0
PORT=8000

# Analysis Configuration
MAX_RETRIES=3
TIMEOUT_SECONDS=60
```

### Model Configuration

The system uses OpenAI's GPT models for analysis. You can configure:

- **Model**: Choose between `gpt-4`, `gpt-3.5-turbo`, etc.
- **Temperature**: Controls randomness (0.0-2.0, lower = more deterministic)
- **Max Tokens**: Maximum response length
- **Retries**: Number of retry attempts for failed requests

## Development

### Setup Development Environment

```bash
# Install development dependencies
uv sync --extra dev

# Run linting
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
uv run mypy src/

# Run tests
uv run pytest tests/
```

### Adding New Features

1. **Models**: Add new Pydantic models in `models.py`
2. **Services**: Create new service classes in separate files
3. **API**: Add new endpoints in `api.py`
4. **Configuration**: Add new settings in `config.py`

## API Documentation

When the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is set in the `.env` file
   - Verify the key has sufficient credits

2. **Import Errors**
   - Make sure you're running from the project root
   - Check that all dependencies are installed with `uv sync`

3. **Timeout Errors**
   - Increase `TIMEOUT_SECONDS` in configuration
   - Check your internet connection

4. **JSON Parsing Errors**
   - The OpenAI response might be malformed
   - Check the `max_tokens` setting

### Debug Mode

Enable debug mode for detailed error messages:

```bash
DEBUG=true uv run python -m cv_matching.main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub