#!/usr/bin/env python3
"""
Simple test to verify Cerebras Cloud integration via OpenAI SDK
"""

import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

def test_openai_cerebras():
    """Test the OpenAI SDK integration with Cerebras Cloud."""
    try:
        print("🧪 Testing OpenAI SDK + Cerebras Cloud Integration...")

        # Check environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")

        print(f"✓ API_KEY configured: {'Yes' if api_key else 'No'}")
        print(f"✓ BASE_URL configured: {base_url or 'default'}")

        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment")
            return False

        # Initialize OpenAI client with Cerebras endpoint
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None
        )

        # Test simple chat completion
        print("2️⃣ Testing chat completion...")
        response = client.chat.completions.create(
            model="gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": "Hello! Respond with a very short greeting."}
            ],
            max_completion_tokens=50,
            temperature=0.7
        )

        # Extract and display response
        if response.choices and response.choices[0].message:
            content = response.choices[0].message.content
            print(f"✓ Chat completion successful!")
            print(f"   Response: '{content}'")
            return True
        else:
            print("❌ Empty response from Cerebras")
            return False

    except ImportError as e:
        print(f"❌ Missing OpenAI package: {e}")
        return False
    except Exception as e:
        print(f"❌ API call failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_crewai_cerebras():
    """Test basic CrewAI instantiation with Cerebras configuration."""
    try:
        print("\n🚀 Testing CrewAI with Cerebras Configuration...")

        from prd_generator.crew import PrdGenerator

        print("1️⃣ Initializing PrdGenerator...")
        crew_instance = PrdGenerator()
        print("   ✓ Crew instance created")

        # Try to access the crew
        print("2️⃣ Testing crew creation...")
        crew = crew_instance.crew()
        print("   ✓ Crew created successfully")

        return True

    except Exception as e:
        print(f"❌ CrewAI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 OpenAI + Cerebras Cloud Integration Test")
    print("=" * 50)

    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ Loaded .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed")

    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")

    print("\n🔧 Environment Variables:")
    print(f"OPENAI_API_KEY: {'***' + os.getenv('OPENAI_API_KEY', '')[-4:] if os.getenv('OPENAI_API_KEY') else 'NOT SET'}")
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL', 'DEFAULT')}")

    # Run tests
    api_test = test_openai_cerebras()
    crewai_test = test_crewai_cerebras()

    print("\n" + "=" * 50)
    if api_test and crewai_test:
        print("🎉 ALL TESTS PASSED! Cerebras integration is working!")
        print("\n📝 You can now run the PRD generator:")
        print("   python src/prd_generator/main.py")
        sys.exit(0)
    elif api_test:
        print("⚠️  OpenAI API test passed, but CrewAI test failed.")
        print("   This indicates provider connection is working but CrewAI setup needs adjustment.")
        sys.exit(1)
    else:
        print("❌ TESTS FAILED. Check OpenAI API key and Cerebras endpoint configuration.")
        sys.exit(1)
