#!/usr/bin/env python3
"""
Alternative entry point for the BracketsTV API
"""

from index import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
