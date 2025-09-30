#!/usr/bin/env python3
"""
Detailed Server-Side Profiling Test
Shows internal processing breakdown with server-side profiling.
"""

import asyncio
import json
import httpx
import time

async def test_detailed_profiling():
    """Test with detailed server-side profiling."""
    
    test_data = {
        "data of CV": {
            "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
            "experience": [
                {"title": "Software Developer", "company": "Tech Corp", "duration": "2 years"},
                {"title": "Junior Developer", "company": "Startup Inc", "duration": "1 year"}
            ],
            "education": [
                {"degree": "Bachelor of Computer Science", "institution": "University of Tech"}
            ]
        },
        "JD": {
            "title": "Senior Full Stack Developer",
            "description": "Looking for an experienced full-stack developer with strong Python and JavaScript skills. Must have experience with React and Node.js. Database experience with MongoDB preferred.",
            "requirements": [
                "Python programming (3+ years)",
                "JavaScript/TypeScript",
                "React framework",
                "Node.js backend development",
                "Database design and optimization",
                "API development and integration"
            ],
            "preferred_qualifications": [
                "MongoDB experience",
                "Cloud deployment (AWS/Azure)",
                "Team leadership experience"
            ]
        }
    }
    
    print("🔍 Detailed Server-Side Profiling Test")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        start_time = time.time()
        
        response = await client.post(
            "http://localhost:8000/match",
            headers={"Content-Type": "application/json"},
            content=json.dumps(test_data)
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Request completed successfully")
            print(f"Total Time: {total_time:.4f}s")
            print(f"Server Processing Time: {data.get('processing_time', 0):.4f}s")
            print(f"Network Overhead: {total_time - data.get('processing_time', 0):.4f}s")
            
            # Display profiling data if available
            if "profiling" in data:
                profiling = data["profiling"]
                print(f"\n🔍 Server-Side Profiling Breakdown:")
                print(f"Session ID: {profiling.get('session_id', 'N/A')}")
                print(f"Total Server Time: {profiling.get('total_time', 0):.4f}s")
                
                print(f"\n⏱️  Internal Processing Steps:")
                for timing in profiling.get('timings', []):
                    indent = "  " if timing.get('parent') else ""
                    print(f"{indent}{timing['name']:<30} {timing['duration']:>8.4f}s ({timing['percentage']:>5.1f}%) {timing.get('details', '')}")
                
                print(f"\n🔥 Server Bottlenecks:")
                for i, (name, duration) in enumerate(profiling.get('bottlenecks', []), 1):
                    print(f"   {i}. {name}: {duration:.4f}s")
                
                # Analysis
                print(f"\n📊 Performance Analysis:")
                api_calls = [t for t in profiling.get('timings', []) if 'API Call' in t['name']]
                if api_calls:
                    total_api_time = sum(t['duration'] for t in api_calls)
                    print(f"   Total API Call Time: {total_api_time:.4f}s")
                    print(f"   API Calls as % of total: {(total_api_time/profiling.get('total_time', 1)*100):.1f}%")
                
                prompt_construction = next((t for t in profiling.get('timings', []) if t['name'] == 'Prompt Construction'), None)
                if prompt_construction:
                    print(f"   Prompt Construction: {prompt_construction['duration']:.4f}s")
                
                json_parsing = next((t for t in profiling.get('timings', []) if t['name'] == 'JSON Parsing'), None)
                if json_parsing:
                    print(f"   JSON Parsing: {json_parsing['duration']:.4f}s")
            
            # Display analysis results
            analysis = data.get("analysis", {})
            if analysis:
                print(f"\n📋 Analysis Results:")
                print(f"   Compatibility Score: {analysis.get('overall_analysis', {}).get('compatibility_score', 0)}")
                print(f"   Matched Requirements: {len(analysis.get('matched_requirements', []))}")
                print(f"   Missing Requirements: {len(analysis.get('missing_requirements', []))}")
                
                # Show some matched requirements
                matched = analysis.get('matched_requirements', [])
                if matched:
                    print(f"\n✅ Matched Requirements:")
                    for req in matched[:3]:  # Show first 3
                        print(f"   - {req.get('requirement', 'N/A')} (Score: {req.get('relevance_score', 0)})")
                
                # Show some missing requirements
                missing = analysis.get('missing_requirements', [])
                if missing:
                    print(f"\n❌ Missing Requirements:")
                    for req in missing[:3]:  # Show first 3
                        print(f"   - {req.get('requirement', 'N/A')} ({req.get('importance', 'N/A')})")
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")

async def main():
    """Main test function."""
    await test_detailed_profiling()

if __name__ == "__main__":
    asyncio.run(main())
