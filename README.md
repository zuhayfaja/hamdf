# 🚀 AI PRD & Development Guide Generator

A sophisticated multi-agent AI system that transforms app and web ideas into comprehensive Product Requirements Documents (PRDs) and detailed development guides using advanced AI agents.

## 🎯 Features

- **5 Specialized AI Agents**: Requirements Analyst, PRD Architect, Tech Stack Advisor, Development Planner, Quality Reviewer
- **Comprehensive Documents**: Generate 8000+ word PRDs with complete stakeholder analysis and technical specifications
- **Technology Recommendations**: Open-source focused tech stack suggestions with cost analysis
- **Development Roadmaps**: 30-week implementation plans with sprint breakdowns
- **Quality Assurance**: Automated validation and improvement suggestions
- **Web Interface**: User-friendly web interface for easy access
- **API Endpoints**: Programmatic access for integrations
- **Production Ready**: Optimized for cloud deployment with health checks

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key
- Pinecone API Key (vector database)
- Git (for version control)

### Local Development

```bash
# Clone and navigate to your project directory
cd prd-agent-system/prd_generator

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your_openai_key"
export PINECONE_API_KEY="your_pinecone_key"

# Run the service
python -m prd_generator.main
```

### Access the Application
- **Web Interface**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **API Endpoints**: http://localhost:8000/generate-prd

## ☁️ Cloud Deployment

### Railway (Recommended - Super Fast)
1. **Create GitHub Repository**: Push your project files to GitHub
2. **Connect to Railway**: Link your GitHub repo to Railway dashboard
3. **Configure Environment Variables**:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
4. **Deploy**: Railway automatically builds and deploys your Docker container
5. **Access**: Your PRD Agent service will be live in minutes!

### Other Cloud Providers
The system includes Docker configuration for easy deployment to:
- **Google Cloud Run**
- **Azure Container Instances**
- **AWS ECS**
- **Heroku**
- **Render**

## 📋 Usage Examples

### Web Interface
1. Open your browser to the application URL
2. Describe your app idea in detail
3. Click "Generate PRD & Development Guide"
4. Wait 3-5 minutes for AI processing
5. Download or view generated documents

### API Usage
```bash
curl -X POST "http://your-app-url/generate-prd" \\
     -H "Content-Type: application/json" \\
     -d '{
       "idea_description": "A mobile habit tracking app with social features",
       "session_id": "my_project_001"
     }'
```

### CLI Usage
```bash
# From Python
from prd_generator.crew import PrdGenerator

crew = PrdGenerator()
result = crew.crew().kickoff({
    "idea_description": "Your app idea here..."
})
```

## 🏗️ System Architecture

### AI Agents
1. **Requirements Analyst** - Analyzes and structures user ideas
2. **PRD Architect** - Creates comprehensive specifications
3. **Tech Stack Advisor** - Recommends optimal technologies
4. **Development Planner** - Plans implementation phases
5. **Quality Reviewer** - Validates and improves output

### Workflow
```
User Idea → Requirements Analysis → PRD Generation → Technology Recommendations → Development Guide → Quality Review → Final Deliverables
```

## 📁 Project Structure

```
prd-generator/
├── Dockerfile              # Container configuration
├── railway.json            # Railway deployment config
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
├── .env                    # Environment variables
├── src/prd_generator/      # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI web service
│   ├── crew.py            # CrewAI orchestration
│   ├── config/            # Agent and task configurations
│   ├── tools/             # Custom AI tools
│   └── ...
├── tests/                  # Test suites
├── outputs/               # Generated PRD files
├── knowledge/             # Knowledge base files
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY="your_openai_api_key_here"
PINECONE_API_KEY="your_pinecone_api_key_here"

# Optional
PINECONE_ENVIRONMENT="us-east-1"
DEBUG="false"
LOG_LEVEL="INFO"
OUTPUT_DIRECTORY="./outputs"
```

### API Keys Setup
1. **OpenRouter**: Get key from [OpenRouter](https://openrouter.ai/) - provides access to Sonoma Sky Alpha and other models
2. **Pinecone**: Get key from [Pinecone Console](https://app.pinecone.io/)

## 📊 Generated Outputs

Each PRD generation creates multiple markdown files:

- `product_requirements_document.md` - 8000+ word PRD with full specifications
- `technology_stack_recommendations.md` - Tech stack analysis with costs
- `development_guide.md` - 30-week implementation plan
- `quality_review_report.md` - Validation and improvement suggestions

## 🎯 Success Metrics

### Document Quality
- ✅ **Completeness**: Full feature specifications, user stories, and requirements
- ✅ **Professionals**: Industry-standard PRD format and structure
- ✅ **Accuracy**: Technical feasibility and business alignment
- ✅ **Actionable**: Clear implementation guidance and timelines

### System Performance
- ✅ **Generation Time**: 3-5 minutes per PRD
- ✅ **Scalability**: Supports concurrent users in cloud
- ✅ **Reliability**: Production-grade error handling and logging

## 🛠️ Development

### Local Testing
```bash
# Run tests
pytest tests/ -v

# Health check
curl http://localhost:8000/health

# Start development server
python -m prd_generator.main
```

### Extending the System
- **Add New Agents**: Create new agent configurations in `config/agents.yaml`
- **Custom Tools**: Add new tools in `src/prd_generator/tools/`
- **API Endpoints**: Extend FastAPI endpoints in `main.py`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-agent`
3. Make changes and test thoroughly
4. Submit pull request with detailed description

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Pinecone connection errors:**
- Check API key and region settings
- Verify network connectivity

**OpenAI API rate limits:**
- Monitor usage in your OpenAI dashboard
- Implement retry logic for production

**Deployment issues:**
- Check Railway logs for detailed error messages
- Verify environment variable configuration
- Ensure Dockerfile builds successfully

### Health Check
Always test the health endpoint to verify service status:
```bash
curl https://your-railway-app.railway.app/health
```

## 🚀 Future Enhancements

- [ ] PDF export functionality
- [ ] Team collaboration features
- [ ] Integrations with Jira, GitHub, Notion
- [ ] Advanced analytics and reporting
- [ ] Custom template library
- [ ] Multi-language support
- [ ] Real-time collaboration mode

---

**Ready to transform your app ideas into professional PRDs? 🚀**

Visit the web interface and describe your next big idea!
