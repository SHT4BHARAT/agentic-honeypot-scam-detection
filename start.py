#!/usr/bin/env python3
"""
Entrypoint script for Railway deployment.
Handles dynamic PORT environment variable.
"""
import os
import sys

if __name__ == "__main__":
    # Get PORT from environment, default to 8000
    port = os.environ.get("PORT", "8000")
    
    # Build uvicorn command
    cmd = f"uvicorn app:app --host 0.0.0.0 --port {port}"
    
    print(f"🚀 Starting server on port {port}")
    print(f"Command: {cmd}")
    
    # Execute uvicorn
    os.system(cmd)
