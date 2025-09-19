from crewai.tools import BaseTool
from typing import Type, Any, Dict, List
from pydantic import BaseModel, Field
import json
import os
from datetime import datetime

class PRDTemplateInput(BaseModel):
    """Input schema for PRD template generation."""
    project_name: str = Field(..., description="Name of the project")
    requirements_data: Dict[str, Any] = Field(..., description="Processed requirements data")
    stakeholders: List[str] = Field(default_factory=list, description="List of stakeholders")

class PRDTemplateGenerator(BaseTool):
    name: str = "PRD Template Generator"
    description: str = "Generates industry-standard PRD templates with structured sections"
    args_schema: Type[BaseModel] = PRDTemplateInput

    def _run(self, project_name: str, requirements_data: Dict[str, Any], stakeholders: List[str] = None) -> str:
        """Generate a comprehensive PRD template."""

        prd_template = f"""
# Product Requirements Document (PRD)
**Project:** {project_name}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Version:** 1.0

## 1. Document Information
- **Document Owner:** Product Manager
- **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
- **Review Cycle:** Weekly
- **Distribution:** Development Team, Stakeholders, QA Team

## 2. Executive Summary

### 2.1 Product Vision
[Product vision statement based on requirements]

### 2.2 Business Objectives
[Key business objectives and goals]

### 2.3 Success Metrics
[Measurable outcomes and KPIs]

## 3. Product Overview

### 3.1 Product Description
[Comprehensive product description]

### 3.2 Target Market
[Market analysis and opportunity]

### 3.3 User Personas
[Detailed user persona definitions]

## 4. Stakeholder Analysis

### 4.1 Internal Stakeholders
[Internal team members and their roles]

### 4.2 External Stakeholders
[External parties and their interests]

## 5. Functional Requirements

### 5.1 Core Features
[Primary feature set with detailed descriptions]

### 5.2 User Stories
[User stories in "As a [user], I want [feature] so that [benefit]" format]

### 5.3 Feature Prioritization
[MoSCoW prioritization or similar framework]

## 6. Non-Functional Requirements

### 6.1 Performance Requirements
[Response times, throughput, scalability requirements]

### 6.2 Security Requirements
[Authentication, authorization, data protection]

### 6.3 Usability Requirements
[User experience standards and accessibility]

### 6.4 Compatibility Requirements
[Browser, device, and platform compatibility]

## 7. Technical Requirements

### 7.1 System Architecture
[High-level architecture overview]

### 7.2 Integration Requirements
[Third-party integrations and APIs]

### 7.3 Data Requirements
[Database schema and data flow requirements]

## 8. Design & User Experience

### 8.1 Design Principles
[UI/UX design guidelines and principles]

### 8.2 Wireframes & Mockups
[References to design artifacts]

### 8.3 User Journey Mapping
[Key user flows and interactions]

## 9. Success Metrics & Analytics

### 9.1 Key Performance Indicators
[Specific KPIs and measurement methods]

### 9.2 Analytics Requirements
[Tracking and reporting requirements]

## 10. Timeline & Milestones

### 10.1 Project Phases
[High-level project timeline]

### 10.2 Key Milestones
[Critical project milestones and deadlines]

### 10.3 Dependencies
[External dependencies and blockers]

## 11. Resource Requirements

### 11.1 Team Structure
[Required team members and roles]

### 11.2 Budget Considerations
[Cost estimates and budget requirements]

### 11.3 Technology Resources
[Hardware, software, and infrastructure needs]

## 12. Risk Management

### 12.1 Risk Assessment
[Identified risks and impact assessment]

### 12.2 Mitigation Strategies
[Risk mitigation and contingency plans]

## 13. Quality Assurance

### 13.1 Testing Strategy
[Testing approach and methodologies]

### 13.2 Acceptance Criteria
[Definition of done for each feature]

## 14. Launch Strategy

### 14.1 Go-to-Market Plan
[Product launch and marketing strategy]

### 14.2 Success Criteria
[Launch success metrics and evaluation]

## 15. Post-Launch Support

### 15.1 Maintenance Plan
[Ongoing maintenance and updates]

### 15.2 Support Strategy
[User support and issue resolution]

## 16. Appendices

### 16.1 Glossary
[Technical terms and definitions]

### 16.2 References
[Supporting documents and research]

### 16.3 Change Log
[Document revision history]
        """

        return prd_template.strip()

class TechStackInput(BaseModel):
    """Input schema for tech stack recommendations."""
    project_type: str = Field(..., description="Type of project (web, mobile, desktop)")
    requirements: Dict[str, Any] = Field(..., description="Technical requirements")
    scale: str = Field(default="medium", description="Expected project scale")

class TechStackAdvisor(BaseTool):
    name: str = "Tech Stack Advisor"
    description: str = "Provides technology stack recommendations based on project requirements"
    args_schema: Type[BaseModel] = TechStackInput

    def _run(self, project_type: str, requirements: Dict[str, Any], scale: str = "medium") -> str:
        """Generate tech stack recommendations."""

        tech_stacks = {
            "web": {
                "frontend": {
                    "primary": ["React.js + Next.js", "Vue.js + Nuxt.js", "Angular"],
                    "styling": ["Tailwind CSS", "Material-UI", "Ant Design"],
                    "state_management": ["Redux Toolkit", "Zustand", "Pinia"]
                },
                "backend": {
                    "primary": ["Node.js + Express", "Python + FastAPI", "Python + Django"],
                    "alternatives": [".NET Core", "Ruby on Rails", "Go + Gin"]
                },
                "database": {
                    "relational": ["PostgreSQL", "MySQL", "SQLite"],
                    "nosql": ["MongoDB", "Redis", "Firebase Firestore"]
                },
                "deployment": {
                    "hosting": ["Vercel", "Netlify", "AWS", "DigitalOcean"],
                    "containers": ["Docker", "Kubernetes"],
                    "ci_cd": ["GitHub Actions", "GitLab CI", "Jenkins"]
                }
            },
            "mobile": {
                "cross_platform": ["React Native", "Flutter", "Ionic"],
                "native_ios": ["Swift", "Objective-C"],
                "native_android": ["Kotlin", "Java"],
                "backend": ["Firebase", "Supabase", "Node.js", "Python"]
            },
            "desktop": {
                "cross_platform": ["Electron", "Tauri", "Flutter Desktop"],
                "native": ["Python + Tkinter", "C# + WPF", "Java + JavaFX"]
            }
        }

        recommendations = tech_stacks.get(project_type.lower(), tech_stacks["web"])

        recommendation_text = f"""
# Technology Stack Recommendations

## Project Type: {project_type.title()}
## Scale: {scale.title()}

## Recommended Architecture

### Frontend Technologies
{self._format_tech_options(recommendations.get('frontend', {}))}

### Backend Technologies
{self._format_tech_options(recommendations.get('backend', {}))}

### Database Solutions
{self._format_tech_options(recommendations.get('database', {}))}

### DevOps & Deployment
{self._format_tech_options(recommendations.get('deployment', {}))}

## Open Source Alternatives
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Version Control:** Git + GitHub/GitLab
- **Project Management:** OpenProject, Taiga
- **Communication:** Mattermost, Rocket.Chat

## Cost Analysis
- **Development Phase:** $0-500/month (using free tiers)
- **Production Phase:** $50-500/month (depending on scale)
- **Enterprise Scale:** $500-2000/month

## Implementation Timeline
1. **Week 1-2:** Development environment setup
2. **Week 3-4:** Core architecture implementation
3. **Week 5-8:** Feature development
4. **Week 9-10:** Testing and optimization
5. **Week 11-12:** Deployment and launch
        """

        return recommendation_text.strip()

    def _format_tech_options(self, tech_dict: Dict[str, List[str]]) -> str:
        """Format technology options into readable text."""
        formatted = ""
        for category, options in tech_dict.items():
            formatted += f"\n**{category.title()}:**\n"
            for option in options:
                formatted += f"- {option}\n"
        return formatted

class DevelopmentGuideInput(BaseModel):
    """Input schema for development guide generation."""
    project_data: Dict[str, Any] = Field(..., description="Complete project information")
    methodology: str = Field(default="agile", description="Development methodology")

class DevelopmentGuideGenerator(BaseTool):
    name: str = "Development Guide Generator"
    description: str = "Creates detailed phase-by-phase development guides"
    args_schema: Type[BaseModel] = DevelopmentGuideInput

    def _run(self, project_data: Dict[str, Any], methodology: str = "agile") -> str:
        """Generate comprehensive development guide."""

        guide = f"""
# Comprehensive Development Guide

## Methodology: {methodology.title()}

## Phase 1: Planning & Architecture (Weeks 1-4)

### Week 1: Project Initialization
**Objectives:** Set up project foundation and team structure

**Daily Tasks:**
- **Day 1-2:**
  - Initialize Git repository
  - Set up development environment
  - Configure IDE and development tools
  - Create project documentation structure

- **Day 3-4:**
  - Finalize team roles and responsibilities
  - Set up communication channels (Slack, Discord)
  - Establish code review processes
  - Create development guidelines document

- **Day 5:**
  - Sprint planning meeting
  - Define Definition of Done (DoD)
  - Set up project management tools (Jira, Trello)

**Deliverables:**
- Project repository with initial structure
- Team communication setup
- Development process documentation
- Sprint 1 planning complete

### Week 2: Technical Architecture Design
**Objectives:** Design system architecture and database schema

**Daily Tasks:**
- **Day 1-2:**
  - Create high-level architecture diagrams
  - Design database schema (ERD)
  - Define API endpoints and data models
  - Document system components and interactions

- **Day 3-4:**
  - Set up development database
  - Create database migration scripts
  - Design authentication and authorization system
  - Plan third-party integrations

- **Day 5:**
  - Architecture review meeting
  - Finalize technical decisions
  - Create technical specification document

**Deliverables:**
- System architecture documentation
- Database schema and migration scripts
- API specification document
- Technical decision log

### Week 3: Development Environment Setup
**Objectives:** Prepare all development and deployment environments

**Daily Tasks:**
- **Day 1-2:**
  - Set up local development environment
  - Configure development database
  - Install and configure all required tools
  - Create environment configuration files

- **Day 3-4:**
  - Set up CI/CD pipeline
  - Configure automated testing framework
  - Set up code quality tools (linters, formatters)
  - Create deployment scripts

- **Day 5:**
  - Environment testing and validation
  - Documentation of setup processes
  - Team training on tools and processes

**Deliverables:**
- Complete development environment
- CI/CD pipeline configuration
- Deployment automation scripts
- Environment setup documentation

### Week 4: UI/UX Design & Planning
**Objectives:** Finalize user interface designs and user experience flows

**Daily Tasks:**
- **Day 1-2:**
  - Create detailed wireframes
  - Design user interface mockups
  - Define user interaction patterns
  - Establish design system and components

- **Day 3-4:**
  - User experience flow mapping
  - Accessibility compliance planning
  - Mobile responsiveness design
  - Design review and iteration

- **Day 5:**
  - Final design approval
  - Create design handoff documentation
  - Plan Phase 2 development sprints

**Deliverables:**
- Complete UI/UX design package
- Design system documentation
- User flow diagrams
- Phase 2 sprint planning

## Phase 2: Core Development Setup (Weeks 5-6)

### Week 5: Foundation Development
**Objectives:** Build core application structure and basic functionality

**Sprint Goals:**
- Set up project scaffolding
- Implement authentication system
- Create basic database operations
- Set up routing and navigation

**Daily Implementation Tasks:**

**Day 1: Project Structure**
```


# Create project structure

mkdir -p src/components src/pages src/utils src/services
mkdir -p src/styles src/assets src/hooks src/context
mkdir -p tests/unit tests/integration tests/e2e
mkdir -p docs/api docs/deployment docs/development

# Initialize package.json and dependencies

npm init -y
npm install [required packages]

```

**Day 2: Authentication Implementation**
```

// Example authentication service setup
class AuthService {{
async login(credentials) {{
// Implementation
}}

async register(userData) {{
// Implementation
}}

async logout() {{
// Implementation
}}
}}

```

**Day 3: Database Setup**
```


# Database models and migrations

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
__tablename__ = 'users'
id = Column(Integer, primary_key=True)
email = Column(String(120), unique=True, nullable=False)
\# Additional fields

```

**Day 4: API Endpoints**
```


# Basic API routes

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/api/auth/login")
async def login(credentials: UserCredentials, db: Session = Depends(get_db)):
\# Implementation
pass

```

**Day 5: Testing & Integration**
- Write unit tests for authentication
- Integration testing for API endpoints
- End-to-end testing setup
- Code review and refactoring

### Week 6: Core Features Implementation
**Objectives:** Implement primary application features

**Feature Development Checklist:**
- [ ] User management system
- [ ] Core business logic implementation
- [ ] Data validation and error handling
- [ ] Basic UI components
- [ ] API integration testing

## Phase 3: MVP Feature Development (Weeks 7-18)

### Sprint Structure (2-week sprints)

**Sprint 1 (Weeks 7-8): User Management**
- User registration and authentication
- Profile management
- Password reset functionality
- Email verification system

**Sprint 2 (Weeks 9-10): Core Features Set 1**
- Primary feature implementation
- Data input/output functionality
- Basic search and filtering
- User dashboard development

**Sprint 3 (Weeks 11-12): Core Features Set 2**
- Advanced feature implementation
- File upload/management
- Notification system
- User preferences

**Sprint 4 (Weeks 13-14): Integration & APIs**
- Third-party API integrations
- Payment system integration (if required)
- Social media integrations
- External service connections

**Sprint 5 (Weeks 15-16): Advanced Features**
- Analytics and reporting
- Admin panel development
- Advanced user permissions
- Data export/import functionality

**Sprint 6 (Weeks 17-18): Polish & Optimization**
- Performance optimization
- UI/UX improvements
- Bug fixes and refinements
- Accessibility improvements

## Phase 4: Advanced Features & Integrations (Weeks 19-24)

### Advanced Development Tasks

**Weeks 19-20: Performance Optimization**
- Database query optimization
- Caching implementation (Redis)
- CDN setup for static assets
- Code splitting and lazy loading

**Weeks 21-22: Security Hardening**
- Security audit and penetration testing
- Data encryption implementation
- API rate limiting
- HTTPS and security headers

**Weeks 23-24: Scalability Preparation**
- Load balancing configuration
- Database scaling strategies
- Monitoring and alerting setup
- Disaster recovery planning

## Phase 5: Testing & Quality Assurance (Weeks 25-28)

### Comprehensive Testing Strategy

**Week 25: Unit Testing**
- Complete unit test coverage (>90%)
- Test automation setup
- Mock service implementation
- Test documentation

**Week 26: Integration Testing**
- API integration testing
- Database integration testing
- Third-party service testing
- Cross-browser compatibility testing

**Week 27: User Acceptance Testing**
- UAT test case creation
- Stakeholder testing sessions
- Feedback collection and analysis
- Bug prioritization and fixing

**Week 28: Performance & Security Testing**
- Load testing and stress testing
- Security vulnerability scanning
- Performance benchmarking
- Final bug fixes and optimization

## Phase 6: Deployment & Launch (Weeks 29-30)

### Week 29: Production Deployment
**Pre-deployment Checklist:**
- [ ] Production environment setup
- [ ] Database migration and seeding
- [ ] SSL certificate installation
- [ ] DNS configuration
- [ ] Monitoring tools setup
- [ ] Backup systems configuration

**Deployment Steps:**
1. **Infrastructure Setup**
```


# Example Docker deployment

docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic

```

2. **Database Migration**
```


# Production database setup

pg_dump development_db > backup.sql
psql production_db < backup.sql

```

3. **SSL and Security Configuration**
```


# Nginx SSL configuration

server {{
listen 443 ssl;
ssl_certificate /path/to/certificate.crt;
ssl_certificate_key /path/to/private.key;
\# Additional SSL settings
}}

```

### Week 30: Launch & Monitoring
**Launch Day Tasks:**
- [ ] Final production testing
- [ ] DNS cutover to production
- [ ] Launch announcement
- [ ] Real-time monitoring
- [ ] User support preparation
- [ ] Performance monitoring
- [ ] Issue tracking and resolution

## Phase 7: Post-Launch Support (Ongoing)

### Week 31+: Maintenance & Iteration

**Daily Monitoring Tasks:**
- System health checks
- Performance metrics review
- User feedback analysis
- Security monitoring

**Weekly Tasks:**
- Bug fixes and patches
- Performance optimizations
- User support ticket resolution
- Analytics review and reporting

**Monthly Tasks:**
- Feature usage analysis
- Security updates and patches
- Backup verification
- Infrastructure cost optimization

**Quarterly Tasks:**
- Major feature releases
- Technology stack updates
- Security audits
- Performance reviews

## Quality Gates & Review Checkpoints

### Phase Gate Reviews
1. **Planning Phase Gate:** Architecture approval, team readiness
2. **Development Phase Gate:** Code quality, test coverage, feature completeness
3. **Testing Phase Gate:** Bug resolution, performance benchmarks
4. **Launch Phase Gate:** Production readiness, launch criteria met

### Code Quality Standards
- **Code Coverage:** Minimum 90% for critical paths
- **Performance:** Page load times < 3 seconds
- **Security:** OWASP compliance
- **Accessibility:** WCAG 2.1 AA compliance

### Risk Mitigation Strategies

**Technical Risks:**
- Regular code reviews and pair programming
- Comprehensive testing at all levels
- Performance monitoring and optimization
- Security audits and penetration testing

**Project Risks:**
- Agile methodology with regular sprint reviews
- Clear communication channels
- Risk register maintenance
- Contingency planning for critical issues

**Resource Risks:**
- Cross-training team members
- Documentation of all processes
- Knowledge sharing sessions
- External consultant backup plans

## Team Coordination & Communication

### Daily Processes
- **Daily Standups:** 15-minute sync meetings
- **Code Reviews:** All code changes reviewed before merge
- **Continuous Integration:** Automated testing and deployment
- **Issue Tracking:** Real-time bug and task management

### Weekly Processes
- **Sprint Planning:** Feature prioritization and estimation
- **Sprint Reviews:** Demo completed features to stakeholders
- **Retrospectives:** Team process improvement discussions
- **Architecture Reviews:** Technical decision validation

### Tools & Platforms
- **Version Control:** Git with branching strategy
- **Project Management:** Jira/Trello for task tracking
- **Communication:** Slack/Discord for team chat
- **Documentation:** Confluence/Notion for knowledge base
- **Code Quality:** SonarQube for code analysis
- **Monitoring:** Prometheus/Grafana for system monitoring

## Success Metrics & KPIs

### Development Metrics
- **Velocity:** Story points completed per sprint
- **Code Quality:** Technical debt ratio, code coverage
- **Bug Rate:** Defects per feature, resolution time
- **Deployment Frequency:** Releases per month

### Business Metrics
- **User Adoption:** Monthly active users, user retention
- **Performance:** System uptime, response times
- **Customer Satisfaction:** NPS score, support ticket volume
- **Revenue Impact:** Feature usage correlation with business goals

This comprehensive development guide provides a structured approach to building your application from initial planning through post-launch support. Each phase includes specific tasks, deliverables, and quality checkpoints to ensure successful project completion.
     """

        return guide.strip()
