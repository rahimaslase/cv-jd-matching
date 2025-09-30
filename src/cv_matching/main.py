"""Main entry point for the CV matching application."""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from .api import run_server


def main():
    """Main entry point."""
    print("🚀 Starting CV Matching API Server")
    print("=" * 50)
    print("Make sure you have set your OPENAI_API_KEY environment variable")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
