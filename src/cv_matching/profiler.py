"""Server-side performance profiler for detailed timing analysis."""

import time
import functools
from typing import Dict, Any, List, Callable
from dataclasses import dataclass, field
from contextlib import contextmanager

@dataclass
class TimingEntry:
    name: str
    start_time: float
    end_time: float
    duration: float
    parent: str = ""
    details: str = ""

@dataclass
class ProfilerSession:
    session_id: str
    start_time: float
    end_time: float = 0
    timings: List[TimingEntry] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_timing(self, name: str, start: float, end: float, parent: str = "", details: str = ""):
        duration = end - start
        self.timings.append(TimingEntry(name, start, end, duration, parent, details))
    
    def get_summary(self) -> Dict[str, Any]:
        total_time = self.end_time - self.start_time if self.end_time else time.time() - self.start_time
        return {
            "session_id": self.session_id,
            "total_time": total_time,
            "timings": [
                {
                    "name": t.name,
                    "duration": t.duration,
                    "percentage": (t.duration / total_time) * 100 if total_time > 0 else 0,
                    "parent": t.parent,
                    "details": t.details
                }
                for t in self.timings
            ],
            "bottlenecks": sorted(
                [(t.name, t.duration) for t in self.timings],
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }

class ServerProfiler:
    def __init__(self):
        self.sessions: Dict[str, ProfilerSession] = {}
        self.current_session: str = None
    
    def start_session(self, session_id: str) -> str:
        """Start a new profiling session."""
        self.current_session = session_id
        self.sessions[session_id] = ProfilerSession(
            session_id=session_id,
            start_time=time.time()
        )
        return session_id
    
    def end_session(self, session_id: str = None):
        """End a profiling session."""
        sid = session_id or self.current_session
        if sid and sid in self.sessions:
            self.sessions[sid].end_time = time.time()
    
    @contextmanager
    def time_block(self, name: str, parent: str = "", details: str = ""):
        """Context manager for timing code blocks."""
        session_id = self.current_session
        if not session_id:
            yield
            return
        
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            self.sessions[session_id].add_timing(name, start_time, end_time, parent, details)
    
    def time_function(self, name: str = None, parent: str = ""):
        """Decorator for timing functions."""
        def decorator(func: Callable):
            func_name = name or f"{func.__module__}.{func.__name__}"
            
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                session_id = self.current_session
                if not session_id:
                    return await func(*args, **kwargs)
                
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    self.sessions[session_id].add_timing(
                        func_name, start_time, end_time, parent, 
                        f"args={len(args)}, kwargs={len(kwargs)}"
                    )
            
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                session_id = self.current_session
                if not session_id:
                    return func(*args, **kwargs)
                
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    end_time = time.time()
                    self.sessions[session_id].add_timing(
                        func_name, start_time, end_time, parent,
                        f"args={len(args)}, kwargs={len(kwargs)}"
                    )
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    def get_session_summary(self, session_id: str = None) -> Dict[str, Any]:
        """Get summary for a specific session."""
        sid = session_id or self.current_session
        if sid and sid in self.sessions:
            return self.sessions[sid].get_summary()
        return {}
    
    def print_session_summary(self, session_id: str = None):
        """Print detailed session summary."""
        summary = self.get_session_summary(session_id)
        if not summary:
            print("No session data available")
            return
        
        print(f"\n🔍 Profiling Session: {summary['session_id']}")
        print(f"Total Time: {summary['total_time']:.4f}s")
        print("\n⏱️  Detailed Breakdown:")
        
        for timing in summary['timings']:
            indent = "  " if timing['parent'] else ""
            print(f"{indent}{timing['name']:<30} {timing['duration']:>8.4f}s ({timing['percentage']:>5.1f}%) {timing['details']}")
        
        print("\n🔥 Top Bottlenecks:")
        for i, (name, duration) in enumerate(summary['bottlenecks'], 1):
            print(f"   {i}. {name}: {duration:.4f}s")

# Global profiler instance
profiler = ServerProfiler()

# Import asyncio for the decorator
import asyncio
