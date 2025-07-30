# OpenHands Premium - Quick Start Guide

## 🚀 Save to GitHub

### Option 1: Using the Script (Recommended)
```bash
# Set your GitHub token and run the script
export GITHUB_TOKEN="your_github_token_here"
./create_github_repo.sh
```

### Option 2: Manual GitHub Setup
1. Create a new repository on GitHub named `openhands-premium-setup`
2. Add the remote and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/openhands-premium-setup.git
git push -u origin master
```

## 📥 Clone and Setup on Any Machine

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/openhands-premium-setup.git
cd openhands-premium-setup

# Run the complete setup
./setup_openhands.sh

# Configure API keys
./setup_api_keys.sh

# Start OpenHands
./start_openhands.sh
```

## 🎯 What You Get

### Premium Features
- **Enhanced Agents**: Specialized agents for different tasks
- **Quality Analysis**: Real-time code quality scoring
- **Security Scanning**: Automated vulnerability detection
- **Performance Optimization**: Performance analysis and recommendations
- **Smart Web Interface**: Enhanced UI with advanced features
- **Production Deployment**: Enterprise-grade deployment scripts

### Quality Agents
- `PremiumCodeActAgent`: All-purpose premium agent
- `SecurityFocusedAgent`: Security specialist
- `PerformanceOptimizedAgent`: Performance expert
- `TestingSpecialistAgent`: Testing specialist
- `DocumentationExpertAgent`: Documentation expert

### Microagents
- **Code Quality**: Comprehensive code analysis
- **Security**: Vulnerability scanning
- **Performance**: Optimization recommendations
- **Testing**: Coverage analysis
- **Documentation**: Quality assessment

### Web Enhancements
- Smart input suggestions
- Code execution from chat
- Quality mode toggle
- Advanced file upload with analysis
- Keyboard shortcuts
- Auto-save functionality

## 🛠️ Management Commands

```bash
# Start OpenHands
~/start_openhands.sh

# Manage OpenHands
~/manage_openhands.sh start|stop|status|update|config|logs

# Production deployment
python3 deployment_script.py deploy
python3 deployment_script.py start
python3 deployment_script.py status

# Quality assurance
~/qa_openhands.sh
```

## ⚙️ Configuration

### LLM Models (Recommended Order)
1. **Claude Sonnet** - Highest quality
2. **GPT-4o** - Best balance
3. **GPT-4o Mini** - Cost-effective
4. **O1 Preview** - Complex reasoning

### API Keys Setup
```bash
# Interactive setup
./setup_api_keys.sh

# Manual configuration
nano ~/.openhands/config.toml
```

## 🔧 Customization

### Custom Agents
```python
from quality_agents import QualityAgentFactory
agent = QualityAgentFactory.create_agent('premium', config)
```

### Microagent Analysis
```python
from advanced_microagents import MicroagentOrchestrator
orchestrator = MicroagentOrchestrator()
results = orchestrator.comprehensive_analysis(code, language)
```

## 📊 Quality Metrics

The setup tracks:
- Code Quality Score (0-100)
- Security Score
- Performance Score
- Test Coverage
- Documentation Quality

## 🆘 Troubleshooting

### Common Issues
1. **Docker not running**: `sudo systemctl start docker`
2. **Port in use**: Check `lsof -i :3000`
3. **API keys**: Run `./setup_api_keys.sh`
4. **Permissions**: `sudo usermod -aG docker $USER`

### Get Help
- Check logs: `~/.openhands/logs/`
- Run QA: `./qa_openhands.sh`
- Check status: `./manage_openhands.sh status`

## 🎉 Enjoy Your Premium OpenHands Setup!

This setup provides enterprise-grade quality matching the All-Hands free trial with additional premium features for local development.