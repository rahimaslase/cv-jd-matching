#!/usr/bin/env python3
"""
Performance Test for CV Matching API
Measures response time at each step to identify bottlenecks.
"""

import asyncio
import time
import json
import httpx
import sys
from typing import Dict, Any, List
from dataclasses import dataclass
from contextlib import asynccontextmanager

@dataclass
class TimingResult:
    step_name: str
    start_time: float
    end_time: float
    duration: float
    details: str = ""

class PerformanceProfiler:
    def __init__(self):
        self.timings: List[TimingResult] = []
        self.start_time = time.time()
    
    def add_timing(self, step_name: str, start: float, end: float, details: str = ""):
        duration = end - start
        self.timings.append(TimingResult(step_name, start, end, duration, details))
        print(f"⏱️  {step_name}: {duration:.4f}s {details}")
    
    def get_summary(self) -> Dict[str, Any]:
        total_time = time.time() - self.start_time
        return {
            "total_time": total_time,
            "step_breakdown": [
                {
                    "step": t.step_name,
                    "duration": t.duration,
                    "percentage": (t.duration / total_time) * 100,
                    "details": t.details
                }
                for t in self.timings
            ],
            "bottlenecks": sorted(
                [(t.step_name, t.duration) for t in self.timings],
                key=lambda x: x[1],
                reverse=True
            )[:3]
        }

async def test_api_performance():
    """Test API performance with detailed timing breakdown."""
    
    profiler = PerformanceProfiler()
    
    # Test data
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
    
    print("🚀 Starting Performance Test")
    print("=" * 60)
    
    # Step 1: Data Preparation
    step_start = time.time()
    json_data = json.dumps(test_data)
    step_end = time.time()
    profiler.add_timing("Data Preparation", step_start, step_end, f"JSON serialization ({len(json_data)} bytes)")
    
    # Step 2: HTTP Request Setup
    step_start = time.time()
    async with httpx.AsyncClient(timeout=120.0) as client:
        step_end = time.time()
        profiler.add_timing("HTTP Client Setup", step_start, step_end, "AsyncClient initialization")
        
        # Step 3: Network Request
        step_start = time.time()
        try:
            response = await client.post(
                "http://localhost:8000/match",
                headers={"Content-Type": "application/json"},
                content=json_data
            )
            step_end = time.time()
            profiler.add_timing("Network Request", step_start, step_end, f"HTTP POST to /match (Status: {response.status_code})")
            
            # Step 4: Response Processing
            step_start = time.time()
            if response.status_code == 200:
                response_data = response.json()
                step_end = time.time()
                profiler.add_timing("Response Processing", step_start, step_end, f"JSON parsing ({len(response.text)} bytes)")
                
                # Step 5: Analysis Extraction
                step_start = time.time()
                analysis = response_data.get("analysis", {})
                processing_time = response_data.get("processing_time", 0)
                model_used = response_data.get("model_used", "unknown")
                step_end = time.time()
                profiler.add_timing("Analysis Extraction", step_start, step_end, f"Data extraction from response")
                
                # Step 6: Results Validation
                step_start = time.time()
                matched_count = len(analysis.get("matched_requirements", []))
                missing_count = len(analysis.get("missing_requirements", []))
                compatibility_score = analysis.get("overall_analysis", {}).get("compatibility_score", 0)
                step_end = time.time()
                profiler.add_timing("Results Validation", step_start, step_end, f"Validation: {matched_count} matched, {missing_count} missing, score: {compatibility_score}")
                
                print("\n📊 API Response Analysis:")
                print(f"   Model Used: {model_used}")
                print(f"   Server Processing Time: {processing_time:.4f}s")
                print(f"   Compatibility Score: {compatibility_score}")
                print(f"   Matched Requirements: {matched_count}")
                print(f"   Missing Requirements: {missing_count}")
                
            else:
                step_end = time.time()
                profiler.add_timing("Error Response", step_start, step_end, f"HTTP {response.status_code}: {response.text[:100]}")
                
        except httpx.TimeoutException:
            step_end = time.time()
            profiler.add_timing("Network Timeout", step_start, step_end, "Request timed out after 120s")
        except Exception as e:
            step_end = time.time()
            profiler.add_timing("Network Error", step_start, step_end, f"Error: {str(e)[:100]}")
    
    # Generate Summary
    print("\n" + "=" * 60)
    print("📈 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    summary = profiler.get_summary()
    
    print(f"Total Test Time: {summary['total_time']:.4f}s")
    print(f"Server Processing Time: {processing_time:.4f}s" if 'processing_time' in locals() else "N/A")
    
    print("\n⏱️  Step-by-Step Breakdown:")
    for step in summary['step_breakdown']:
        print(f"   {step['step']:<20} {step['duration']:>8.4f}s ({step['percentage']:>5.1f}%) {step['details']}")
    
    print("\n🔥 Top Bottlenecks:")
    for i, (step, duration) in enumerate(summary['bottlenecks'], 1):
        print(f"   {i}. {step}: {duration:.4f}s")
    
    # Performance Analysis
    print("\n🔍 Performance Analysis:")
    if 'processing_time' in locals():
        network_time = summary['total_time'] - processing_time
        print(f"   Network Overhead: {network_time:.4f}s ({(network_time/summary['total_time']*100):.1f}%)")
        print(f"   Server Processing: {processing_time:.4f}s ({(processing_time/summary['total_time']*100):.1f}%)")
        
        if processing_time > 30:
            print("   ⚠️  WARNING: Server processing time > 30s - consider optimization")
        if network_time > 5:
            print("   ⚠️  WARNING: Network overhead > 5s - check connection")
    
    return summary

async def test_multiple_requests():
    """Test multiple requests to measure consistency."""
    print("\n🔄 Testing Multiple Requests for Consistency")
    print("=" * 60)
    
    test_data = {
        "data of CV": {"skills": ["Python"]},
        "JD": {"title": "Python Developer", "description": "Need Python skills"}
    }
    
    times = []
    for i in range(3):
        print(f"\nRequest {i+1}/3:")
        start = time.time()
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    "http://localhost:8000/match",
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(test_data)
                )
                end = time.time()
                duration = end - start
                times.append(duration)
                
                if response.status_code == 200:
                    data = response.json()
                    server_time = data.get("processing_time", 0)
                    print(f"   Total: {duration:.4f}s, Server: {server_time:.4f}s, Network: {duration-server_time:.4f}s")
                else:
                    print(f"   Failed: {response.status_code} - {duration:.4f}s")
                    
            except Exception as e:
                end = time.time()
                duration = end - start
                times.append(duration)
                print(f"   Error: {str(e)[:50]} - {duration:.4f}s")
        
        await asyncio.sleep(1)  # Brief pause between requests
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        print(f"\n📊 Consistency Results:")
        print(f"   Average: {avg_time:.4f}s")
        print(f"   Min: {min_time:.4f}s")
        print(f"   Max: {max_time:.4f}s")
        print(f"   Variance: {max_time - min_time:.4f}s")

async def main():
    """Main test function."""
    print("🧪 CV Matching API Performance Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code != 200:
                print("❌ Server health check failed")
                return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Make sure the server is running on http://localhost:8000")
        return
    
    print("✅ Server is running")
    
    # Run performance test
    await test_api_performance()
    
    # Run consistency test
    await test_multiple_requests()
    
    print("\n✅ Performance test completed!")

if __name__ == "__main__":
    asyncio.run(main())
