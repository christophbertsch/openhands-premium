# OpenHands Premium Local Setup

This repository contains a comprehensive, production-grade local setup for OpenHands that matches the quality of the All-Hands free trial. It includes enhanced agents, quality microagents, advanced configurations, and premium web interface features.

## 🚀 Features

### Core Enhancements
- **Premium Quality Agents**: Enhanced CodeAct agents with specialized capabilities
- **Advanced Microagents**: Code quality, security, performance, testing, and documentation analysis
- **Production Configuration**: Optimized settings for maximum performance and quality
- **Enhanced Web Interface**: Smart suggestions, code quality checks, and advanced file handling
- **Automated Deployment**: Production-ready deployment scripts with monitoring and backup

### Quality Features
- **Code Quality Analysis**: Real-time code quality scoring and suggestions
- **Security Scanning**: Automated security vulnerability detection
- **Performance Optimization**: Performance analysis and optimization recommendations
- **Testing Integration**: Comprehensive testing analysis and coverage reporting
- **Documentation Generation**: Automated documentation quality assessment

### Web Interface Enhancements
- **Smart Suggestions**: Context-aware input suggestions
- **Code Execution**: Direct code execution from chat interface
- **Quality Mode Toggle**: Switch between standard and premium quality modes
- **Advanced File Upload**: Drag-and-drop with automatic quality analysis
- **Keyboard Shortcuts**: Productivity-focused keyboard shortcuts

## 📋 Prerequisites

- **Operating System**: Linux, macOS, or WSL on Windows (Ubuntu 22.04+)
- **Docker**: Latest version with daemon running
- **Python**: 3.12+
- **Node.js**: 22.x+
- **Poetry**: 1.8+
- **Git**: Latest version

## 🛠️ Quick Setup

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd <repo-name>
chmod +x setup_openhands.sh
./setup_openhands.sh
```

### 2. Configure API Keys
```bash
./setup_api_keys.sh
```

### 3. Run Quality Assurance
```bash
./qa_openhands.sh
```

### 4. Start OpenHands
```bash
./start_openhands.sh
```

## 📁 File Structure

```
├── setup_openhands.sh          # Main setup script
├── enhanced_config.toml        # Premium configuration
├── quality_agents.py           # Enhanced agent implementations
├── advanced_microagents.py     # Specialized microagents
├── deployment_script.py        # Production deployment automation
├── web_enhancements.js         # Web interface enhancements
├── OpenHands/                  # OpenHands source code
└── scripts/                    # Management and utility scripts
```

## 🎯 Usage

### Starting OpenHands
```bash
# Quick start
./start_openhands.sh

# Or use the management script
./manage_openhands.sh start
```

### Managing the Installation
```bash
# Show help
./manage_openhands.sh help

# Check status
./manage_openhands.sh status

# Update to latest version
./manage_openhands.sh update

# Clean up resources
./manage_openhands.sh clean
```

### Production Deployment
```bash
# Deploy with full production setup
python3 deployment_script.py deploy

# Start production service
python3 deployment_script.py start

# Check deployment status
python3 deployment_script.py status
```

## ⚙️ Configuration

### LLM Models
The setup supports multiple high-quality LLM providers:

- **Claude Sonnet** (Recommended for highest quality)
- **GPT-4o** (Best balance of quality and speed)
- **GPT-4o Mini** (Cost-effective option)
- **O1 Preview** (Advanced reasoning tasks)

### Agent Types
Choose from specialized agents:

- **PremiumCodeActAgent**: All-purpose premium agent
- **SecurityFocusedAgent**: Security-specialized agent
- **PerformanceOptimizedAgent**: Performance-focused agent
- **TestingSpecialistAgent**: Testing-focused agent
- **DocumentationExpertAgent**: Documentation specialist

### Quality Features
- **Quality Mode**: Enhanced prompts and validation
- **Auto-save**: Automatic conversation saving
- **Code Highlighting**: Advanced syntax highlighting
- **Smart Suggestions**: Context-aware suggestions
- **File Analysis**: Automatic quality analysis for uploaded files

## 🔧 Advanced Configuration

### Custom Agent Configuration
```python
from quality_agents import QualityAgentFactory

# Create specialized agent
agent = QualityAgentFactory.create_agent('premium', config)
```

### Microagent Integration
```python
from advanced_microagents import MicroagentOrchestrator

# Run comprehensive analysis
orchestrator = MicroagentOrchestrator()
results = orchestrator.comprehensive_analysis(code, language, project_path)
```

### Web Enhancement Integration
```javascript
// Initialize enhanced features
new EnhancedChatInterface();
new EnhancedFileUpload();
```

## 📊 Quality Metrics

The setup includes comprehensive quality tracking:

- **Code Quality Score**: 0-100 based on best practices
- **Security Score**: Vulnerability assessment
- **Performance Score**: Efficiency analysis
- **Test Coverage**: Testing completeness
- **Documentation Score**: Documentation quality

## 🔒 Security Features

- **Input Validation**: Comprehensive input sanitization
- **Security Scanning**: Automated vulnerability detection
- **Secure Configuration**: Production-hardened settings
- **Access Control**: Proper permission management
- **Audit Logging**: Complete activity logging

## 🚀 Performance Optimizations

- **Caching**: Intelligent response caching
- **Resource Management**: Optimized memory and CPU usage
- **Concurrent Processing**: Multi-conversation support
- **Load Balancing**: Efficient request distribution
- **Monitoring**: Real-time performance tracking

## 📈 Monitoring and Maintenance

### Health Checks
```bash
# Manual health check
./qa_openhands.sh

# View logs
tail -f ~/.openhands/logs/deployment.log
```

### Backup and Recovery
```bash
# Manual backup
~/.openhands/backup.sh

# Restore from backup
# Backups are stored in ~/.openhands/backups/
```

### Updates
```bash
# Update OpenHands
./manage_openhands.sh update

# Update configuration
./manage_openhands.sh config
```

## 🐛 Troubleshooting

### Common Issues

1. **Docker Permission Issues**
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using port 3000
   lsof -i :3000
   # Kill the process or change port in config
   ```

3. **API Key Issues**
   ```bash
   # Reconfigure API keys
   ./setup_api_keys.sh
   ```

4. **Memory Issues**
   ```bash
   # Check memory usage
   free -h
   # Adjust max_memory in deployment config
   ```

### Getting Help

1. Check the logs: `~/.openhands/logs/`
2. Run quality assurance: `./qa_openhands.sh`
3. Check system status: `./manage_openhands.sh status`
4. Review configuration: `~/.openhands/config.toml`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenHands team for the excellent foundation
- All-Hands AI for the inspiration
- Community contributors for feedback and improvements

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the logs in `~/.openhands/logs/`
- Open an issue in this repository

---

**Note**: This setup provides enterprise-grade quality and features. For production use, ensure you have proper API keys configured and sufficient system resources allocated.