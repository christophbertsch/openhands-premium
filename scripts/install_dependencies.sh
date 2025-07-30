#!/bin/bash

# OpenHands Dependencies Installation Script
# Installs all required dependencies for the premium setup

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🔧 Installing OpenHands Dependencies${NC}"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v apt-get &> /dev/null; then
        PACKAGE_MANAGER="apt"
    elif command -v yum &> /dev/null; then
        PACKAGE_MANAGER="yum"
    elif command -v pacman &> /dev/null; then
        PACKAGE_MANAGER="pacman"
    else
        echo -e "${RED}Unsupported Linux distribution${NC}"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PACKAGE_MANAGER="brew"
else
    echo -e "${RED}Unsupported operating system${NC}"
    exit 1
fi

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"

case $PACKAGE_MANAGER in
    "apt")
        sudo apt-get update
        sudo apt-get install -y \
            curl \
            wget \
            git \
            build-essential \
            python3.12 \
            python3.12-dev \
            python3.12-venv \
            python3-pip \
            nodejs \
            npm \
            docker.io \
            docker-compose \
            tmux \
            htop \
            jq
        ;;
    "yum")
        sudo yum update -y
        sudo yum install -y \
            curl \
            wget \
            git \
            gcc \
            gcc-c++ \
            make \
            python3.12 \
            python3.12-devel \
            nodejs \
            npm \
            docker \
            docker-compose \
            tmux \
            htop \
            jq
        ;;
    "pacman")
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm \
            curl \
            wget \
            git \
            base-devel \
            python \
            nodejs \
            npm \
            docker \
            docker-compose \
            tmux \
            htop \
            jq
        ;;
    "brew")
        brew update
        brew install \
            python@3.12 \
            node \
            docker \
            docker-compose \
            tmux \
            htop \
            jq
        ;;
esac

# Install Poetry
echo -e "${YELLOW}Installing Poetry...${NC}"
if ! command -v poetry &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3.12 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install Node.js 22 if needed
echo -e "${YELLOW}Checking Node.js version...${NC}"
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo -e "${YELLOW}Installing Node.js 22...${NC}"
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Setup Docker
echo -e "${YELLOW}Setting up Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
fi

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
if command -v systemctl &> /dev/null; then
    sudo systemctl enable docker
    sudo systemctl start docker
fi

echo -e "${GREEN}✅ Dependencies installation completed!${NC}"
echo -e "${BLUE}Please log out and back in for Docker permissions to take effect.${NC}"