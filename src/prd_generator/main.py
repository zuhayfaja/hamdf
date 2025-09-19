#!/usr/bin/env python
import sys
import warnings
import os
import asyncio
from typing import Dict, Any, Optional

from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from prd_generator.crew import PrdGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI(title="PRD Agent System", description="AI-powered PRD and Development Guide Generator")
crew_instance = None

# Create static directories
outputs_dir = Path("outputs")
outputs_dir.mkdir(exist_ok=True)
static_dir = Path("static")
static_dir.mkdir(exist_ok=True, parents=True)

@app.on_event("startup")
async def create_crew():
    """Create crew instance on startup to avoid repeated initialization."""
    global crew_instance
    crew_instance = PrdGenerator()


@app.get("/health", summary="Health Check", description="Check if the PRD Agent service is running")
async def health_check():
    """Health check endpoint for Railway monitoring."""
    return {
        "status": "healthy",
        "service": "PRD Agent System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "status_code": 200
    }


@app.get("/", response_class=HTMLResponse, summary="PRD Agent Web Interface")
async def web_interface():
    """Serve the main web interface."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI PRD & Development Guide Generator</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 20px rgba(0,0,0,0.1); }
            .header { text-align: center; margin-bottom: 40px; }
            .logo { color: #3b82f6; font-size: 2em; margin-bottom: 10px; }
            textarea { width: 100%; min-height: 200px; padding: 15px; border: 2px solid #e2e8f0; border-radius: 8px; font-size: 16px; margin-bottom: 20px; resize: vertical; }
            button { background: #3b82f6; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 18px; font-weight: 600; cursor: pointer; transition: background 0.3s ease; }
            button:hover { background: #2563eb; }
            button:disabled { background: #94a3b8; cursor: not-allowed; }
            .status { margin-top: 30px; padding: 20px; border-radius: 8px; display: none; }
            .status.success { background: #d1fae5; color: #047857; border: 1px solid #34d399; }
            .status.error { background: #fee2e2; color: #dc2626; border: 1px solid #f87171; }
            .loading { text-align: center; color: #6b7280; }
            .loading::after { content: ''; animation: spin 1s linear infinite; }
            @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
            .spinner { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #3b82f6; border-radius: 50%; animation: spin 1s linear infinite; }
            .features { margin: 40px 0; padding-left: 20px; }
            .features h3 { color: #1f2937; }
            .features ul { color: #4b5563; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀 PRD Agent</div>
                <h1>AI-Powered PRD & Development Guide Generator</h1>
                <p>Transform your app ideas into comprehensive Product Requirements Documents and detailed development roadmaps using advanced AI agents.</p>
            </div>

            <div class="features">
                <h3>✨ What You Can Generate:</h3>
                <ul>
                    <li><strong>Product Requirements Documents</strong> (8000+ words) - Complete stakeholder analysis, user stories, and technical specifications</li>
                    <li><strong>Technology Stack Recommendations</strong> - Open-source focused with cost analysis and scalability insights</li>
                    <li><strong>Development Roadmaps</strong> - 30-week implementation plans with sprint breakdowns and timelines</li>
                    <li><strong>Quality Reviews</strong> - Automated validation and improvement suggestions</li>
                </ul>
            </div>

            <form id="prdForm">
                <label for="ideaInput">
                    <strong>Describe Your App/Web Idea:</strong><br>
                    <small>Be specific about features, target users, and business goals</small>
                </label>
                <textarea id="ideaInput" name="idea_description" placeholder="Example: A mobile app for tracking daily habits with social sharing, gamification, AI-powered recommendations, and progress analytics. Target users are millennials focused on personal development."></textarea>

                <button type="submit" id="generateBtn">Generate PRD & Development Guide</button>
            </form>

            <div id="status" class="status">
                <div id="statusContent"></div>
            </div>
        </div>

        <script>
            const form = document.getElementById('prdForm');
            const button = document.getElementById('generateBtn');
            const status = document.getElementById('status');
            const statusContent = document.getElementById('statusContent');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();

                const ideaDescription = document.getElementById('ideaInput').value.trim();

                if (!ideaDescription) {
                    showStatus('error', 'Please describe your app idea first.');
                    return;
                }

                if (ideaDescription.length < 20) {
                    showStatus('error', 'Please provide a more detailed description (at least 20 characters).');
                    return;
                }

                // Show loading state
                showLoading();

                try {
                    const response = await fetch('/generate-prd', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            idea_description: ideaDescription,
                            timestamp: new Date().toISOString(),
                            session_id: `web_${Date.now()}`
                        })
                    });

                    if (!response.ok) {
                        const errorData = await response.json();
                        throw new Error(errorData.detail || 'Failed to generate PRD');
                    }

                    const result = await response.json();
                    showStatus('success', `✅ PRD Generation Complete!\\n\\n📊 Documents saved:\\n• Product Requirements Document\\n• Technology Stack Recommendations\\n• Development Guide\\n• Quality Review Report\\n\\nAll files generated successfully!`);

                } catch (error) {
                    console.error('Generation error:', error);
                    showStatus('error', `❌ Generation Failed: ${error.message}`);
                } finally {
                    hideLoading();
                }
            });

            function showLoading() {
                button.disabled = true;
                button.innerHTML = '<div class="spinner" style="margin-right: 10px;"></div> Generating... This may take 3-5 minutes';
                status.style.display = 'block';
                status.className = 'status loading';
                statusContent.innerHTML = '🤖 Initializing AI agents and generating your customized PRD...';
            }

            function hideLoading() {
                button.disabled = false;
                button.innerHTML = 'Generate PRD & Development Guide';
            }

            function showStatus(type, message) {
                status.style.display = 'block';
                status.className = `status ${type}`;
                statusContent.innerHTML = message.replace(/\\n/g, '<br>');
            }
        </script>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.post("/generate-prd", summary="Generate PRD", description="Generate a complete PRD and development guide for your idea")
async def generate_prd(request: Request):
    """Generate PRD and development guide for the given idea."""
    try:
        data = await request.json()
        idea_description = data.get("idea_description", "")
        timestamp = data.get("timestamp", datetime.now().isoformat())
        session_id = data.get("session_id", f"api_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

        if not idea_description or len(idea_description.strip()) < 10:
            raise HTTPException(status_code=400, detail="Idea description is required (minimum 10 characters)")

        print(f"🚀 Processing PRD request: {idea_description[:100]}...")

        # Prepare inputs
        inputs = {
            'idea_description': idea_description.strip(),
            'timestamp': timestamp,
            'session_id': session_id
        }

        # Use the global crew instance
        if crew_instance is None:
            raise HTTPException(status_code=500, detail="PRD Generator service not initialized")

        # Generate documents (this may take several minutes)
        result = crew_instance.crew().kickoff(inputs=inputs)

        return {
            "status": "completed",
            "message": "PRD and development guide generated successfully",
            "session_id": session_id,
            "timestamp": timestamp,
            "result_summary": "Generated: PRD, Technology Stack, Development Guide, Quality Review"
        }

    except Exception as e:
        print(f"❌ PRD Generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PRD generation failed: {str(e)}")


@app.get("/files", summary="List Generated Files")
async def list_generated_files():
    """List all generated files in the outputs directory."""
    try:
        files = []
        if outputs_dir.exists():
            for file_path in outputs_dir.glob("*.md"):
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        return {
            "files": files,
            "total": len(files)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


def run():
    """Run the web service."""
    print("🚀 Starting PRD Agent Web Service...")
    import uvicorn

    # Get port from environment (Railway provides this)
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    print(f"🌐 Service will be available at http://{host}:{port}")
    print("📝 Access the web interface at the root URL")

    uvicorn.run(
        "prd_generator.main:app",
        host=host,
        port=port,
        log_level="info",
        reload=False
    )


def train():
    """Train the crew for a given number of iterations."""
    inputs = {
        "idea_description": "Training session for PRD generation",
        'timestamp': datetime.now().isoformat(),
        'session_id': f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    try:
        global crew_instance
        if crew_instance is None:
            crew_instance = PrdGenerator()
        crew_instance.crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay the crew execution from a specific task."""
    try:
        global crew_instance
        if crew_instance is None:
            crew_instance = PrdGenerator()
        crew_instance.crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test the crew execution and returns the results."""
    inputs = {
        "idea_description": "Test session for PRD generation",
        'timestamp': datetime.now().isoformat(),
        'session_id': f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }

    try:
        global crew_instance
        if crew_instance is None:
            crew_instance = PrdGenerator()
        crew_instance.crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
