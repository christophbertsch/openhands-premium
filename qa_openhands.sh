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

# Check disk space
echo -e "${YELLOW}Checking disk space...${NC}"
FREE_SPACE=$(df -h / | awk 'NR==2 {print $4}')
echo -e "${GREEN}✓ Available disk space: $FREE_SPACE${NC}"

# Check memory
echo -e "${YELLOW}Checking memory...${NC}"
FREE_MEM=$(free -h | awk '/^Mem:/ {print $7}')
echo -e "${GREEN}✓ Available memory: $FREE_MEM${NC}"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command -v python3.12 &> /dev/null; then
    PYTHON_VERSION=$(python3.12 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Python 3.12 not found. Using default Python version.${NC}"
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
fi

# Check Node.js version
echo -e "${YELLOW}Checking Node.js version...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not installed${NC}"
fi

# Check OpenHands directory
echo -e "${YELLOW}Checking OpenHands directory...${NC}"
if [ -d "/workspace/OpenHands" ]; then
    echo -e "${GREEN}✓ OpenHands directory exists${NC}"
else
    echo -e "${RED}✗ OpenHands directory not found${NC}"
    exit 1
fi

# Check startup scripts
echo -e "${YELLOW}Checking startup scripts...${NC}"
if [ -f "$HOME/start_openhands.sh" ]; then
    echo -e "${GREEN}✓ Startup script exists${NC}"
else
    echo -e "${RED}✗ Startup script missing${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Quality assurance check completed${NC}"