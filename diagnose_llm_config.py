#!/usr/bin/env python3
"""
Diagnostic script to find all model configurations and determine where the old model is referenced
"""

import os
import sys
from pathlib import Path
import subprocess

def check_environment_variables():
    """Check all LLM-related environment variables."""
    print("🔍 Environment Variables:")
    env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'MODEL_NAME', 'LLM_MODEL', 'OPENROUTER_API_KEY']
    for var in env_vars:
        value = os.getenv(var, 'NOT SET')
        if 'API_KEY' in var and value != 'NOT SET':
            print(f"   {var}: ***{value[-8:]} (masked)")
        else:
            print(f"   {var}: {value}")

def find_model_references():
    """Search for all model references in the codebase."""
    print("\n🔍 Searching for model references in codebase...")

    # Search for common model patterns
    patterns = [
        'grok-4-fast:free',
        'x-ai/grok',
        'gpt-oss-120b',
        'sonoma-sky',
        'openrouter',
        'openai/gpt'
    ]

    found_references = []
    for pattern in patterns:
        try:
            result = subprocess.run(
                ['grep', '-r', '--include=*.py', '--include=*.yaml', '--include=*.md', pattern, '.'],
                capture_output=True, text=True, cwd=str(Path(__file__).parent)
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if lines and lines[0]:
                    found_references.extend(lines)
        except Exception as e:
            print(f"   Error searching for {pattern}: {e}")

    if found_references:
        print(f"   Found {len(found_references)} model references:")
        for ref in found_references[:10]:  # Show first 10
            print(f"     {ref}")
        if len(found_references) > 10:
            print(f"     ... and {len(found_references) - 10} more")
    else:
        print("   ✓ No model references found (or grep not available)")

def test_litellm_config():
    """Test what LiteLLM sees as the default configuration."""
    print("\n🔍 Testing LiteLLM configuration...")

    try:
        import litellm
        print("   LiteLLM version:", getattr(litellm, '__version__', 'unknown'))

        # Try to set up the model configuration
        print("   Testing model configuration...")
        model_resp = litellmcompletion(  # Try to use installed version
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print("   ✓ Model configuration working")

    except ImportError:
        print("   ❌ LiteLLM not installed")
    except Exception as e:
        print(f"   ❌ LiteLLM configuration error: {e}")

def check_crewai_models():
    """Check how CrewAI resolves models."""
    print("\n🔍 Testing CrewAI model resolution...")

    try:
        from crewai import Agent
        print("   ✓ CrewAI Agent import successful")

        # Test with our configuration
        agent_config = {
            "role": "Test Agent",
            "goal": "Test model configuration",
            "backstory": "Testing model setup",
            "llm": "openai/gpt-oss-120b"
        }

        print("   Creating agent with Cerebras model...")
        agent = Agent(config=agent_config)
        print("   ✅ Agent created successfully")

        # Check if we can see what LLM it's using
        if hasattr(agent, 'llm'):
            print(f"   Agent LLM: {agent.llm}")

    except Exception as e:
        print(f"   ❌ CrewAI model resolution error: {e}")

def main():
    """Run all diagnostic tests."""
    print("🚀 LLM Configuration Diagnostic Tool")
    print("=" * 50)

    check_environment_variables()
    find_model_references()
    test_litellm_config()
    check_crewai_models()

    print("\n" + "=" * 50)
    print("📋 Summary of findings:")
    print("• Check environment variables are correctly set")
    print("• Ensure all model references point to 'gpt-oss-120b'")
    print("• Clear any cached configurations")
    print("• Restart the application to pick up changes")

if __name__ == "__main__":
    main()
