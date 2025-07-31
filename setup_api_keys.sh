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