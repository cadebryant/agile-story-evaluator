#!/usr/bin/env python3
"""
Startup script for Agile Story Evaluator
"""

import os
import sys

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import gradio
        import openai
        from dotenv import load_dotenv
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check if OpenAI API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured.")
        print("   The app will work but AI analysis features will be disabled.")
        print("   To enable AI features:")
        print("   1. Get an API key from: https://platform.openai.com/api-keys")
        print("   2. Create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Agile Story Evaluator...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check API key
    has_api_key = check_api_key()
    
    if has_api_key:
        print("✅ All systems ready! Starting full application...")
    else:
        print("ℹ️  Starting application with limited features...")
    
    # Import and run the main application
    try:
        from agile_story_evaluator import create_gradio_interface
        interface = create_gradio_interface()
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nTry running the demo instead:")
        print("python demo_evaluator.py")

if __name__ == "__main__":
    main()
