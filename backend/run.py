#!/usr/bin/env python3
"""
Start the FastAPI backend server

Usage:
    python backend/run.py
    
Or with uvicorn directly:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""

import sys
import os

# Add parent directory to Python path so we can import src module
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
