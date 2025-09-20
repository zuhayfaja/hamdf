#!/usr/bin/env python
"""
GitHub Authentication Testing Script
Test GitHub connectivity and authentication before pushing
"""

import subprocess
import sys
import os
from pathlib import Path

def check_git_config():
    """Check Git configuration."""
    print("🔧 Checking Git Configuration...")

    try:
        # Check Git user name
        result = subprocess.run(['git', 'config', '--global', 'user.name'],
                              capture_output=True, text=True, check=True)
        print(f"✅ Git User Name: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("❌ Git user.name not set")
        print("   To set: git config --global user.name 'Your Name'")
        return False

    try:
        # Check Git user email
        result = subprocess.run(['git', 'config', '--global', 'user.email'],
                              capture_output=True, text=True, check=True)
        user_email = result.stdout.strip()
        print(f"✅ Git User Email: {user_email}")
    except subprocess.CalledProcessError:
        print("❌ Git user.email not set")
        print("   To set: git config --global user.email 'your.email@example.com'")
        return False

    print(f"   Git should work with: https://github.com/moijusk")
    return True

def test_github_connection():
    """Test GitHub repository access."""
    print("\n🌐 Testing GitHub Connection...")

    try:
        # Try to connect to the repository (without pushing)
        result = subprocess.run(['git', 'ls-remote', '--heads', 'https://github.com/moijusk/prd-agent-system.git'],
                              capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ GitHub repository accessible!")
            # Parse output to get branch information
            lines = result.stdout.strip().split('\n')
            branches = [line.split('\t')[1] for line in lines if line]
            print(f"   Available branches: {branches}")
            return True
        else:
            print(f"❌ GitHub repository not accessible: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Connection timeout (check internet connection)")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def repository_creation_check():
    """Check if repository actually exists."""
    print("\n📋 Repository Status Check...")

    # Check if this is the first push (if it fails, repository might not exist)
    # This is just informational
    print("   If this is a new repository, make sure:")
    print("   1. Repository is created on GitHub")
    print("   2. Spelling is exact: 'prd-agent-system'")
    print("   3. Repository is public or you're authenticated properly")

def recommend_auth_methods():
    """Recommend authentication methods."""
    print("\n🔐 GitHub Authentication Options:")

    print("\n1. GitHub CLI Authentication (Recommended):")
    print("   gh auth login")
    print("   Follow the prompts to authenticate")

    print("\n2. Personal Access Token (PAT):")
    print(f"   • Go to: github.com/settings/tokens")
    print("   • Generate new token with repo permissions"
    print("   • Use as password when Git asks for authentication"

    print("\n3. SSH Key (Alternative):")
    print("   • Generate: ssh-keygen -t ed25519 -C 'your_email@example.com'")
    print("   • Add to GitHub: github.com/settings/keys"
    print("   • Use: git remote set-url origin git@github.com:moijusk/prd-agent-system.git"

    print("\n4. Verify Everything:"
    print("   • Check: git remote -v"
    print("   • Check: gh auth status (if using GitHub CLI")

def test_full_push_simulation():
    """Test full push conditions."""
    print("\n🚀 Final Push Readiness Test...")

    issues = []

    # Check working directory
    git_dir = Path(".git")
    if not git_dir.exists():
        issues.append("❌ Not in a Git repository")

    # Check if we can get repository info
    try:
        result = subprocess.run(['git', 'status', '--porcelain'],
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("   ⚠️  Working directory has uncommitted changes")
        else:
            print("   ✅ Working directory is clean")
    except subprocess.CalledProcessError:
        issues.append("❌ Git status failed")

    # Check master/main branch
    try:
        result = subprocess.run(['git', 'branch', '--show-current'],
                              capture_output=True, text=True, check=True)
        current_branch = result.stdout.strip()
        print(f"   ✅ Current branch: {current_branch}")
    except subprocess.CalledProcessError:
        issues.append("❌ Cannot determine current branch")

    # Check remote
    try:
        result = subprocess.run(['git', 'remote', '-v'],
                              capture_output=True, text=True, check=True)
        remotes = result.stdout.strip()
        if 'origin' in remotes:
            print("   ✅ Remote 'origin' configured")
        else:
            issues.append("❌ No origin remote configured")
    except subprocess.CalledProcessError:
        issues.append("❌ Cannot check remotes")

    # Summary
    print("\n📊 Push Readiness Summary:")
    if issues:
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✅ All basic checks passed!")
        print("   🔥 Ready to push! Your Git configuration looks good.")

    return len(issues) == 0

def main():
    """Main function."""
    print("🔐 GITHUB AUTHENTICATION DIAGNOSTIC")
    print("="*50)

    # Test all components
    git_ok = check_git_config()
    github_ok = test_github_connection()
    push_ok = test_full_push_simulation()

    print("\n" + "="*50)
    print("📋 FINAL DIAGNOSIS:")

    if github_ok and push_ok:
        print("🎉 GREEN LIGHT: Everything looks good!")
        print("   Try: git push -u origin main")
    elif git_ok and not github_ok:
        print("🔧 YELLOW LIGHT: Git OK, GitHub access issue")
        print("   Focus on GitHub authentication (see recommendations above)")
    else:
        print("🔴 RED LIGHT: Multiple issues detected")
        print("   Address the configuration issues above first")

    print("\n💡 Next Steps:")
    print("1. Address any ❌ issues shown above")
    print("2. Use one of the authentication methods recommended")
    print("3. Try the push command: git push -u origin main")
    print("4. If still failing, Railway direct integration is the best backup plan")

    repository_creation_check()

if __name__ == "__main__":
    main()
