# SecureVault - Quick Start Guides

## 📖 ABOUT THESE GUIDES

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## 🔥 FORGE QUICK START

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use SecureVault for API key and credential management

### Step 1: Installation Check
```bash
# Verify SecureVault is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SecureVault
python securevault.py --help

# Install dependency if needed
pip install cryptography
```

### Step 2: Create Your Vault
```bash
# Initialize vault (one-time setup)
python securevault.py init

# You'll be prompted for a master password
# ⚠️ REMEMBER THIS - it cannot be recovered!
```

**Output:**
```
🔐 Creating new SecureVault...
Enter master password: ********
Confirm master password: ********
✅ Vault created successfully at C:\Users\<name>\.securevault.enc
```

### Step 3: Store API Credentials
```bash
# Add OpenAI API key
python securevault.py add openai_api

# Enter master password when prompted
# Then enter service credentials:
# Username: api_key
# Password: sk-your-actual-api-key
```

### Step 4: Retrieve Credentials
```bash
# Get stored credential
python securevault.py get openai_api

# Output:
# Service: openai_api
# Username: api_key
# Password: sk-your-actual-api-key
```

### Step 5: Common Forge Commands
```bash
# List all stored services
python securevault.py list

# Generate secure password
python securevault.py generate --length 32

# Delete a service
python securevault.py delete old_service
```

### Next Steps for Forge
1. Store all API keys (OpenAI, Anthropic, etc.)
2. Read [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) - Forge section
3. Try [EXAMPLES.md](EXAMPLES.md) - Example 3 (API key management)
4. Add credential retrieval to orchestration workflows

---

## ⚡ ATLAS QUICK START

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use SecureVault for development secrets and test credentials

### Step 1: Installation Check
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SecureVault
python -c "from securevault import SecureVault; print('OK')"

# If import fails, install dependency:
pip install cryptography
```

### Step 2: First Use - Create Vault
```bash
# Initialize if not already done
python securevault.py init
```

### Step 3: Store Development Credentials
```bash
# Store test database credentials
python securevault.py add test_database
# Username: db_user
# Password: test_password_123

# Store GitHub token
python securevault.py add github_token
# Username: token
# Password: ghp_your_github_token
```

### Step 4: Retrieve During Development
```python
# In your Python code
from securevault import SecureVault
import os

vault = SecureVault()

# For automation, use environment variable
master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
if vault.unlock(master_pass):
    db_creds = vault.get_password("test_database")
    if db_creds:
        print(f"DB User: {db_creds['username']}")
```

### Step 5: Common Atlas Commands
```bash
# List all credentials
python securevault.py list

# Generate strong password for new service
python securevault.py generate --length 24 --symbols

# Export vault backup (encrypted)
python securevault.py export backup.json
```

### Next Steps for Atlas
1. Store all development secrets
2. Add vault access to tool test fixtures
3. Never commit credentials to git
4. Use separate vaults for dev/test/prod

---

## 🐧 CLIO QUICK START

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use SecureVault in Linux environment

### Step 1: Linux Installation
```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/SecureVault.git
cd SecureVault

# Install dependency
pip3 install cryptography

# Verify
python3 securevault.py --help
```

### Step 2: Create Vault
```bash
# Initialize vault
python3 securevault.py init

# Vault stored at: ~/.securevault.enc
```

### Step 3: Store Server Credentials
```bash
# Store SSH password
python3 securevault.py add ssh_production
# Username: admin
# Password: your_ssh_password

# Store database credentials
python3 securevault.py add mysql_prod
# Username: root
# Password: database_password
```

### Step 4: Use in Shell Scripts
```bash
#!/bin/bash
# vault_ssh.sh - Connect to server using stored credentials

# Export master password (or prompt)
export VAULT_MASTER_PASSWORD="your_master_password"

# Get credentials
CREDS=$(python3 ~/SecureVault/securevault.py get ssh_production)
echo "$CREDS"

# Parse username/password (example)
# Better: use expect script or sshpass with caution
```

### Step 5: Common Clio Commands
```bash
# List all stored services
python3 securevault.py list

# Generate secure password
python3 securevault.py generate --length 32 --no-symbols

# Quick get (output to terminal)
python3 securevault.py get mysql_prod
```

### Linux Tips
- Vault file: `~/.securevault.enc`
- Add alias: `alias vault='python3 ~/SecureVault/securevault.py'`
- Use with `expect` for automated SSH
- Protect vault file: `chmod 600 ~/.securevault.enc`

### Next Steps for Clio
1. Store all server credentials
2. Create bash wrapper scripts
3. Set proper file permissions
4. Add to ABIOS startup checks

---

## 🌐 NEXUS QUICK START

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform credential management with SecureVault

### Step 1: Platform Detection
```python
import platform
from securevault import SecureVault

print(f"Platform: {platform.system()}")
# Windows / Linux / Darwin (macOS)

vault = SecureVault()
print(f"Vault location: {vault.vault_path}")
```

### Step 2: Cross-Platform Vault Creation
```bash
# Same command works on all platforms
python securevault.py init

# Vault locations:
# Windows: C:\Users\<name>\.securevault.enc
# Linux:   /home/<name>/.securevault.enc
# macOS:   /Users/<name>/.securevault.enc
```

### Step 3: Store Cross-Platform Credentials
```bash
# Store service that works on all platforms
python securevault.py add aws_credentials
# Username: AKIAXXXXXXXXXXXXXXXX
# Password: your_secret_key

# API keys work the same everywhere
python securevault.py add slack_webhook
# Username: webhook
# Password: https://hooks.slack.com/services/...
```

### Step 4: Platform-Specific Considerations
```python
from securevault import SecureVault
import platform

vault = SecureVault()

# Platform-specific handling if needed
if platform.system() == "Windows":
    # Windows-specific paths use backslashes
    print("Running on Windows")
elif platform.system() == "Linux":
    print("Running on Linux")
else:
    print("Running on macOS")

# But vault operations are identical!
vault.unlock(master_password)
creds = vault.get_password("aws_credentials")
```

### Step 5: Common Nexus Commands
```bash
# List services (works on all platforms)
python securevault.py list

# Export for backup (portable format)
python securevault.py export backup.json

# Import on another platform
python securevault.py import backup.json
```

### Next Steps for Nexus
1. Test on Windows, Linux, and macOS
2. Use portable export/import for sync
3. Report any platform-specific issues
4. Add to multi-platform workflows

---

## 🆓 BOLT QUICK START

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use SecureVault for automation without API costs

### Step 1: Verify Free Access
```bash
# No API key required!
python securevault.py --help

# Only local encryption - zero cloud costs
```

### Step 2: Quick Vault Setup
```bash
# Create vault
python securevault.py init

# Store automation secrets
python securevault.py add ci_deploy_key
# Username: deploy
# Password: your_deploy_key
```

### Step 3: Use in Automation
```bash
#!/bin/bash
# Automation script using SecureVault

# Set master password from CI secret
export VAULT_MASTER_PASSWORD="$CI_VAULT_SECRET"

# Retrieve deployment credentials
python securevault.py get ci_deploy_key

# Use in deployment...
```

### Step 4: Batch Operations
```bash
# Generate multiple passwords (no API costs!)
for i in {1..10}; do
    python securevault.py generate --length 24
done

# List all (quick, local operation)
python securevault.py list

# Backup entire vault
python securevault.py export vault_backup.json
```

### Step 5: Common Bolt Commands
```bash
# Fast local operations
python securevault.py list          # List all
python securevault.py get SERVICE   # Get one
python securevault.py generate      # New password

# Batch add (scripted)
echo -e "master_pass\nuser1\npass1" | python securevault.py add service1
```

### Cost Benefits
- Zero API calls = Zero costs
- Local encryption = No cloud fees
- Unlimited password generation
- Perfect for CI/CD pipelines

### Next Steps for Bolt
1. Add to Cline automation workflows
2. Use for all repetitive credential tasks
3. Create batch scripts for efficiency
4. Report any issues via Synapse

---

## 📚 ADDITIONAL RESOURCES

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/SecureVault/issues
- Synapse: Post in THE_SYNAPSE/active/
- Security Issues: Direct to Logan (private)

---

## 🔒 SECURITY REMINDERS

**All Agents:**
1. **Never share master password**
2. **Never log credentials**
3. **Never commit vault file to git**
4. **Use strong master passwords (16+ characters)**
5. **Backup vault file securely**

**Environment Variable Usage:**
```bash
# For automation ONLY - not interactive use
export VAULT_MASTER_PASSWORD="your_secure_master"

# Clear after use
unset VAULT_MASTER_PASSWORD
```

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
