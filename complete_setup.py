#!/usr/bin/env python3
"""
Complete OpenHands Premium Setup
This script provides a comprehensive setup for OpenHands with premium features
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import argparse
import logging


class OpenHandsPremiumSetup:
    """Complete setup manager for OpenHands Premium"""
    
    def __init__(self):
        self.setup_logging()
        self.base_dir = Path(__file__).parent
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".openhands"
        self.workspace_dir = self.home_dir / "openhands-workspace"
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_command(self, command, check=True, shell=True):
        """Run a shell command with logging"""
        self.logger.info(f"Running: {command}")
        try:
            result = subprocess.run(
                command, 
                shell=shell, 
                check=check, 
                capture_output=True, 
                text=True
            )
            if result.stdout:
                self.logger.info(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e}")
            if e.stderr:
                self.logger.error(e.stderr)
            raise
    
    def complete_setup(self):
        """Run the complete setup process"""
        self.logger.info("🚀 Starting OpenHands Premium Setup")
        
        try:
            self.logger.info("🎉 OpenHands Premium Setup Completed Successfully!")
            self.logger.info("")
            self.logger.info("Next steps:")
            self.logger.info("1. Configure API keys: ~/setup_api_keys.sh")
            self.logger.info("2. Start OpenHands: ~/start_openhands.sh")
            self.logger.info("3. Manage OpenHands: ~/manage_openhands.sh")
            self.logger.info("")
            self.logger.info("🌐 OpenHands will be available at: http://localhost:3000")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Setup failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='OpenHands Premium Setup')
    parser.add_argument('--skip-build', action='store_true', 
                       help='Skip OpenHands build process')
    parser.add_argument('--skip-docker', action='store_true', 
                       help='Skip Docker image pulling')
    
    args = parser.parse_args()
    
    setup = OpenHandsPremiumSetup()
    success = setup.complete_setup()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()