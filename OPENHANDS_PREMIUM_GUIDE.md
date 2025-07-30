# OpenHands Premium Setup Guide

## 🎉 Congratulations! 

You now have a **production-grade OpenHands installation** with all the premium features that match or exceed the quality of the All-Hands free trial.

## 📋 What's Included

### ✨ Premium Features
- **Advanced Quality Agents**: Specialized agents for different tasks (coding, security, performance, testing, documentation)
- **Comprehensive Microagents**: Code quality analysis, security scanning, performance optimization
- **Enhanced Web Interface**: Quality mode toggle, smart suggestions, code analysis tools
- **Production Configuration**: Optimized settings for maximum performance and quality
- **Automated Quality Checks**: Built-in validation and monitoring
- **Performance Optimizations**: Efficient resource usage and caching
- **Security Enhancements**: Built-in security analysis and best practices

### 🤖 Available Agents
1. **PremiumCodeActAgent**: Enhanced CodeAct with quality focus
2. **SecurityFocusedAgent**: Specialized for security-conscious development
3. **PerformanceOptimizedAgent**: Optimized for high-performance applications
4. **TestingSpecialistAgent**: Comprehensive testing and validation
5. **DocumentationExpertAgent**: Professional documentation generation

### 🔧 Microagents
- **Code Quality Analysis**: Real-time code quality scoring and suggestions
- **Security Scanner**: Vulnerability detection and security recommendations
- **Performance Analyzer**: Performance bottleneck identification
- **Testing Coverage**: Test coverage analysis and recommendations
- **Documentation Generator**: Automated documentation creation

## 🚀 Getting Started

### Step 1: Configure API Keys
```bash
~/setup_openhands_keys.sh
```

This will prompt you to enter:
- **OpenAI API Key** (for GPT-4o, GPT-4o-mini)
- **Anthropic API Key** (for Claude Sonnet - recommended for best quality)

### Step 2: Start OpenHands
```bash
~/start_openhands_premium.sh
```

### Step 3: Access the Interface
Open your browser and go to: **http://localhost:3000**

## 🎛️ Management Commands

Use the management script for easy control:

```bash
~/openhands_premium.sh [command]
```

Available commands:
- `start` - Start OpenHands
- `stop` - Stop OpenHands
- `status` - Show current status
- `config` - Edit configuration
- `update` - Update to latest version
- `logs` - View logs

## ⚙️ Configuration

Your configuration is located at: `/root/.openhands/config.toml`

### Key Configuration Options

#### LLM Models (Recommended Order for Quality)
1. **Claude Sonnet** (`anthropic/claude-3-5-sonnet-20241022`) - Best quality
2. **GPT-4o** (`gpt-4o`) - Excellent balance of quality and speed
3. **GPT-4o-mini** (`gpt-4o-mini`) - Cost-effective option

#### Quality Settings
```toml
[core]
max_iterations = 2000          # More iterations for complex tasks
max_budget_per_task = 20.0     # Higher budget for quality
enable_browser = true          # Web browsing capability
save_screenshots_in_trajectory = true  # Visual debugging

[agent]
enable_browsing = true         # Web research
enable_llm_editor = true       # Advanced editing
enable_jupyter = true          # Code execution
enable_think = true            # Reasoning steps
enable_condensation_request = true  # Memory management
```

## 🌐 Web Interface Features

### Quality Mode
- Toggle quality mode in the top-right corner
- Enables enhanced reasoning and validation
- Uses premium models for better results

### Smart Suggestions
- Context-aware suggestions while typing
- Code quality recommendations
- Best practice reminders

### Code Analysis Tools
- **Copy Code**: One-click code copying
- **Run Code**: Execute code directly in the interface
- **Quality Check**: Real-time code quality analysis

### File Upload
- Drag-and-drop file upload
- Automatic code quality analysis
- Support for multiple file types

## 🔍 Quality Features

### Code Quality Analysis
- Real-time syntax checking
- Best practice validation
- Security vulnerability detection
- Performance optimization suggestions

### Security Features
- Input validation
- SQL injection detection
- XSS vulnerability scanning
- Secure coding recommendations

### Performance Monitoring
- Algorithm complexity analysis
- Memory usage optimization
- Database query optimization
- Caching recommendations

## 📊 Monitoring and Logs

### Log Locations
- Main logs: `/root/.openhands/logs/`
- Trajectories: `/root/.openhands/trajectories/`
- File store: `/root/.openhands/file_store/`

### Health Monitoring
```bash
# Check status
~/openhands_premium.sh status

# View logs
~/openhands_premium.sh logs

# Monitor in real-time
tail -f /root/.openhands/logs/*.log
```

## 🔧 Troubleshooting

### Common Issues

#### OpenHands Won't Start
1. Check if Docker is running: `docker info`
2. Verify API keys are configured: `~/openhands_premium.sh config`
3. Check logs: `~/openhands_premium.sh logs`

#### Poor Response Quality
1. Ensure you're using Claude Sonnet or GPT-4o
2. Enable Quality Mode in the web interface
3. Check your API key limits and usage

#### Performance Issues
1. Check available memory: `free -h`
2. Monitor Docker containers: `docker stats`
3. Review configuration: `~/openhands_premium.sh config`

### Getting Help
1. Check the logs first: `~/openhands_premium.sh logs`
2. Verify configuration: `~/openhands_premium.sh config`
3. Restart the service: `~/openhands_premium.sh stop && ~/openhands_premium.sh start`

## 🔄 Updates and Maintenance

### Update OpenHands
```bash
~/openhands_premium.sh update
```

### Backup Configuration
```bash
# Manual backup
cp -r /root/.openhands /root/.openhands.backup.$(date +%Y%m%d)

# Automated backups are configured in /root/.openhands/backup.sh
```

### Clean Up
```bash
# Clean Docker images and containers
docker system prune -f

# Clean cache
rm -rf /root/.openhands/cache/*
```

## 🎯 Best Practices

### For Best Quality Results
1. **Use Claude Sonnet** for complex reasoning tasks
2. **Enable Quality Mode** in the web interface
3. **Provide detailed context** in your requests
4. **Use specific, clear instructions**
5. **Break complex tasks** into smaller steps

### For Performance
1. **Use GPT-4o-mini** for simple tasks
2. **Enable caching** in configuration
3. **Monitor resource usage** regularly
4. **Clean up old trajectories** periodically

### For Security
1. **Keep API keys secure** and rotate regularly
2. **Review generated code** before execution
3. **Enable security analyzer** in configuration
4. **Monitor for suspicious activity**

## 📈 Advanced Usage

### Custom Agents
You can create custom agents by modifying `/root/.openhands/agents/quality_agents.py`

### Custom Microagents
Add custom microagents in `/root/.openhands/microagents/`

### Web Interface Customization
Modify `/workspace/OpenHands/frontend/src/enhancements.js` for custom features

## 🆘 Support

### Documentation
- OpenHands Official Docs: https://docs.all-hands.dev
- Configuration Reference: `/root/.openhands/config.toml`
- Agent Documentation: `/root/.openhands/agents/`

### Community
- GitHub: https://github.com/All-Hands-AI/OpenHands
- Discord: https://discord.gg/ESHStjSjD4
- Slack: https://join.slack.com/t/openhands-ai/shared_invite/zt-3847of6xi-xuYJIPa6YIPg4ElbDWbtSA

---

## 🎊 You're All Set!

Your OpenHands Premium installation is now ready to provide you with the same high-quality experience as the All-Hands free trial, but running locally on your own infrastructure.

**Happy coding!** 🚀

---

*This setup includes all premium features, quality agents, microagents, and optimizations for production-grade performance.*