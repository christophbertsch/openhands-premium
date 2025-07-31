#!/bin/bash

# OpenHands Startup Script
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Starting OpenHands...${NC}"

# Navigate to OpenHands directory
cd "/workspace/OpenHands"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}Starting Docker...${NC}"
    sudo systemctl start docker
    sleep 3
fi

# Pull latest runtime image
echo -e "${YELLOW}Pulling latest runtime image...${NC}"
docker pull docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik

# Start OpenHands
echo -e "${GREEN}Starting OpenHands web interface...${NC}"
export OPENHANDS_CONFIG_FILE="$HOME/.openhands/config.toml"
make run

echo -e "${GREEN}OpenHands is running at http://localhost:3000${NC}"