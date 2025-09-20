#!/usr/bin/env python3
"""
Test script to verify Cerebras Cloud LLM integration with CrewAI
"""

import os
import sys
import traceback
from pathlib import Path

# Add src to Python path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))

def test_cerebras_llm():
    """Test the Cerebras LLM integration."""
    try:
        print("🧪 Testing Cerebras LLM Integration...")
        print(f"CEREBRAS_API_KEY env var: {'✓ Found' if os.getenv('CEREBRAS_API_KEY') else '✗ Missing'}")

        from prd_generator.tools.cerebras_llm import CerebrasLLM

        # Initialize the Cerebras LLM
        print("1️⃣ Initializing CerebrasLLM...")
        llm = CerebrasLLM(
            model="gpt-oss-120b",
            temperature=0.7,
            max_tokens=1000  # Smaller for testing
        )
        print("   ✓ CerebrasLLM initialized successfully")

        # Test a simple call
        print("2️⃣ Testing API call...")
        test_messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Hello! Please respond with a short greeting."}
        ]

        response = llm.call(messages=test_messages)
        print(f"   ✓ API call successful! Response: '{response[:100]}...'")
        print(f"   ✓ Response length: {len(response)} characters")

        # Test different message format (CrewAI style)
        print("3️⃣ Testing CrewAI message format...")
        crewai_messages = [
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": "Write a Python function that adds two numbers and returns the result."}
        ]

        response2 = llm.call(messages=crewai_messages)
        print(f"   ✓ CrewAI format test successful! Response length: {len(response2)} characters")
        print(f"   ✓ Response preview: '{response2[:100]}...'")

        print("\n🎉 All Cerebras LLM tests passed!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you've installed the cerebras-cloud package:")
        print("   pip install cerebras-cloud>=0.5.0")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("   Full traceback:")
        traceback.print_exc()
        return False

def test_cerebras_crew_integration():
    """Test the full CrewAI + Cerebras integration."""
    try:
        print("\n🚀 Testing CrewAI + Cerebras Integration...")

        from prd_generator.crew import PrdGenerator

        print("1️⃣ Initializing PrdGenerator crew...")
        crew_instance = PrdGenerator()
        print("   ✓ Crew instance created")

        print("2️⃣ Checking agents...")
        agents = crew_instance.agents
        print(f"   ✓ Found {len(agents)} agents:")
        for i, agent in enumerate(agents, 1):
            print(f"     {i}. {agent.role}")

        print("3️⃣ Testing crew creation...")
        crew = crew_instance.crew()
        print("   ✓ Crew created successfully")

        print("\n🎉 CrewAI integration tests passed!")
        return True

    except Exception as e:
        print(f"❌ CrewAI integration test failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Cerebras Cloud LLM Integration Test")
    print("=" * 50)

    # Load environment variables from .env
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✓ Loaded .env file")
    except ImportError:
        print("⚠️  python-dotenv not installed, make sure .env variables are set manually")

    # Run tests
    success = True

    print("\n🔧 Testing Environment Setup...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")

    # Test Cerebras LLM
    if not test_cerebras_llm():
        success = False

    # Test full integration
    if not test_cerebras_crew_integration():
        success = False

    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED! Cerebras integration is ready!")
        print("\n📝 You can now run the PRD generator:")
        print("   python src/prd_generator/main.py")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED. Check the errors above.")
        sys.exit(1)
