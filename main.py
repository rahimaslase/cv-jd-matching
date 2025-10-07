import time
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="CV-JD Match Score API", version="1.0.0")

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")
client = OpenAI(api_key=api_key)

class MatchRequest(BaseModel):
    job_description: str
    cv: str

class MatchResponse(BaseModel):
    analysis: Dict[str, Any]
    execution_time: float

@app.get("/")
async def root():
    return {"message": "CV-JD Match Score API"}

@app.post("/match", response_model=MatchResponse)
async def match_cv_jd(request: MatchRequest):
    try:
        start_time = time.time()
        
        completion = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an HR assistant who evaluates the suitability of a CV for a given Job Description. Provide the analysis in JSON format."},
                {"role": "user", "content": f"Please evaluate the following CV against the Job Description and provide a matching score and analysis in the following JSON format:\n\n```json\n{{\n  \"analysis\": {{\n    \"matched_requirements\": [\n      {{\n        \"requirement\": \"requirement text\",\n        \"cv_evidence\": \"evidence from CV\",\n        \"match_strength\": \"high/medium/low\",\n        \"relevance_score\": 1-10\n      }}\n    ],\n    \"missing_requirements\": [\n      {{\n        \"requirement\": \"missing requirement\",\n        \"importance\": \"critical/important/nice-to-have\",\n        \"alternative_skills\": [\"alternative skills found\"]\n      }}\n    ],\n    \"overall_analysis\": {{\n      \"compatibility_score\": 0-100,\n      \"strengths\": [\"list of strengths\"],\n      \"gaps\": [\"list of gaps\"],\n      \"recommendations\": [\"list of recommendations\"]\n    }},\n    \"detailed_breakdown\": {{\n      \"education_match\": 0-100,\n      \"skills_match\": 0-100,\n      \"experience_match\": 0-100,\n      \"tools_frameworks_match\": 0-100\n    }}\n  }}\n}}\n```\n\nJob Description:\n{request.job_description}\n\nCV:\n{request.cv}"}
            ]
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Parse the JSON response
        import json
        try:
            analysis = json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Failed to parse AI response")
        
        return MatchResponse(analysis=analysis, execution_time=execution_time)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)