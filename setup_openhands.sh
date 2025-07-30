#!/bin/bash

# OpenHands High-Quality Local Setup Script
# This script sets up OpenHands with the same quality as the free trial

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OPENHANDS_DIR="/workspace/OpenHands"
CONFIG_DIR="$HOME/.openhands"
WORKSPACE_DIR="$HOME/openhands-workspace"

echo -e "${GREEN}🚀 OpenHands High-Quality Local Setup${NC}"
echo -e "${BLUE}Setting up OpenHands with production-grade quality...${NC}"

# Function to print status
print_status() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Create necessary directories
print_status "Creating directories..."
mkdir -p "$CONFIG_DIR"
mkdir -p "$WORKSPACE_DIR"
mkdir -p "$HOME/.cache/openhands"

# Check system requirements
print_status "Checking system requirements..."

# Check Python 3.12
if ! command -v python3.12 &> /dev/null; then
    print_error "Python 3.12 is required but not installed"
    print_status "Installing Python 3.12..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3.12 python3.12-dev python3.12-venv build-essential
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3.12 python3.12-devel gcc gcc-c++ make
    else
        print_error "Please install Python 3.12 manually"
        exit 1
    fi
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_status "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
elif [[ $(node --version | cut -d'v' -f2 | cut -d'.' -f1) -lt 22 ]]; then
    print_error "Node.js 22+ is required. Current version: $(node --version)"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    print_status "Please log out and back in for Docker permissions to take effect"
fi

# Check Poetry
if ! command -v poetry &> /dev/null; then
    print_status "Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3.12 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Navigate to OpenHands directory
cd "$OPENHANDS_DIR"

print_status "Building OpenHands..."
make build

print_success "OpenHands build completed!"

# Create optimized configuration
print_status "Creating optimized configuration..."

cat > "$CONFIG_DIR/config.toml" << 'EOF'
###################### OpenHands High-Quality Configuration ######################
# Optimized for production-grade local deployment
##############################################################################

[core]
# Workspace configuration
workspace_base = "~/openhands-workspace"
cache_dir = "~/.cache/openhands"

# Performance settings
max_iterations = 1000
max_budget_per_task = 10.0
enable_browser = true
run_as_openhands = true
runtime = "docker"
default_agent = "CodeActAgent"

# Quality settings
debug = false
save_trajectory_path = "~/.openhands/trajectories"
save_screenshots_in_trajectory = true
enable_default_condenser = true
max_concurrent_conversations = 5
conversation_max_age_seconds = 86400  # 24 hours

# File handling
file_store = "local"
file_store_path = "~/.openhands/file_store"
file_uploads_max_file_size_mb = 100
file_uploads_restrict_file_types = false

[llm]
# Default to GPT-4o for best quality (user can change)
model = "gpt-4o"
api_key = ""
temperature = 0.1
max_input_tokens = 128000
max_output_tokens = 4096
num_retries = 5
retry_max_wait = 60
retry_min_wait = 5
retry_multiplier = 2.0
caching_prompt = true
native_tool_calling = false

[llm.claude]
# Claude Sonnet for premium quality
model = "anthropic/claude-3-5-sonnet-20241022"
api_key = ""
temperature = 0.1
max_input_tokens = 200000
max_output_tokens = 8192

[llm.gpt4o-mini]
# Cost-effective option
model = "gpt-4o-mini"
api_key = ""
temperature = 0.1

[agent]
# Enable all quality features
enable_browsing = true
enable_llm_editor = true
enable_editor = true
enable_jupyter = true
enable_cmd = true
enable_think = true
enable_finish = true
enable_history_truncation = true
enable_condensation_request = true
enable_prompt_extensions = true

# Microagents for enhanced capabilities
disabled_microagents = []

[agent.CodeActAgent]
# Primary agent with full capabilities
llm_config = "llm"

[sandbox]
# Runtime configuration
timeout = 300
user_id = 1000
base_container_image = "docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik"
use_host_network = false
enable_auto_lint = true
initialize_plugins = true
keep_runtime_alive = true
pause_closed_runtimes = true
close_delay = 600
enable_gpu = false

# Security settings
[security]
confirmation_mode = false
enable_security_analyzer = true
security_analyzer = "default"

# Condenser for conversation management
[condenser]
type = "llm"
llm_config = "llm"
keep_first = 2
max_size = 150

[llm.condenser]
model = "gpt-4o-mini"
temperature = 0.1
max_input_tokens = 4096
EOF

print_success "Configuration created at $CONFIG_DIR/config.toml"

# Create startup script
print_status "Creating startup script..."

cat > "$HOME/start_openhands.sh" << EOF
#!/bin/bash

# OpenHands Startup Script
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "\${GREEN}🚀 Starting OpenHands...${NC}"

# Navigate to OpenHands directory
cd "$OPENHANDS_DIR"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "\${YELLOW}Starting Docker...${NC}"
    sudo systemctl start docker
    sleep 3
fi

# Pull latest runtime image
echo -e "\${YELLOW}Pulling latest runtime image...${NC}"
docker pull docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik

# Start OpenHands
echo -e "\${GREEN}Starting OpenHands web interface...${NC}"
export OPENHANDS_CONFIG_FILE="$CONFIG_DIR/config.toml"
make run

echo -e "\${GREEN}OpenHands is running at http://localhost:3000${NC}"
EOF

chmod +x "$HOME/start_openhands.sh"

# Create management script
cat > "$HOME/manage_openhands.sh" << 'EOF'
#!/bin/bash

# OpenHands Management Script
set -e

OPENHANDS_DIR="/workspace/OpenHands"
CONFIG_DIR="$HOME/.openhands"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

show_help() {
    echo -e "${GREEN}OpenHands Management Script${NC}"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       Start OpenHands"
    echo "  stop        Stop OpenHands"
    echo "  restart     Restart OpenHands"
    echo "  update      Update OpenHands to latest version"
    echo "  config      Edit configuration"
    echo "  logs        Show logs"
    echo "  status      Show status"
    echo "  clean       Clean up containers and cache"
    echo "  help        Show this help"
}

start_openhands() {
    echo -e "${GREEN}Starting OpenHands...${NC}"
    cd "$OPENHANDS_DIR"
    export OPENHANDS_CONFIG_FILE="$CONFIG_DIR/config.toml"
    make run
}

stop_openhands() {
    echo -e "${YELLOW}Stopping OpenHands...${NC}"
    pkill -f "uvicorn openhands.server.listen:app" || true
    pkill -f "npm run dev" || true
    docker stop $(docker ps -q --filter "name=openhands") 2>/dev/null || true
    echo -e "${GREEN}OpenHands stopped${NC}"
}

update_openhands() {
    echo -e "${YELLOW}Updating OpenHands...${NC}"
    cd "$OPENHANDS_DIR"
    git pull origin main
    make build
    echo -e "${GREEN}OpenHands updated${NC}"
}

show_status() {
    echo -e "${BLUE}OpenHands Status:${NC}"
    if pgrep -f "uvicorn openhands.server.listen:app" > /dev/null; then
        echo -e "${GREEN}✓ Backend is running${NC}"
    else
        echo -e "${RED}✗ Backend is not running${NC}"
    fi
    
    if pgrep -f "npm run dev" > /dev/null; then
        echo -e "${GREEN}✓ Frontend is running${NC}"
    else
        echo -e "${RED}✗ Frontend is not running${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}Docker containers:${NC}"
    docker ps --filter "name=openhands" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
}

clean_up() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    docker system prune -f
    docker volume prune -f
    rm -rf ~/.cache/openhands/*
    echo -e "${GREEN}Cleanup completed${NC}"
}

case "$1" in
    start)
        start_openhands
        ;;
    stop)
        stop_openhands
        ;;
    restart)
        stop_openhands
        sleep 2
        start_openhands
        ;;
    update)
        stop_openhands
        update_openhands
        ;;
    config)
        ${EDITOR:-nano} "$CONFIG_DIR/config.toml"
        ;;
    logs)
        tail -f logs/*.log 2>/dev/null || echo "No logs found"
        ;;
    status)
        show_status
        ;;
    clean)
        clean_up
        ;;
    help|*)
        show_help
        ;;
esac
EOF

chmod +x "$HOME/manage_openhands.sh"

# Create quality agents configuration
print_status "Setting up quality agents..."

mkdir -p "$CONFIG_DIR/agents"

cat > "$CONFIG_DIR/agents/quality_coder.py" << 'EOF'
"""
High-Quality Coding Agent
Optimized for production-grade code generation and problem solving
"""

from openhands.agenthub.codeact_agent.codeact_agent import CodeActAgent
from openhands.core.config import AgentConfig

class QualityCoderAgent(CodeActAgent):
    """Enhanced CodeAct agent with quality-focused prompts and behaviors"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        
        # Enhanced system prompt for quality
        self.system_prompt = """You are a world-class software engineer with expertise in:
        - Writing clean, maintainable, and efficient code
        - Following best practices and design patterns
        - Comprehensive testing and debugging
        - Security-conscious development
        - Performance optimization
        - Documentation and code clarity

        Always:
        1. Write production-ready code with proper error handling
        2. Include comprehensive comments and documentation
        3. Follow language-specific best practices
        4. Consider security implications
        5. Optimize for performance and maintainability
        6. Write tests when appropriate
        7. Use meaningful variable and function names
        8. Handle edge cases properly

        When solving problems:
        1. Analyze the requirements thoroughly
        2. Plan your approach before coding
        3. Break down complex problems into smaller parts
        4. Test your solutions comprehensively
        5. Provide clear explanations of your approach
        """

    def get_quality_guidelines(self):
        """Return quality guidelines for code generation"""
        return {
            "code_style": "Follow PEP 8 for Python, Google Style for other languages",
            "error_handling": "Always include proper error handling and validation",
            "testing": "Write unit tests for critical functionality",
            "documentation": "Include docstrings and inline comments",
            "security": "Validate inputs and handle sensitive data properly",
            "performance": "Consider time and space complexity",
            "maintainability": "Write code that's easy to read and modify"
        }
EOF

# Create enhanced microagents
print_status "Setting up enhanced microagents..."

mkdir -p "$CONFIG_DIR/microagents"

cat > "$CONFIG_DIR/microagents/code_quality.md" << 'EOF'
# Code Quality Microagent

You are a code quality specialist. When reviewing or writing code:

## Code Standards
- Follow language-specific style guides (PEP 8 for Python, etc.)
- Use meaningful variable and function names
- Keep functions small and focused (single responsibility)
- Avoid code duplication (DRY principle)
- Write self-documenting code with clear logic flow

## Error Handling
- Always validate inputs and handle edge cases
- Use appropriate exception handling mechanisms
- Provide meaningful error messages
- Log errors appropriately for debugging

## Security Best Practices
- Validate and sanitize all user inputs
- Use parameterized queries for database operations
- Handle sensitive data (passwords, tokens) securely
- Implement proper authentication and authorization
- Follow OWASP security guidelines

## Performance Considerations
- Choose appropriate data structures and algorithms
- Avoid premature optimization but consider performance implications
- Use caching where appropriate
- Minimize resource usage (memory, CPU, I/O)
- Profile code when performance is critical

## Testing
- Write unit tests for critical functionality
- Include edge cases and error conditions in tests
- Use descriptive test names that explain what's being tested
- Maintain good test coverage
- Write integration tests for complex workflows

## Documentation
- Include docstrings for all public functions and classes
- Write clear inline comments for complex logic
- Maintain up-to-date README files
- Document API endpoints and data structures
- Include usage examples where helpful
EOF

cat > "$CONFIG_DIR/microagents/debugging.md" << 'EOF'
# Debugging Microagent

You are a debugging specialist. When troubleshooting issues:

## Systematic Debugging Approach
1. **Reproduce the issue** - Understand the exact conditions that cause the problem
2. **Gather information** - Collect logs, error messages, and system state
3. **Form hypotheses** - Based on symptoms, identify potential root causes
4. **Test hypotheses** - Use debugging tools and techniques to validate theories
5. **Fix and verify** - Implement solution and confirm it resolves the issue

## Debugging Techniques
- Use print statements or logging for tracing execution flow
- Leverage debugger tools (pdb for Python, gdb for C/C++, browser dev tools)
- Check system resources (memory, CPU, disk space)
- Examine network connectivity and API responses
- Review recent changes that might have introduced the issue

## Common Issue Categories
- **Logic errors** - Incorrect algorithms or conditional statements
- **Runtime errors** - Null pointer exceptions, array bounds, type mismatches
- **Performance issues** - Slow queries, memory leaks, inefficient algorithms
- **Integration problems** - API failures, database connectivity, service dependencies
- **Configuration issues** - Environment variables, file permissions, network settings

## Best Practices
- Start with the most likely causes based on error symptoms
- Use binary search approach to isolate the problem area
- Keep detailed notes of what you've tried and the results
- Don't make multiple changes at once - test one fix at a time
- Consider rollback strategies if fixes introduce new issues
EOF

# Create Docker optimization
print_status "Optimizing Docker configuration..."

cat > "$CONFIG_DIR/docker-compose.override.yml" << 'EOF'
version: '3.8'

services:
  openhands:
    environment:
      - OPENHANDS_CONFIG_FILE=/app/config.toml
      - LOG_LEVEL=INFO
      - PYTHONUNBUFFERED=1
    volumes:
      - ~/.openhands/config.toml:/app/config.toml:ro
      - ~/.openhands/trajectories:/app/trajectories
      - ~/.openhands/file_store:/app/file_store
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
EOF

# Create quality assurance script
cat > "$HOME/qa_openhands.sh" << 'EOF'
#!/bin/bash

# OpenHands Quality Assurance Script
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔍 OpenHands Quality Assurance Check${NC}"

# Check configuration
echo -e "${YELLOW}Checking configuration...${NC}"
if [ -f "$HOME/.openhands/config.toml" ]; then
    echo -e "${GREEN}✓ Configuration file exists${NC}"
else
    echo -e "${RED}✗ Configuration file missing${NC}"
    exit 1
fi

# Check API keys
echo -e "${YELLOW}Checking API configuration...${NC}"
if grep -q 'api_key = ""' "$HOME/.openhands/config.toml"; then
    echo -e "${YELLOW}⚠ API keys not configured. Please set your LLM API keys.${NC}"
fi

# Check Docker
echo -e "${YELLOW}Checking Docker...${NC}"
if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Docker is running${NC}"
else
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi

# Check runtime image
echo -e "${YELLOW}Checking runtime image...${NC}"
if docker images | grep -q "docker.all-hands.dev/all-hands-ai/runtime"; then
    echo -e "${GREEN}✓ Runtime image available${NC}"
else
    echo -e "${YELLOW}⚠ Pulling runtime image...${NC}"
    docker pull docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik
fi

# Check workspace
echo -e "${YELLOW}Checking workspace...${NC}"
if [ -d "$HOME/openhands-workspace" ]; then
    echo -e "${GREEN}✓ Workspace directory exists${NC}"
else
    echo -e "${YELLOW}⚠ Creating workspace directory...${NC}"
    mkdir -p "$HOME/openhands-workspace"
fi

echo -e "${GREEN}✅ Quality assurance check completed${NC}"
EOF

chmod +x "$HOME/qa_openhands.sh"

# Create API key setup script
cat > "$HOME/setup_api_keys.sh" << 'EOF'
#!/bin/bash

# API Key Setup Script
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

CONFIG_FILE="$HOME/.openhands/config.toml"

echo -e "${GREEN}🔑 OpenHands API Key Setup${NC}"
echo ""
echo -e "${BLUE}This script will help you configure API keys for LLM providers.${NC}"
echo -e "${BLUE}You can skip any provider by pressing Enter without typing a key.${NC}"
echo ""

# OpenAI API Key
echo -e "${YELLOW}OpenAI API Key (for GPT-4o, GPT-4o-mini):${NC}"
read -p "Enter your OpenAI API key: " openai_key
if [ ! -z "$openai_key" ]; then
    sed -i "s/api_key = \"\"/api_key = \"$openai_key\"/" "$CONFIG_FILE"
    echo -e "${GREEN}✓ OpenAI API key configured${NC}"
fi

# Anthropic API Key
echo -e "${YELLOW}Anthropic API Key (for Claude models):${NC}"
read -p "Enter your Anthropic API key: " anthropic_key
if [ ! -z "$anthropic_key" ]; then
    sed -i "/\[llm\.claude\]/,/\[/ s/api_key = \"\"/api_key = \"$anthropic_key\"/" "$CONFIG_FILE"
    echo -e "${GREEN}✓ Anthropic API key configured${NC}"
fi

echo ""
echo -e "${GREEN}✅ API key setup completed!${NC}"
echo -e "${BLUE}You can now start OpenHands with: ~/start_openhands.sh${NC}"
EOF

chmod +x "$HOME/setup_api_keys.sh"

print_success "Setup completed successfully!"

echo ""
echo -e "${GREEN}🎉 OpenHands High-Quality Setup Complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Configure your API keys: ${YELLOW}~/setup_api_keys.sh${NC}"
echo -e "2. Run quality check: ${YELLOW}~/qa_openhands.sh${NC}"
echo -e "3. Start OpenHands: ${YELLOW}~/start_openhands.sh${NC}"
echo -e "4. Manage OpenHands: ${YELLOW}~/manage_openhands.sh help${NC}"
echo ""
echo -e "${BLUE}Configuration file: ${YELLOW}$CONFIG_DIR/config.toml${NC}"
echo -e "${BLUE}Workspace directory: ${YELLOW}$WORKSPACE_DIR${NC}"
echo ""
echo -e "${GREEN}OpenHands will be available at: http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}For best quality, use Claude Sonnet or GPT-4o models.${NC}"