#!/bin/bash

# GitHub Repository Creation Script
# Creates a GitHub repository for OpenHands Premium Setup

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 GitHub Repository Creation Script${NC}"

# Check if GitHub token is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}GitHub token not found in environment variables.${NC}"
    read -p "Enter your GitHub token: " GITHUB_TOKEN
    
    if [ -z "$GITHUB_TOKEN" ]; then
        echo -e "${RED}Error: GitHub token is required.${NC}"
        exit 1
    fi
fi

# Get GitHub username
echo -e "${YELLOW}Getting GitHub username...${NC}"
USERNAME=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)

if [ -z "$USERNAME" ]; then
    echo -e "${RED}Error: Could not get GitHub username. Check your token.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ GitHub username: $USERNAME${NC}"

# Repository name
REPO_NAME="openhands-premium-setup"
echo -e "${YELLOW}Repository name: $REPO_NAME${NC}"

# Create repository
echo -e "${YELLOW}Creating repository...${NC}"
RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
    -d "{\"name\":\"$REPO_NAME\",\"description\":\"OpenHands Premium Setup with enhanced features\",\"private\":false}" \
    https://api.github.com/user/repos)

if echo "$RESPONSE" | grep -q "errors"; then
    if echo "$RESPONSE" | grep -q "name already exists"; then
        echo -e "${YELLOW}Repository already exists. Continuing...${NC}"
    else
        echo -e "${RED}Error creating repository:${NC}"
        echo "$RESPONSE"
        exit 1
    fi
else
    echo -e "${GREEN}✓ Repository created successfully${NC}"
fi

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: OpenHands Premium Setup"
fi

# Add remote
echo -e "${YELLOW}Adding remote...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://$USERNAME:$GITHUB_TOKEN@github.com/$USERNAME/$REPO_NAME.git"

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push -u origin main --force

echo -e "${GREEN}✅ Repository setup completed!${NC}"
echo -e "${BLUE}Repository URL: https://github.com/$USERNAME/$REPO_NAME${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Clone the repository on your local machine:"
echo -e "   git clone https://github.com/$USERNAME/$REPO_NAME.git"
echo -e "2. Follow the instructions in QUICK_START.md"