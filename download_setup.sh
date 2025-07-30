#!/bin/bash

# OpenHands Premium Setup - Download Script
# This script creates a downloadable package of all setup files

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}📦 Creating OpenHands Premium Setup Package${NC}"

# Create package directory
PACKAGE_DIR="openhands-premium-setup"
mkdir -p "$PACKAGE_DIR"

# Copy all files except OpenHands directory
echo -e "${YELLOW}Copying files...${NC}"

# Main files
cp README.md "$PACKAGE_DIR/"
cp LICENSE "$PACKAGE_DIR/"
cp QUICK_START.md "$PACKAGE_DIR/"
cp .gitignore "$PACKAGE_DIR/"
cp enhanced_config.toml "$PACKAGE_DIR/"
cp quality_agents.py "$PACKAGE_DIR/"
cp advanced_microagents.py "$PACKAGE_DIR/"
cp deployment_script.py "$PACKAGE_DIR/"
cp web_enhancements.js "$PACKAGE_DIR/"
cp setup_openhands.sh "$PACKAGE_DIR/"
cp complete_setup.py "$PACKAGE_DIR/"
cp create_github_repo.sh "$PACKAGE_DIR/"

# Scripts directory
mkdir -p "$PACKAGE_DIR/scripts"
cp scripts/install_dependencies.sh "$PACKAGE_DIR/scripts/"

# Make scripts executable
chmod +x "$PACKAGE_DIR"/*.sh
chmod +x "$PACKAGE_DIR"/*.py
chmod +x "$PACKAGE_DIR/scripts"/*.sh

# Create archive
echo -e "${YELLOW}Creating archive...${NC}"
tar -czf openhands-premium-setup.tar.gz "$PACKAGE_DIR"
zip -r openhands-premium-setup.zip "$PACKAGE_DIR"

echo -e "${GREEN}✅ Package created successfully!${NC}"
echo
echo -e "${BLUE}Files created:${NC}"
echo "📁 openhands-premium-setup/ (directory)"
echo "📦 openhands-premium-setup.tar.gz"
echo "📦 openhands-premium-setup.zip"
echo
echo -e "${YELLOW}To download:${NC}"
echo "1. Download the .tar.gz or .zip file"
echo "2. Extract on your local machine"
echo "3. Follow the QUICK_START.md guide"

# List contents
echo -e "${BLUE}Package contents:${NC}"
ls -la "$PACKAGE_DIR"