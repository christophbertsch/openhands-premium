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