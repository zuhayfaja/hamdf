# 🚀 Railway Deployment Guide

## 🎯 Quick Deployment (5 Minutes)

### Step 1: Push to GitHub
```bash
# Initialize Git repository
git init
git add .
git commit -m "Initial PRD Agent System setup"

# Create GitHub repository at https://github.com
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Connect to Railway
1. **Create Railway Account**: Go to [Railway.app](https://railway.app)
2. **New Project**: Click "New Project" → "Deploy from GitHub"
3. **Connect Repository**: Select your PRD Agent repository
4. **Auto Deploy**: Railway will automatically detect the Docker configuration

### Step 3: Configure Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```
# OpenRouter Configuration (replaces OpenAI)
OPENROUTER_API_KEY=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
OPENROUTER_MODEL=openrouter/sonoma-sky-alpha
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# For CrewAI compatibility
OPENAI_API_KEY=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

# Database & Infrastructure
PINECONE_API_KEY=pcsk_23s9bu_2GziKR8YDLFMNsehYruC5qTAbVR3QHJ4YSgWSnVp7EHqHuV1qcZLfGYMjLx36Hr
PINECONE_ENVIRONMENT=us-east-1
PYTHONPATH=/app/src
DEBUG=false
LOG_LEVEL=INFO
```

### Step 4: Deploy
Railway will automatically build and deploy your container. Monitor the build logs in the Railway dashboard.

### Step 5: Access Your PRD Agent
Once deployed, Railway will provide a URL (e.g., `https://prd-agent.up.railway.app`)

- **🌐 Web Interface**: Open the URL in your browser
- **🏥 Health Check**: Visit `https://your-url.up.railway.app/health`
- **🔗 API Endpoint**: Use `https://your-url.up.railway.app/generate-prd`

## 📊 What Happens During Deployment

1. **Automatic Build**: Railway uses your `Dockerfile` to build the container in cloud Linux environment
2. **No Compilation Issues**: Bypasses Windows ChromaDB C++ compilation entirely
3. **Health Monitoring**: Railway uses `/health` endpoint to monitor service status
4. **Auto Scaling**: Service automatically scales based on demand
5. **Logging**: All logs available in Railway dashboard

## ✅ Success Checklist

- [ ] GitHub repository created and code pushed
- [ ] Railway project connected to repository
- [ ] Environment variables configured in Railway
- [ ] Docker build successful (monitor logs)
- [ ] Service reachable via provided URL
- [ ] Web interface loads at root URL
- [ ] Health check returns "healthy" status

## 🎯 Testing Your Deployment

1. **Web Interface Test**:
   - Go to your Railway URL
   - Describe an app idea
   - Click "Generate PRD & Development Guide"
   - Wait 3-5 minutes for completion

2. **API Test**:
   ```bash
   curl -X POST "https://your-railway-url.up.railway.app/generate-prd" \
        -H "Content-Type: application/json" \
        -d '{"idea_description": "Test app idea"}'
   ```

3. **Health Check**:
   ```bash
   curl https://your-railway-url.up.railway.app/health
   # Should return: {"status": "healthy", ...}
   ```

## 🚫 Troubleshooting

### Build Failed
- Check Railway build logs for errors
- Verify `requirements.txt` includes all needed packages
- Ensure `Dockerfile` uses correct paths

### Import Errors
- Verify `PYTHONPATH=/app/src` is set in Railway variables
- Check that all required packages are in `requirements.txt`

### Service Doesn't Start
- Check the `/health` endpoint for detailed error messages
- Verify API keys are correctly set in Railway variables
- Look at Railway application logs

### Web Interface Not Loading
- Verify the FastAPI app is starting correctly
- Check that port 8000 is exposed in Dockerfile
- Test `/health` endpoint to confirm service health

## 💰 Cost Estimate

**Railway Free Tier**:
- ✅ Perfect for development and testing
- ✅ Includes database connections
- ✅ Full Docker support
- ✅ Health checks and logging

**Railway Pro** ($5/month for starter):
- Full production features
- PostgreSQL database included
- Unlimited bandwidth
- priority support

## 🎯 What's Included

Your deployed PRD Agent can generate:
- ✅ **8,000+ word PRDs** with full specifications
- ✅ **Technology recommendations** with cost analysis
- ✅ **30-week development plans** with sprint breakdowns
- ✅ **Quality reviews** and validation reports
- ✅ **Professional documentation** in markdown format

## 🚀 Going Live!

Your PRD generation service will be live in minutes and ready to transform app ideas into professional documentation!

**🎉 Ready to generate your first PRD in the cloud!**
