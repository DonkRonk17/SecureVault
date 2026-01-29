# SecureVault - Usage Examples

Quick navigation:
- [Example 1: First Time Setup](#example-1-first-time-setup)
- [Example 2: Store and Retrieve Credentials](#example-2-store-and-retrieve-credentials)
- [Example 3: API Key Management](#example-3-api-key-management)
- [Example 4: Generate Secure Passwords](#example-4-generate-secure-passwords)
- [Example 5: List All Services](#example-5-list-all-services)
- [Example 6: Delete Old Credentials](#example-6-delete-old-credentials)
- [Example 7: Export Backup](#example-7-export-backup)
- [Example 8: Import from Backup](#example-8-import-from-backup)
- [Example 9: Python API Usage](#example-9-python-api-usage)
- [Example 10: Automation Script](#example-10-automation-script)

---

## Example 1: First Time Setup

**Scenario:** You've just installed SecureVault and want to create your encrypted vault.

**Steps:**
```bash
# Navigate to SecureVault
cd C:\Users\logan\OneDrive\Documents\AutoProjects\SecureVault

# Initialize your vault
python securevault.py init
```

**Prompts and Responses:**
```
🔐 Creating new SecureVault...

Enter master password: ****************
Confirm master password: ****************

✅ Vault created successfully at C:\Users\logan\.securevault.enc

💡 IMPORTANT:
- Remember your master password - it cannot be recovered!
- Your passwords are encrypted with AES-256
- Vault is stored locally - no cloud sync
```

**What You Learned:**
- How to create a new vault
- Master password is required and unrecoverable
- Vault location on your system

---

## Example 2: Store and Retrieve Credentials

**Scenario:** Store login credentials for a website and retrieve them later.

**Steps:**
```bash
# Add a new credential
python securevault.py add gmail_personal

# Follow prompts:
# Master password: [your master password]
# Username: myemail@gmail.com
# Password: MyGmailPassword123!
```

**Output:**
```
🔓 Vault unlocked
Enter username: myemail@gmail.com
Enter password: 
✅ Added: gmail_personal
```

**Retrieve Later:**
```bash
python securevault.py get gmail_personal
```

**Output:**
```
🔓 Vault unlocked

═══════════════════════════════════════
  Service: gmail_personal
═══════════════════════════════════════
  Username: myemail@gmail.com
  Password: MyGmailPassword123!
═══════════════════════════════════════
```

**What You Learned:**
- How to add credentials with `add`
- How to retrieve with `get`
- Credentials are displayed securely after unlocking

---

## Example 3: API Key Management

**Scenario:** Store and manage API keys for various services.

**Steps:**
```bash
# Store OpenAI API key
python securevault.py add openai_api
# Username: api_key
# Password: sk-proj-your-openai-api-key-here

# Store Anthropic API key
python securevault.py add anthropic_api
# Username: api_key
# Password: sk-ant-your-anthropic-key-here

# Store GitHub personal access token
python securevault.py add github_token
# Username: token
# Password: ghp_your_github_token_here
```

**Retrieve for Use:**
```bash
# Get OpenAI key
python securevault.py get openai_api

# Output:
# Service: openai_api
# Username: api_key
# Password: sk-proj-your-openai-api-key-here
```

**What You Learned:**
- Store API keys like any credential
- Use descriptive service names
- Username field can be used for key type

---

## Example 4: Generate Secure Passwords

**Scenario:** Generate strong, random passwords for new accounts.

**Steps:**
```bash
# Generate default password (16 chars, letters, numbers, symbols)
python securevault.py generate

# Output:
# Generated password: kX9#mP2$wQ7@nL4!
```

**Custom Options:**
```bash
# Longer password (24 characters)
python securevault.py generate --length 24

# Output: X9m#kP2$wQ7@nL4!rT8^yU5*

# No symbols (for restrictive sites)
python securevault.py generate --length 20 --no-symbols

# Output: X9mkP2wQ7nL4rT8yU5mK
```

**What You Learned:**
- Generate random passwords instantly
- Customize length and character sets
- No master password needed for generation

---

## Example 5: List All Services

**Scenario:** See all credentials stored in your vault.

**Steps:**
```bash
python securevault.py list
```

**Output:**
```
🔓 Vault unlocked

═══════════════════════════════════════
  STORED SERVICES (5 total)
═══════════════════════════════════════

  1. gmail_personal
  2. openai_api
  3. anthropic_api
  4. github_token
  5. aws_credentials

═══════════════════════════════════════
```

**What You Learned:**
- View all stored services at a glance
- Credentials are not displayed (only names)
- Use `get` to retrieve specific credentials

---

## Example 6: Delete Old Credentials

**Scenario:** Remove credentials you no longer need.

**Steps:**
```bash
# Delete a service
python securevault.py delete old_service
```

**Output:**
```
🔓 Vault unlocked
⚠️  Delete 'old_service'? This cannot be undone.
Confirm (yes/no): yes
✅ Deleted: old_service
```

**What You Learned:**
- Delete with confirmation prompt
- Action is permanent (no undo)
- Regularly clean up old credentials

---

## Example 7: Export Backup

**Scenario:** Create a backup of your vault for safekeeping.

**Steps:**
```bash
# Export to encrypted backup file
python securevault.py export vault_backup.json
```

**Output:**
```
🔓 Vault unlocked
✅ Exported 5 services to: vault_backup.json
💡 Store this backup securely - it contains encrypted data
```

**Backup File:**
```json
{
  "exported": "2026-01-28T12:00:00Z",
  "services_count": 5,
  "encrypted_data": "base64_encoded_encrypted_vault_data..."
}
```

**What You Learned:**
- Export creates encrypted backup
- Backup requires master password to restore
- Store backups in secure location

---

## Example 8: Import from Backup

**Scenario:** Restore credentials from a backup file.

**Steps:**
```bash
# Import from backup
python securevault.py import vault_backup.json
```

**Output:**
```
🔓 Vault unlocked
📥 Importing from: vault_backup.json
⚠️  This will merge with existing vault. Continue? (yes/no): yes
✅ Imported 5 services
💡 Duplicates were skipped (existing services kept)
```

**What You Learned:**
- Import merges with existing vault
- Duplicates are handled (existing kept)
- Useful for migrating between machines

---

## Example 9: Python API Usage

**Scenario:** Use SecureVault programmatically in Python scripts.

**Code:**
```python
#!/usr/bin/env python3
"""Example: Using SecureVault Python API"""

from securevault import SecureVault
import os

# Initialize vault
vault = SecureVault()

# Get master password (from environment for automation)
master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
if not master_pass:
    from getpass import getpass
    master_pass = getpass("Master password: ")

# Unlock vault
if vault.unlock(master_pass):
    print("[OK] Vault unlocked")
    
    # Get a credential
    creds = vault.get_password("openai_api")
    if creds:
        print(f"Username: {creds['username']}")
        # Use creds['password'] in your API call
        
    # List all services
    services = vault.list_services()
    print(f"Total services: {len(services)}")
    
    # Generate password
    new_pass = vault.generate_password(length=24)
    print(f"Generated: {new_pass}")
    
else:
    print("[X] Unlock failed")
```

**Output:**
```
[OK] Vault unlocked
Username: api_key
Total services: 5
Generated: X9m#kP2$wQ7@nL4!rT8^yU5*
```

**What You Learned:**
- Import and initialize vault
- Use environment variable for automation
- Access all vault functions programmatically

---

## Example 10: Automation Script

**Scenario:** Create a script that uses SecureVault in CI/CD pipeline.

**Script: deploy.sh**
```bash
#!/bin/bash
# Deployment script using SecureVault credentials

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Ensure master password is set (from CI secrets)
if [ -z "$VAULT_MASTER_PASSWORD" ]; then
    echo "❌ VAULT_MASTER_PASSWORD not set"
    exit 1
fi

# Get deployment credentials
echo "🔐 Retrieving credentials..."
DEPLOY_KEY=$(python securevault.py get deploy_key << EOF
$VAULT_MASTER_PASSWORD
EOF
)

# Extract password from output (simple parsing)
API_KEY=$(echo "$DEPLOY_KEY" | grep "Password:" | cut -d: -f2 | tr -d ' ')

# Use in deployment
echo "📦 Deploying with retrieved credentials..."
curl -H "Authorization: Bearer $API_KEY" \
     -X POST \
     https://api.example.com/deploy

echo "✅ Deployment complete!"
```

**Usage:**
```bash
# Set secret in CI environment
export VAULT_MASTER_PASSWORD="$CI_SECRET_VAULT_PASS"

# Run deployment
./deploy.sh
```

**Output:**
```
🚀 Starting deployment...
🔐 Retrieving credentials...
📦 Deploying with retrieved credentials...
✅ Deployment complete!
```

**What You Learned:**
- Use SecureVault in CI/CD pipelines
- Pass master password via environment variable
- Never hardcode credentials in scripts

---

## 📝 Tips and Best Practices

1. **Master Password:** Use 16+ characters with mixed case, numbers, symbols
2. **Service Names:** Use descriptive names (e.g., `prod_database`, `dev_aws`)
3. **Regular Backups:** Export backup monthly and store securely
4. **Credential Rotation:** Update passwords periodically
5. **Clean Up:** Delete old/unused credentials regularly

---

## 🚨 Security Reminders

- **NEVER** share your master password
- **NEVER** store master password in scripts
- **NEVER** commit vault file to git
- **DO** use environment variables for automation
- **DO** use strong, unique master password
- **DO** backup your vault regularly

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
