# How to Copy OpenHands Premium Setup to Your Local Machine

This guide will help you copy all the necessary files from this repository to your local machine.

## Option 1: Clone the Repository (Recommended)

The easiest way to get all files is to clone the repository:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/openhands-premium-setup.git
cd openhands-premium-setup

# Make scripts executable
chmod +x *.sh *.py scripts/*.sh
```

## Option 2: Download as ZIP

1. Click the "Code" button on the GitHub repository page
2. Select "Download ZIP"
3. Extract the ZIP file on your local machine
4. Make scripts executable:
   ```bash
   chmod +x *.sh *.py scripts/*.sh
   ```

## Option 3: Manual Copy (If Needed)

If you need to copy files manually, follow these steps:

1. Create the directory structure:
   ```bash
   mkdir -p ~/openhands-premium-setup/scripts
   mkdir -p ~/openhands-premium-setup/.vscode
   cd ~/openhands-premium-setup
   ```

2. Copy each file from the repository to your local machine:
   - README.md
   - LICENSE
   - QUICK_START.md
   - OPENHANDS_PREMIUM_GUIDE.md
   - COPY_TO_LOCAL.md
   - COMPLETE_FILE_LIST.md
   - setup_openhands.sh
   - enhanced_config.toml
   - quality_agents.py
   - advanced_microagents.py
   - deployment_script.py
   - web_enhancements.js
   - complete_setup.py
   - create_github_repo.sh
   - download_setup.sh
   - get-docker.sh
   - scripts/install_dependencies.sh
   - .vscode/settings.json (optional)

3. Make scripts executable:
   ```bash
   chmod +x *.sh *.py scripts/*.sh
   ```

## Verifying Your Setup

After copying all files, verify your setup:

```bash
# Check if all required files are present
ls -la

# Verify scripts are executable
ls -la *.sh *.py scripts/*.sh

# Check setup script help
./setup_openhands.sh --help
```

## Next Steps

After copying all files:

1. Configure API keys:
   ```bash
   ./setup_api_keys.sh
   ```

2. Start OpenHands:
   ```bash
   ./setup_openhands.sh
   ```

3. Access OpenHands at http://localhost:3000

## Troubleshooting

If you encounter any issues:

1. Make sure all scripts are executable (`chmod +x *.sh *.py scripts/*.sh`)
2. Check if you have all required dependencies installed
3. Verify that Docker is running
4. Check the logs in `~/.openhands/logs/`

For more detailed instructions, refer to the QUICK_START.md and OPENHANDS_PREMIUM_GUIDE.md files.