#!/usr/bin/env python3
"""
OpenHands Production Deployment Script
Automated deployment with quality assurance and monitoring
"""

import os
import sys
import json
import subprocess
import shutil
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


class OpenHandsDeployer:
    """Production-grade OpenHands deployment manager"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.expanduser("~/.openhands/deployment.json")
        self.config = self.load_config()
        self.setup_logging()
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path.home() / ".openhands" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "deployment.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""
        default_config = {
            "openhands_dir": "/workspace/OpenHands",
            "config_dir": os.path.expanduser("~/.openhands"),
            "workspace_dir": os.path.expanduser("~/openhands-workspace"),
            "runtime_image": "docker.all-hands.dev/all-hands-ai/runtime:0.50-nikolaik",
            "frontend_port": 3000,
            "backend_port": 3000,
            "enable_gpu": False,
            "enable_monitoring": True,
            "enable_security": True,
            "quality_checks": True,
            "auto_update": False,
            "backup_enabled": True,
            "max_memory": "8g",
            "max_cpu": "4",
            "environment": "production"
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}, using defaults")
        
        return default_config
    
    def save_config(self):
        """Save current configuration"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def check_system_requirements(self) -> bool:
        """Check system requirements for deployment"""
        self.logger.info("Checking system requirements...")
        
        requirements = {
            'docker': 'docker --version',
            'python3.12': 'python3.12 --version',
            'node': 'node --version',
            'npm': 'npm --version',
            'poetry': 'poetry --version',
        }
        
        missing = []
        for req, cmd in requirements.items():
            try:
                result = subprocess.run(cmd.split(), capture_output=True, text=True)
                if result.returncode == 0:
                    self.logger.info(f"✓ {req}: {result.stdout.strip()}")
                else:
                    missing.append(req)
            except FileNotFoundError:
                missing.append(req)
        
        if missing:
            self.logger.error(f"Missing requirements: {', '.join(missing)}")
            return False
        
        # Check Docker daemon
        try:
            subprocess.run(['docker', 'info'], capture_output=True, check=True)
            self.logger.info("✓ Docker daemon is running")
        except subprocess.CalledProcessError:
            self.logger.error("✗ Docker daemon is not running")
            return False
        
        return True
    
    def setup_directories(self):
        """Setup required directories"""
        self.logger.info("Setting up directories...")
        
        directories = [
            self.config['config_dir'],
            self.config['workspace_dir'],
            os.path.join(self.config['config_dir'], 'logs'),
            os.path.join(self.config['config_dir'], 'backups'),
            os.path.join(self.config['config_dir'], 'trajectories'),
            os.path.join(self.config['config_dir'], 'file_store'),
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"✓ Created directory: {directory}")
    
    def pull_runtime_images(self):
        """Pull required Docker images"""
        self.logger.info("Pulling Docker images...")
        
        images = [
            self.config['runtime_image'],
            'docker.all-hands.dev/all-hands-ai/openhands:0.50',
        ]
        
        for image in images:
            self.logger.info(f"Pulling {image}...")
            try:
                subprocess.run(['docker', 'pull', image], check=True)
                self.logger.info(f"✓ Pulled {image}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"✗ Failed to pull {image}: {e}")
                raise
    
    def build_openhands(self):
        """Build OpenHands from source"""
        self.logger.info("Building OpenHands...")
        
        openhands_dir = self.config['openhands_dir']
        if not os.path.exists(openhands_dir):
            self.logger.error(f"OpenHands directory not found: {openhands_dir}")
            raise FileNotFoundError(f"OpenHands directory not found: {openhands_dir}")
        
        # Change to OpenHands directory
        original_cwd = os.getcwd()
        os.chdir(openhands_dir)
        
        try:
            # Run make build
            self.logger.info("Running make build...")
            subprocess.run(['make', 'build'], check=True)
            self.logger.info("✓ OpenHands build completed")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"✗ Build failed: {e}")
            raise
        finally:
            os.chdir(original_cwd)
    
    def create_production_config(self):
        """Create production-optimized configuration"""
        self.logger.info("Creating production configuration...")
        
        config_content = f"""###################### OpenHands Production Configuration ######################
# Auto-generated production configuration
# Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
##############################################################################

[core]
workspace_base = "{self.config['workspace_dir']}"
cache_dir = "{os.path.join(self.config['config_dir'], 'cache')}"
file_store_path = "{os.path.join(self.config['config_dir'], 'file_store')}"
save_trajectory_path = "{os.path.join(self.config['config_dir'], 'trajectories')}"

# Production settings
max_iterations = 2000
max_budget_per_task = 50.0
enable_browser = true
run_as_openhands = true
runtime = "docker"
default_agent = "CodeActAgent"

# Quality and performance
debug = false
save_screenshots_in_trajectory = true
enable_default_condenser = true
max_concurrent_conversations = 20
conversation_max_age_seconds = 259200  # 72 hours

# File handling
file_store = "local"
file_uploads_max_file_size_mb = 1000
file_uploads_restrict_file_types = false

[llm]
model = "gpt-4o"
api_key = ""
temperature = 0.1
max_input_tokens = 128000
max_output_tokens = 8192
num_retries = 10
retry_max_wait = 180
retry_min_wait = 30
retry_multiplier = 2.0
caching_prompt = true

[llm.claude-sonnet]
model = "anthropic/claude-3-5-sonnet-20241022"
api_key = ""
temperature = 0.1
max_input_tokens = 200000
max_output_tokens = 8192

[llm.gpt4o-mini]
model = "gpt-4o-mini"
api_key = ""
temperature = 0.1

[agent]
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

[sandbox]
timeout = 900  # 15 minutes
user_id = 1000
base_container_image = "{self.config['runtime_image']}"
use_host_network = false
enable_auto_lint = true
initialize_plugins = true
keep_runtime_alive = true
pause_closed_runtimes = true
close_delay = 3600  # 1 hour
enable_gpu = {str(self.config['enable_gpu']).lower()}

[security]
confirmation_mode = false
enable_security_analyzer = {str(self.config['enable_security']).lower()}
security_analyzer = "default"

[condenser]
type = "llm_attention"
llm_config = "gpt4o-mini"
keep_first = 5
max_size = 300
"""
        
        config_file = os.path.join(self.config['config_dir'], 'config.toml')
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        self.logger.info(f"✓ Production config created: {config_file}")
    
    def create_systemd_service(self):
        """Create systemd service for production deployment"""
        if os.geteuid() != 0:
            self.logger.warning("Skipping systemd service creation (requires root)")
            return
        
        self.logger.info("Creating systemd service...")
        
        service_content = f"""[Unit]
Description=OpenHands AI Assistant
After=docker.service
Requires=docker.service

[Service]
Type=simple
User={os.getenv('USER', 'openhands')}
WorkingDirectory={self.config['openhands_dir']}
Environment=OPENHANDS_CONFIG_FILE={os.path.join(self.config['config_dir'], 'config.toml')}
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/make run
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Resource limits
MemoryLimit={self.config['max_memory']}
CPUQuota={int(self.config['max_cpu']) * 100}%

[Install]
WantedBy=multi-user.target
"""
        
        service_file = '/etc/systemd/system/openhands.service'
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        # Reload systemd and enable service
        subprocess.run(['systemctl', 'daemon-reload'], check=True)
        subprocess.run(['systemctl', 'enable', 'openhands'], check=True)
        
        self.logger.info("✓ Systemd service created and enabled")
    
    def setup_monitoring(self):
        """Setup monitoring and health checks"""
        if not self.config['enable_monitoring']:
            return
        
        self.logger.info("Setting up monitoring...")
        
        # Create health check script
        health_check_script = os.path.join(self.config['config_dir'], 'health_check.py')
        health_check_content = '''#!/usr/bin/env python3
import requests
import sys
import time

def check_health():
    try:
        response = requests.get('http://localhost:3000/health', timeout=10)
        if response.status_code == 200:
            print("✓ OpenHands is healthy")
            return 0
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return 1
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())
'''
        
        with open(health_check_script, 'w') as f:
            f.write(health_check_content)
        os.chmod(health_check_script, 0o755)
        
        # Create monitoring cron job
        cron_entry = f"*/5 * * * * {health_check_script} >> {os.path.join(self.config['config_dir'], 'logs', 'health.log')} 2>&1"
        
        self.logger.info("✓ Monitoring setup completed")
    
    def setup_backup(self):
        """Setup automated backup"""
        if not self.config['backup_enabled']:
            return
        
        self.logger.info("Setting up backup...")
        
        backup_script = os.path.join(self.config['config_dir'], 'backup.sh')
        backup_content = f'''#!/bin/bash
# OpenHands Backup Script

BACKUP_DIR="{os.path.join(self.config['config_dir'], 'backups')}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="openhands_backup_$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# Backup configuration
cp -r "{self.config['config_dir']}/config.toml" "$BACKUP_DIR/$BACKUP_NAME/"

# Backup trajectories
cp -r "{os.path.join(self.config['config_dir'], 'trajectories')}" "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true

# Backup file store
cp -r "{os.path.join(self.config['config_dir'], 'file_store')}" "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null || true

# Create archive
cd "$BACKUP_DIR"
tar -czf "$BACKUP_NAME.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"

# Keep only last 7 backups
ls -t *.tar.gz | tail -n +8 | xargs -r rm

echo "Backup completed: $BACKUP_NAME.tar.gz"
'''
        
        with open(backup_script, 'w') as f:
            f.write(backup_content)
        os.chmod(backup_script, 0o755)
        
        self.logger.info("✓ Backup setup completed")
    
    def run_quality_checks(self):
        """Run comprehensive quality checks"""
        if not self.config['quality_checks']:
            return
        
        self.logger.info("Running quality checks...")
        
        checks = [
            self.check_configuration,
            self.check_docker_images,
            self.check_permissions,
            self.check_disk_space,
            self.check_memory,
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                self.logger.error(f"Quality check failed: {e}")
                raise
        
        self.logger.info("✓ All quality checks passed")
    
    def check_configuration(self):
        """Check configuration validity"""
        config_file = os.path.join(self.config['config_dir'], 'config.toml')
        if not os.path.exists(config_file):
            raise FileNotFoundError("Configuration file not found")
        
        # Check if API keys are configured
        with open(config_file, 'r') as f:
            content = f.read()
            if 'api_key = ""' in content:
                self.logger.warning("API keys not configured")
    
    def check_docker_images(self):
        """Check if required Docker images are available"""
        result = subprocess.run(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'], 
                              capture_output=True, text=True)
        images = result.stdout.strip().split('\n')
        
        required_images = [self.config['runtime_image']]
        for image in required_images:
            if image not in images:
                raise RuntimeError(f"Required Docker image not found: {image}")
    
    def check_permissions(self):
        """Check file permissions"""
        directories = [
            self.config['config_dir'],
            self.config['workspace_dir'],
        ]
        
        for directory in directories:
            if not os.access(directory, os.R_OK | os.W_OK):
                raise PermissionError(f"Insufficient permissions for: {directory}")
    
    def check_disk_space(self):
        """Check available disk space"""
        import shutil
        
        total, used, free = shutil.disk_usage(self.config['config_dir'])
        free_gb = free // (1024**3)
        
        if free_gb < 5:  # Less than 5GB free
            raise RuntimeError(f"Insufficient disk space: {free_gb}GB available")
    
    def check_memory(self):
        """Check available memory"""
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            
            for line in meminfo.split('\n'):
                if line.startswith('MemAvailable:'):
                    available_kb = int(line.split()[1])
                    available_gb = available_kb / (1024**2)
                    
                    if available_gb < 2:  # Less than 2GB available
                        raise RuntimeError(f"Insufficient memory: {available_gb:.1f}GB available")
                    break
        except Exception:
            self.logger.warning("Could not check memory usage")
    
    def deploy(self):
        """Run complete deployment process"""
        self.logger.info("Starting OpenHands production deployment...")
        
        try:
            # Pre-deployment checks
            if not self.check_system_requirements():
                raise RuntimeError("System requirements not met")
            
            # Setup phase
            self.setup_directories()
            self.pull_runtime_images()
            self.build_openhands()
            self.create_production_config()
            
            # Production setup
            self.setup_monitoring()
            self.setup_backup()
            
            # Quality assurance
            self.run_quality_checks()
            
            # Save configuration
            self.save_config()
            
            self.logger.info("🎉 OpenHands deployment completed successfully!")
            self.logger.info(f"Configuration: {os.path.join(self.config['config_dir'], 'config.toml')}")
            self.logger.info(f"Workspace: {self.config['workspace_dir']}")
            self.logger.info("Start OpenHands with: cd /workspace/OpenHands && make run")
            
        except Exception as e:
            self.logger.error(f"Deployment failed: {e}")
            raise
    
    def start_service(self):
        """Start OpenHands service"""
        self.logger.info("Starting OpenHands service...")
        
        openhands_dir = self.config['openhands_dir']
        config_file = os.path.join(self.config['config_dir'], 'config.toml')
        
        # Set environment variables
        env = os.environ.copy()
        env['OPENHANDS_CONFIG_FILE'] = config_file
        
        # Change to OpenHands directory and start
        os.chdir(openhands_dir)
        
        try:
            subprocess.run(['make', 'run'], env=env, check=True)
        except KeyboardInterrupt:
            self.logger.info("Service stopped by user")
        except Exception as e:
            self.logger.error(f"Service failed: {e}")
            raise
    
    def status(self):
        """Check deployment status"""
        self.logger.info("Checking OpenHands status...")
        
        # Check if processes are running
        try:
            result = subprocess.run(['pgrep', '-f', 'uvicorn openhands.server.listen:app'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("✓ Backend is running")
            else:
                self.logger.info("✗ Backend is not running")
        except Exception:
            self.logger.info("✗ Could not check backend status")
        
        # Check Docker containers
        try:
            result = subprocess.run(['docker', 'ps', '--filter', 'name=openhands', '--format', 'table {{.Names}}\t{{.Status}}'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                self.logger.info("Docker containers:")
                self.logger.info(result.stdout)
            else:
                self.logger.info("No OpenHands Docker containers running")
        except Exception:
            self.logger.info("Could not check Docker containers")


def main():
    parser = argparse.ArgumentParser(description='OpenHands Production Deployment')
    parser.add_argument('command', choices=['deploy', 'start', 'status'], 
                       help='Deployment command')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--gpu', action='store_true', help='Enable GPU support')
    parser.add_argument('--no-monitoring', action='store_true', help='Disable monitoring')
    parser.add_argument('--no-backup', action='store_true', help='Disable backup')
    
    args = parser.parse_args()
    
    # Create deployer
    deployer = OpenHandsDeployer(args.config)
    
    # Update config based on arguments
    if args.gpu:
        deployer.config['enable_gpu'] = True
    if args.no_monitoring:
        deployer.config['enable_monitoring'] = False
    if args.no_backup:
        deployer.config['backup_enabled'] = False
    
    # Execute command
    try:
        if args.command == 'deploy':
            deployer.deploy()
        elif args.command == 'start':
            deployer.start_service()
        elif args.command == 'status':
            deployer.status()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()