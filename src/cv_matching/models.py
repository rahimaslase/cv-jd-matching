"""Pydantic models for CV matching system."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field


class MatchedRequirement(BaseModel):
    """Model for matched requirements between CV and job description."""
    
    requirement: Optional[str] = Field(default=None, description="Specific requirement from job description")
    cv_evidence: Optional[str] = Field(default=None, description="Corresponding evidence from CV")
    match_strength: Optional[str] = Field(default=None, description="Strength of the match")
    relevance_score: Optional[int] = Field(default=0, ge=0, le=10, description="Relevance score from 0-10")


class MissingRequirement(BaseModel):
    """Model for missing requirements in CV compared to job description."""
    
    requirement: Optional[str] = Field(default=None, description="Missing requirement from job description")
    importance: Optional[str] = Field(default=None, description="Importance level")
    alternative_skills: Optional[List[str]] = Field(default=None, description="Potential alternatives found in CV")


class OverallAnalysis(BaseModel):
    """Model for overall analysis results."""
    
    compatibility_score: Optional[int] = Field(default=0, ge=0, le=100, description="Overall compatibility score (0-100)")
    strengths: Optional[List[str]] = Field(default=None, description="Key strengths of the candidate")
    gaps: Optional[List[str]] = Field(default=None, description="Main areas of concern")
    recommendations: Optional[List[str]] = Field(default=None, description="Suggestions for improvement")


class DetailedBreakdown(BaseModel):
    """Model for detailed breakdown of matching scores."""
    
    education_match: Optional[int] = Field(default=0, ge=0, le=100, description="Education matching score (0-100)")
    skills_match: Optional[int] = Field(default=0, ge=0, le=100, description="Skills matching score (0-100)")
    experience_match: Optional[int] = Field(default=0, ge=0, le=100, description="Experience matching score (0-100)")
    tools_frameworks_match: Optional[int] = Field(default=0, ge=0, le=100, description="Tools and frameworks matching score (0-100)")


class CVData(BaseModel):
    """Model for structured CV data."""
    
    personal_info: Optional[Dict[str, Any]] = Field(default=None, description="Personal information")
    education: Optional[List[Dict[str, Any]]] = Field(default=None, description="Educational background")
    experience: Optional[List[Dict[str, Any]]] = Field(default=None, description="Work experience")
    skills: Optional[List[str]] = Field(default=None, description="Technical and soft skills")
    projects: Optional[List[Dict[str, Any]]] = Field(default=None, description="Projects and achievements")
    certifications: Optional[List[Dict[str, Any]]] = Field(default=None, description="Certifications")
    languages: Optional[List[Dict[str, Any]]] = Field(default=None, description="Language proficiencies")
    additional_info: Optional[Dict[str, Any]] = Field(default=None, description="Additional relevant information")


class JobDescription(BaseModel):
    """Model for job description data."""
    
    title: Optional[str] = Field(default=None, description="Job title")
    company: Optional[str] = Field(default=None, description="Company name")
    description: Optional[str] = Field(default=None, description="Full job description text")
    requirements: Optional[List[str]] = Field(default=None, description="List of requirements")
    preferred_qualifications: Optional[List[str]] = Field(default=None, description="Preferred qualifications")
    location: Optional[str] = Field(default=None, description="Job location")
    employment_type: Optional[str] = Field(default=None, description="Employment type (full-time, part-time, etc.)")
    salary_range: Optional[str] = Field(default=None, description="Salary range if available")


class MatchingAnalysis(BaseModel):
    """Complete model for CV-Job Description matching analysis."""
    
    matched_requirements: Optional[List[MatchedRequirement]] = Field(default=None, description="List of matched requirements")
    missing_requirements: Optional[List[MissingRequirement]] = Field(default=None, description="List of missing requirements")
    overall_analysis: Optional[OverallAnalysis] = Field(default=None, description="Overall analysis results")
    detailed_breakdown: Optional[DetailedBreakdown] = Field(default=None, description="Detailed breakdown of scores")


class MatchingRequest(BaseModel):
    """Model for CV matching request."""
    
    cv_data: Optional[CVData] = Field(default=None, description="Structured CV data")
    job_description: Optional[JobDescription] = Field(default=None, description="Job description data")


class MatchingResponse(BaseModel):
    """Model for CV matching response."""
    
    analysis: Optional[MatchingAnalysis] = Field(default=None, description="Complete matching analysis")
    processing_time: Optional[float] = Field(default=None, description="Processing time in seconds")
    model_used: Optional[str] = Field(default=None, description="OpenAI model used for analysis")
