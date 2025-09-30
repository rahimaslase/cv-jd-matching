"""Command-line interface for testing CV matching locally."""

import asyncio
import json
from pathlib import Path
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cv_matching.models import CVData, JobDescription, MatchingRequest
from cv_matching.matcher import CVMatchingService


def create_sample_data():
    """Create sample CV and job description data."""
    
    # Sample CV Data
    cv_data = CVData(
        personal_info={
            "name": "Sarah Johnson",
            "email": "sarah.johnson@email.com",
            "phone": "+1-555-0456",
            "location": "New York, NY"
        },
        education=[
            {
                "degree": "Bachelor of Science",
                "field": "Data Science",
                "institution": "NYU",
                "year": "2021",
                "gpa": "3.7"
            }
        ],
        experience=[
            {
                "title": "Data Scientist",
                "company": "Analytics Corp",
                "duration": "2021 - Present",
                "description": "Developed predictive models using Python and R. Worked with large datasets and implemented machine learning solutions for business intelligence."
            }
        ],
        skills=[
            "Python", "R", "SQL", "Machine Learning", "Statistics", 
            "Pandas", "NumPy", "Scikit-learn", "Tableau", "Excel"
        ],
        projects=[
            {
                "name": "Customer Churn Prediction",
                "description": "Built ML model to predict customer churn with 85% accuracy",
                "technologies": ["Python", "Scikit-learn", "Pandas"]
            }
        ],
        certifications=[
            {
                "name": "Google Data Analytics Certificate",
                "issuer": "Google",
                "year": "2022"
            }
        ]
    )
    
    # Sample Job Description
    job_description = JobDescription(
        title="Senior Data Scientist",
        company="TechStart Inc.",
        location="Remote",
        employment_type="Full-time",
        description="""
        We are looking for a Senior Data Scientist to join our growing team. You will be responsible for 
        building and deploying machine learning models, analyzing large datasets, and providing insights 
        to drive business decisions.
        
        Responsibilities:
        - Develop and deploy machine learning models
        - Analyze large datasets to extract insights
        - Collaborate with engineering and product teams
        - Present findings to stakeholders
        - Mentor junior data scientists
        """,
        requirements=[
            "Master's degree in Data Science, Statistics, or related field",
            "3+ years of experience in data science",
            "Strong programming skills in Python and R",
            "Experience with machine learning frameworks",
            "Experience with SQL and databases",
            "Strong statistical knowledge",
            "Experience with data visualization tools"
        ],
        preferred_qualifications=[
            "PhD in Data Science or related field",
            "Experience with deep learning",
            "Experience with cloud platforms (AWS, GCP)",
            "Experience with big data tools (Spark, Hadoop)",
            "Strong communication skills",
            "Experience in startup environment"
        ]
    )
    
    return MatchingRequest(cv_data=cv_data, job_description=job_description)


async def run_local_analysis():
    """Run CV matching analysis locally without API."""
    
    print("🔍 CV Matching Analysis (Local)")
    print("=" * 50)
    
    # Create sample data
    request = create_sample_data()
    
    print(f"📄 CV: {request.cv_data.personal_info['name']}")
    print(f"💼 Job: {request.job_description.title} at {request.job_description.company}")
    print(f"🎯 Skills: {', '.join(request.cv_data.skills[:5])}...")
    print("-" * 50)
    
    try:
        # Initialize service
        cv_service = CVMatchingService()
        
        # Validate inputs
        if not cv_service.validate_inputs(request):
            print("❌ Invalid input data")
            return
        
        print("🤖 Running AI analysis...")
        
        # Perform analysis
        response = await cv_service.match_cv_to_job(request)
        
        # Display results
        analysis = response.analysis
        overall = analysis.overall_analysis
        
        print(f"\n✅ Analysis Complete!")
        print(f"⏱️  Processing Time: {response.processing_time:.2f} seconds")
        print(f"🤖 Model Used: {response.model_used}")
        print("-" * 50)
        
        print(f"🎯 Overall Compatibility: {overall.compatibility_score}%")
        print(f"✅ Matched Requirements: {len(analysis.matched_requirements)}")
        print(f"❌ Missing Requirements: {len(analysis.missing_requirements)}")
        
        # Show detailed breakdown
        breakdown = analysis.detailed_breakdown
        print(f"\n📊 Detailed Breakdown:")
        print(f"  • Education: {breakdown.education_match}%")
        print(f"  • Skills: {breakdown.skills_match}%")
        print(f"  • Experience: {breakdown.experience_match}%")
        print(f"  • Tools/Frameworks: {breakdown.tools_frameworks_match}%")
        
        # Show strengths
        print(f"\n💪 Key Strengths:")
        for strength in overall.strengths[:3]:
            print(f"  • {strength}")
        
        # Show gaps
        print(f"\n⚠️  Main Gaps:")
        for gap in overall.gaps[:3]:
            print(f"  • {gap}")
        
        # Show recommendations
        print(f"\n💡 Recommendations:")
        for rec in overall.recommendations[:3]:
            print(f"  • {rec}")
        
        # Show top matches
        print(f"\n✅ Top Matched Requirements:")
        for match in analysis.matched_requirements[:3]:
            print(f"  • {match.requirement}")
            print(f"    Evidence: {match.cv_evidence}")
            print(f"    Strength: {match.match_strength} (Score: {match.relevance_score}/10)")
        
        # Show critical missing
        critical_missing = [req for req in analysis.missing_requirements if req.importance == "critical"]
        if critical_missing:
            print(f"\n❌ Critical Missing Requirements:")
            for missing in critical_missing[:3]:
                print(f"  • {missing.requirement}")
                if missing.alternative_skills:
                    print(f"    Alternatives: {', '.join(missing.alternative_skills)}")
        
        # Get summary
        summary = cv_service.get_analysis_summary(analysis)
        print(f"\n📋 Summary:")
        print(f"  • High Strength Matches: {summary['high_strength_matches']}")
        print(f"  • Critical Missing: {summary['critical_missing']}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Make sure you have set your OPENAI_API_KEY environment variable")


def main():
    """Main function."""
    print("🚀 CV Matching CLI Test")
    print("=" * 50)
    print("This script tests the CV matching system locally.")
    print("Make sure you have set your OPENAI_API_KEY environment variable.")
    print("=" * 50)
    
    try:
        asyncio.run(run_local_analysis())
    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
