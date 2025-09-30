#!/usr/bin/env python3
"""
Simple test to verify profiling is working.
"""

import asyncio
import json
import httpx

async def test_simple():
    """Simple test with minimal data."""
    
    test_data = {
        "data of CV": {"skills": ["Python"]},
        "JD": {"title": "Python Developer", "description": "Need Python skills"}
    }
    
    print("🧪 Simple Profiling Test")
    print("=" * 40)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:8000/match",
            headers={"Content-Type": "application/json"},
            content=json.dumps(test_data)
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {list(data.keys())}")
            
            if "profiling" in data:
                profiling = data["profiling"]
                print(f"Profiling keys: {list(profiling.keys())}")
                print(f"Total time: {profiling.get('total_time', 0):.4f}s")
                print(f"Timings count: {len(profiling.get('timings', []))}")
                
                for timing in profiling.get('timings', []):
                    print(f"  {timing['name']}: {timing['duration']:.4f}s")
            else:
                print("No profiling data found")
                print(f"Available keys: {list(data.keys())}")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_simple())
