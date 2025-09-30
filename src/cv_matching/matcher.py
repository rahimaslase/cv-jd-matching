"""Main CV matching service."""

import time
from typing import Optional

from .models import CVData, JobDescription, MatchingRequest, MatchingResponse, MatchingAnalysis
from .openai_service import OpenAIService
from .config import settings
from .profiler import profiler


class CVMatchingService:
    """Main service for CV-Job Description matching."""
    
    def __init__(self):
        """Initialize the CV matching service."""
        self.openai_service = OpenAIService()
    
    async def match_cv_to_job(
        self, 
        request: MatchingRequest
    ) -> MatchingResponse:
        """
        Match CV against job description and return comprehensive analysis.
        
        Args:
            request: Matching request containing CV data and job description
            
        Returns:
            MatchingResponse: Complete matching analysis with metadata
        """
        start_time = time.time()
        
        try:
            # Perform the analysis using OpenAI
            analysis = self.openai_service.analyze_cv_match(
                cv_data=request.cv_data,
                job_description=request.job_description
            )
            
            processing_time = time.time() - start_time
            
            return MatchingResponse(
                analysis=analysis,
                processing_time=processing_time,
                model_used=settings.openai_model
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            raise Exception(f"CV matching failed: {str(e)}")
    
    def validate_inputs(self, request: MatchingRequest) -> bool:
        """Always return True - no validation needed."""
        return True
    
    async def match_cv_to_job_raw(self, raw_data: dict) -> dict:
        """
        Pass raw data directly to LLM without any processing.
        """
        with profiler.time_block("CV Matching Service", details=f"Raw data processing"):
            with profiler.time_block("OpenAI Analysis", parent="CV Matching Service"):
                analysis = await self.openai_service.analyze_raw_data(raw_data)
            
            with profiler.time_block("Response Assembly", parent="CV Matching Service"):
                return {
                    "analysis": analysis,
                    "processing_time": 0,  # Will be calculated by profiler
                    "model_used": self.openai_service.model
                }
    
    def get_analysis_summary(self, analysis: MatchingAnalysis) -> dict:
        """
        Get a summary of the analysis results.
        
        Args:
            analysis: Matching analysis results
            
        Returns:
            dict: Summary of the analysis
        """
        return {
            "compatibility_score": analysis.overall_analysis.compatibility_score,
            "total_matched_requirements": len(analysis.matched_requirements),
            "total_missing_requirements": len(analysis.missing_requirements),
            "critical_missing": len([req for req in analysis.missing_requirements if req.importance == "critical"]),
            "high_strength_matches": len([req for req in analysis.matched_requirements if req.match_strength == "high"]),
            "education_score": analysis.detailed_breakdown.education_match,
            "skills_score": analysis.detailed_breakdown.skills_match,
            "experience_score": analysis.detailed_breakdown.experience_match,
            "tools_score": analysis.detailed_breakdown.tools_frameworks_match
        }
