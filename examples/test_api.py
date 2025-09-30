"""Test script for the CV matching API."""

import asyncio
import json
import httpx
from typing import Dict, Any

from sample_cv_data import get_sample_matching_request


async def test_cv_matching_api():
    """Test the CV matching API with sample data."""
    
    # Get sample data
    request_data = get_sample_matching_request()
    
    # Convert to dict for JSON serialization
    request_dict = request_data.model_dump()
    
    # API endpoint
    url = "http://localhost:8000/match"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            print("Sending CV matching request...")
            print(f"CV Name: {request_dict['cv_data']['personal_info']['name']}")
            print(f"Job Title: {request_dict['job_description']['title']}")
            print(f"Company: {request_dict['job_description']['company']}")
            print("-" * 50)
            
            response = await client.post(url, json=request_dict)
            
            if response.status_code == 200:
                result = response.json()
                
                print("✅ CV Matching Analysis Complete!")
                print(f"Processing Time: {result.get('processing_time', 'N/A'):.2f} seconds")
                print(f"Model Used: {result.get('model_used', 'N/A')}")
                print("-" * 50)
                
                # Display analysis results
                analysis = result['analysis']
                overall = analysis['overall_analysis']
                
                print(f"🎯 Overall Compatibility Score: {overall['compatibility_score']}%")
                print(f"✅ Matched Requirements: {len(analysis['matched_requirements'])}")
                print(f"❌ Missing Requirements: {len(analysis['missing_requirements'])}")
                print("-" * 50)
                
                # Show strengths
                print("💪 Key Strengths:")
                for strength in overall['strengths'][:3]:
                    print(f"  • {strength}")
                
                # Show gaps
                print("\n⚠️  Main Gaps:")
                for gap in overall['gaps'][:3]:
                    print(f"  • {gap}")
                
                # Show recommendations
                print("\n💡 Recommendations:")
                for rec in overall['recommendations'][:3]:
                    print(f"  • {rec}")
                
                # Show detailed breakdown
                breakdown = analysis['detailed_breakdown']
                print(f"\n📊 Detailed Breakdown:")
                print(f"  • Education Match: {breakdown['education_match']}%")
                print(f"  • Skills Match: {breakdown['skills_match']}%")
                print(f"  • Experience Match: {breakdown['experience_match']}%")
                print(f"  • Tools/Frameworks Match: {breakdown['tools_frameworks_match']}%")
                
                # Show some matched requirements
                print(f"\n✅ Top Matched Requirements:")
                for match in analysis['matched_requirements'][:3]:
                    print(f"  • {match['requirement']} (Strength: {match['match_strength']}, Score: {match['relevance_score']}/10)")
                
                # Show some missing requirements
                print(f"\n❌ Critical Missing Requirements:")
                critical_missing = [req for req in analysis['missing_requirements'] if req['importance'] == 'critical']
                for missing in critical_missing[:3]:
                    print(f"  • {missing['requirement']}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except httpx.TimeoutException:
            print("❌ Request timed out. The analysis might be taking longer than expected.")
        except httpx.ConnectError:
            print("❌ Could not connect to the API. Make sure the server is running on http://localhost:8000")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


async def test_summary_endpoint():
    """Test the summary endpoint."""
    
    request_data = get_sample_matching_request()
    request_dict = request_data.model_dump()
    
    url = "http://localhost:8000/match/summary"
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            print("\n" + "="*60)
            print("Testing Summary Endpoint...")
            print("="*60)
            
            response = await client.post(url, json=request_dict)
            
            if response.status_code == 200:
                summary = response.json()
                
                print("📋 Matching Summary:")
                print(f"  • Compatibility Score: {summary['compatibility_score']}%")
                print(f"  • Matched Requirements: {summary['total_matched_requirements']}")
                print(f"  • Missing Requirements: {summary['total_missing_requirements']}")
                print(f"  • Critical Missing: {summary['critical_missing']}")
                print(f"  • High Strength Matches: {summary['high_strength_matches']}")
                print(f"  • Processing Time: {summary['processing_time']:.2f}s")
                print(f"  • Model Used: {summary['model_used']}")
                
            else:
                print(f"❌ Summary API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Summary test error: {e}")


async def test_health_endpoint():
    """Test the health endpoint."""
    
    async with httpx.AsyncClient() as client:
        try:
            print("\n" + "="*60)
            print("Testing Health Endpoint...")
            print("="*60)
            
            response = await client.get("http://localhost:8000/health")
            
            if response.status_code == 200:
                health = response.json()
                print(f"✅ API Health: {health['status']}")
                print(f"  • Service: {health['service']}")
                print(f"  • Version: {health['version']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Health check error: {e}")


async def main():
    """Run all tests."""
    print("🚀 Starting CV Matching API Tests")
    print("="*60)
    
    # Test health endpoint first
    await test_health_endpoint()
    
    # Test main matching endpoint
    await test_cv_matching_api()
    
    # Test summary endpoint
    await test_summary_endpoint()
    
    print("\n" + "="*60)
    print("✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
