"""Sample CV data for testing the CV matching system."""

from cv_matching.models import CVData, JobDescription, MatchingRequest


def get_sample_cv_data() -> CVData:
    """Get sample CV data for testing."""
    return CVData(
        personal_info={
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-555-0123",
            "location": "San Francisco, CA"
        },
        education=[
            {
                "degree": "Master of Science",
                "field": "Computer Science",
                "institution": "Stanford University",
                "year": "2020",
                "gpa": "3.8"
            },
            {
                "degree": "Bachelor of Science",
                "field": "Software Engineering",
                "institution": "UC Berkeley",
                "year": "2018",
                "gpa": "3.6"
            }
        ],
        experience=[
            {
                "title": "Senior AI Engineer",
                "company": "TechCorp Inc.",
                "duration": "2022 - Present",
                "description": "Led development of machine learning models for recommendation systems. Implemented deep learning solutions using PyTorch and TensorFlow. Managed a team of 3 junior engineers."
            },
            {
                "title": "Machine Learning Engineer",
                "company": "DataFlow Solutions",
                "duration": "2020 - 2022",
                "description": "Developed and deployed ML models for predictive analytics. Worked with Python, scikit-learn, and cloud platforms (AWS, GCP). Collaborated with data scientists and product teams."
            },
            {
                "title": "Software Developer",
                "company": "StartupXYZ",
                "duration": "2018 - 2020",
                "description": "Built web applications using React, Node.js, and PostgreSQL. Implemented RESTful APIs and worked in agile development environment."
            }
        ],
        skills=[
            "Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow",
            "scikit-learn", "AWS", "GCP", "Docker", "Kubernetes", "React", "Node.js",
            "PostgreSQL", "MongoDB", "Git", "Agile", "Team Leadership", "Data Analysis",
            "Statistics", "Computer Vision", "NLP", "RESTful APIs", "Microservices"
        ],
        projects=[
            {
                "name": "AI-Powered Recommendation System",
                "description": "Built a recommendation engine using collaborative filtering and deep learning, improving user engagement by 25%",
                "technologies": ["Python", "PyTorch", "AWS", "Docker"]
            },
            {
                "name": "Real-time Fraud Detection",
                "description": "Developed ML model for real-time fraud detection with 95% accuracy using ensemble methods",
                "technologies": ["Python", "scikit-learn", "Apache Kafka", "Redis"]
            }
        ],
        certifications=[
            {
                "name": "AWS Certified Machine Learning - Specialty",
                "issuer": "Amazon Web Services",
                "year": "2023"
            },
            {
                "name": "Google Cloud Professional Machine Learning Engineer",
                "issuer": "Google Cloud",
                "year": "2022"
            }
        ],
        languages=[
            {"language": "English", "proficiency": "Native"},
            {"language": "Spanish", "proficiency": "Conversational"},
            {"language": "French", "proficiency": "Basic"}
        ]
    )


def get_sample_job_description() -> JobDescription:
    """Get sample job description for testing."""
    return JobDescription(
        title="Senior AI Engineer",
        company="InnovateTech Solutions",
        location="San Francisco, CA",
        employment_type="Full-time",
        description="""
        We are seeking a Senior AI Engineer to join our cutting-edge AI team. You will be responsible for designing, 
        developing, and deploying machine learning models that power our next-generation products. The ideal candidate 
        will have strong experience in deep learning, computer vision, and natural language processing.
        
        Key Responsibilities:
        - Design and implement machine learning models for various applications
        - Work with large-scale datasets and distributed computing systems
        - Collaborate with cross-functional teams including data scientists, product managers, and engineers
        - Lead technical projects and mentor junior team members
        - Stay up-to-date with the latest AI/ML research and technologies
        - Optimize model performance and scalability
        """,
        requirements=[
            "Master's degree in Computer Science, AI, or related field",
            "5+ years of experience in machine learning and AI",
            "Strong programming skills in Python",
            "Experience with deep learning frameworks (PyTorch, TensorFlow)",
            "Experience with cloud platforms (AWS, GCP, or Azure)",
            "Strong understanding of statistics and mathematics",
            "Experience with data preprocessing and feature engineering",
            "Knowledge of software engineering best practices"
        ],
        preferred_qualifications=[
            "PhD in Computer Science or related field",
            "Experience with computer vision or NLP",
            "Experience with distributed computing (Spark, Hadoop)",
            "Experience with containerization (Docker, Kubernetes)",
            "Experience with MLOps and model deployment",
            "Strong communication and leadership skills",
            "Experience in agile development methodologies",
            "Publications in top-tier AI/ML conferences"
        ]
    )


def get_sample_matching_request() -> MatchingRequest:
    """Get sample matching request for testing."""
    return MatchingRequest(
        cv_data=get_sample_cv_data(),
        job_description=get_sample_job_description()
    )


if __name__ == "__main__":
    # Example usage
    cv_data = get_sample_cv_data()
    job_desc = get_sample_job_description()
    request = get_sample_matching_request()
    
    print("Sample CV Data:")
    print(f"Name: {cv_data.personal_info.get('name')}")
    print(f"Skills: {', '.join(cv_data.skills[:5])}...")
    print(f"Experience: {len(cv_data.experience)} positions")
    
    print("\nSample Job Description:")
    print(f"Title: {job_desc.title}")
    print(f"Company: {job_desc.company}")
    print(f"Requirements: {len(job_desc.requirements)} items")
