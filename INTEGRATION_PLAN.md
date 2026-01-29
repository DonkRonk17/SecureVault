# SecureVault - Integration Plan

## 🎯 INTEGRATION GOALS

This document outlines how SecureVault integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - future integration
4. Logan's workflows

---

## 📦 OVERVIEW

**SecureVault** is a local encrypted password manager with AES-256 encryption. It provides secure credential storage without cloud dependencies, perfect for:
- API key management
- Service credentials
- Development secrets
- Personal passwords

**Key Differentiators:**
- Zero cloud exposure - all data stored locally
- Military-grade AES-256-CBC encryption
- PBKDF2 key derivation (100,000 iterations)
- Cross-platform Python implementation
- CLI-first design for automation

---

## 📦 BCH INTEGRATION

### Current Status
Not currently integrated with BCH. SecureVault operates as a standalone credential manager.

### Future Integration Potential

**BCH Commands (Proposed):**
```
@securevault get <service>     # Retrieve credentials
@securevault list              # List stored services
@securevault generate          # Generate secure password
```

**Security Considerations:**
- Master password would need secure handling in BCH context
- Consider session-based unlocking (unlock once per session)
- Never transmit passwords over WebSocket - use clipboard or secure display

### Implementation Steps (Future)
1. Create BCH SecureVault adapter
2. Implement secure unlock mechanism
3. Add clipboard integration for password retrieval
4. Create secure session timeout
5. Test thoroughly before deployment

---

## 🤖 AI AGENT INTEGRATION

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | API key management, service credentials | CLI / Python API | HIGH |
| **Atlas** | Development secrets, test credentials | CLI / Python API | HIGH |
| **Clio** | SSH keys, server passwords, Linux creds | CLI | HIGH |
| **Nexus** | Cross-platform credential sync | CLI / Python API | MEDIUM |
| **Bolt** | Automation secrets, CI/CD credentials | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Managing API keys and service credentials for Team Brain coordination.

**Integration Steps:**
1. Store API keys (OpenAI, Anthropic, etc.) in SecureVault
2. Retrieve credentials before API calls
3. Use for SynapseLink authentication (if implemented)

**Example Workflow:**
```python
from securevault import SecureVault
import os

# Initialize vault access
vault = SecureVault()

# For automation, use environment variable for master password
# NEVER hardcode master password!
master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
if not master_pass:
    print("Set VAULT_MASTER_PASSWORD environment variable")
    exit(1)

# Unlock and retrieve
if vault.unlock(master_pass):
    openai_key = vault.get_password("openai")
    if openai_key:
        # Use the API key
        client = OpenAI(api_key=openai_key['password'])
```

**Best Practices for Forge:**
- Store all API keys in vault
- Never log or display credentials
- Use session-based unlocking
- Rotate credentials periodically

#### Atlas (Executor / Builder)

**Primary Use Case:** Managing development secrets and test credentials during tool creation.

**Integration Steps:**
1. Store development database credentials
2. Manage test API keys
3. Keep GitHub tokens secure

**Example Workflow:**
```python
from securevault import SecureVault

vault = SecureVault()

# During development - use test credentials
def get_test_db_connection():
    """Get test database credentials from vault."""
    vault.unlock_from_env()  # Uses VAULT_MASTER_PASSWORD
    
    creds = vault.get_password("test_database")
    if creds:
        return {
            'host': 'localhost',
            'user': creds['username'],
            'password': creds['password'],
            'database': 'test_db'
        }
    return None

# Use in tool development
db_config = get_test_db_connection()
if db_config:
    connection = create_connection(**db_config)
```

**Best Practices for Atlas:**
- Use separate vaults for dev/test/prod
- Store credentials during project setup
- Include credential retrieval in test fixtures
- Never commit credentials to git

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Managing SSH keys, server passwords, and Linux service credentials.

**Platform Considerations:**
- Vault stored at `~/.securevault.enc`
- CLI works natively in bash/zsh
- Can integrate with shell scripts

**Example:**
```bash
# Store SSH password
python securevault.py add ssh_prod_server
# Prompts for master password, then username/password

# Retrieve in script (master password in env)
export VAULT_MASTER_PASSWORD="your_master_pass"
python securevault.py get ssh_prod_server

# Generate secure password
python securevault.py generate --length 24 --symbols
```

**Linux Integration Scripts:**
```bash
#!/bin/bash
# vault_get.sh - Wrapper for secure credential retrieval

SERVICE="$1"
if [ -z "$SERVICE" ]; then
    echo "Usage: vault_get.sh <service_name>"
    exit 1
fi

# Read master password securely
read -s -p "Master Password: " MASTER_PASS
echo

# Get credential (output to clipboard if xclip available)
python3 ~/AutoProjects/SecureVault/securevault.py get "$SERVICE" << EOF
$MASTER_PASS
EOF
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Cross-platform credential access with consistent interface.

**Cross-Platform Notes:**
- Vault file location is user home directory on all platforms
- Windows: `C:\Users\<name>\.securevault.enc`
- Linux/Mac: `/home/<name>/.securevault.enc`
- Same encryption format across platforms

**Example:**
```python
from securevault import SecureVault
import platform

vault = SecureVault()

# Platform detection for any platform-specific handling
current_os = platform.system()
print(f"SecureVault running on {current_os}")

# Vault operations work identically across platforms
vault.unlock(master_password)
creds = vault.get_password("cross_platform_service")
```

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Automation secrets and CI/CD credential management.

**Cost Considerations:**
- SecureVault is free (no API calls)
- Local encryption = no cloud costs
- Perfect for frequent automation runs

**Example:**
```bash
# In automation scripts
export VAULT_MASTER_PASSWORD="${CI_VAULT_PASSWORD}"

# Retrieve secrets for deployment
API_KEY=$(python securevault.py get deploy_api --field password)
DATABASE_URL=$(python securevault.py get prod_db --field password)

# Use in deployment
curl -H "Authorization: Bearer $API_KEY" ...
```

---

## 🔗 INTEGRATION WITH OTHER TEAM BRAIN TOOLS

### With AgentHealth

**Correlation Use Case:** Track credential usage patterns and detect anomalies.

**Integration Pattern:**
```python
from agenthealth import AgentHealth
from securevault import SecureVault

health = AgentHealth()
vault = SecureVault()

# Log credential access
session_id = health.start_session("ATLAS", task="credential_access")

try:
    vault.unlock(master_password)
    creds = vault.get_password("api_service")
    
    # Log success
    health.heartbeat("ATLAS", status="credentials_retrieved")
    
except Exception as e:
    health.log_error("ATLAS", f"Credential access failed: {e}")
    
finally:
    health.end_session("ATLAS", session_id=session_id)
```

### With SynapseLink

**Notification Use Case:** Alert team when credentials are accessed or modified.

**Integration Pattern:**
```python
from synapselink import quick_send
from securevault import SecureVault

vault = SecureVault()

# After credential modification
vault.unlock(master_password)
vault.add_password("new_service", "user@example.com", "generated_pass")

# Notify team (without exposing credentials!)
quick_send(
    "FORGE",
    "Credential Added: new_service",
    "A new credential has been added to SecureVault.\n"
    "Service: new_service\n"
    "Action: Added\n"
    "Agent: ATLAS",
    priority="NORMAL"
)
```

### With ConfigManager

**Configuration Use Case:** Store vault settings in ConfigManager.

**Integration Pattern:**
```python
from configmanager import ConfigManager
from securevault import SecureVault

config = ConfigManager()

# Load SecureVault settings
vault_settings = config.get("securevault", {
    "vault_location": "~/.securevault.enc",
    "password_defaults": {
        "length": 24,
        "use_symbols": True
    },
    "auto_lock_timeout": 300  # 5 minutes
})

# Initialize vault with config
vault = SecureVault(
    vault_path=vault_settings["vault_location"]
)
```

### With MemoryBridge

**Context Persistence Use Case:** Remember vault state across sessions.

**Integration Pattern:**
```python
from memorybridge import MemoryBridge
from securevault import SecureVault

memory = MemoryBridge()

# Store vault metadata (NOT credentials!)
memory.set("securevault_last_access", {
    "timestamp": "2026-01-28T12:00:00Z",
    "services_count": 15,
    "last_modified_service": "api_openai"
})

memory.sync()
```

### With SessionReplay

**Debugging Use Case:** Audit credential access patterns.

**Integration Pattern:**
```python
from sessionreplay import SessionReplay
from securevault import SecureVault

replay = SessionReplay()
vault = SecureVault()

session_id = replay.start_session("ATLAS", task="credential_management")

# Log operations (NOT actual credentials)
replay.log_input(session_id, "Accessing service: api_openai")

try:
    vault.unlock(master_password)
    result = vault.get_password("api_openai")
    
    # Log success without exposing credential
    replay.log_output(session_id, "Credential retrieved successfully")
    replay.end_session(session_id, status="COMPLETED")
    
except Exception as e:
    replay.log_error(session_id, f"Access failed: {e}")
    replay.end_session(session_id, status="FAILED")
```

### With ErrorRecovery

**Error Recovery Use Case:** Handle vault errors gracefully.

**Integration Pattern:**
```python
from errorrecovery import ErrorRecovery
from securevault import SecureVault

recovery = ErrorRecovery()
vault = SecureVault()

try:
    vault.unlock(master_password)
    creds = vault.get_password("service")
    
except FileNotFoundError:
    # Vault doesn't exist
    recovery.log_error(
        "vault_not_found",
        "SecureVault file not found",
        recovery_action="Create new vault with: python securevault.py init"
    )
    
except ValueError as e:
    # Wrong password
    recovery.log_error(
        "vault_auth_failed",
        str(e),
        recovery_action="Verify master password is correct"
    )
```

### With TokenTracker

**Usage Tracking Use Case:** Monitor vault operations for billing/audit.

**Integration Pattern:**
```python
from tokentracker import TokenTracker
from securevault import SecureVault

tracker = TokenTracker()
vault = SecureVault()

# SecureVault operations don't use API tokens, but tracking is useful
tracker.log_local_operation(
    tool="SecureVault",
    operation="get_password",
    service="api_openai"
)
```

---

## 🚀 ADOPTION ROADMAP

### Phase 1: Core Adoption (Week 1)
**Goal:** All agents aware and can use basic features

**Steps:**
1. ✓ Tool deployed to GitHub
2. ☐ Quick-start guides sent via Synapse
3. ☐ Each agent tests init/add/get workflow
4. ☐ Feedback collected

**Success Criteria:**
- All 5 agents have created test vaults
- No blocking issues reported
- Basic workflow documented

### Phase 2: Integration (Week 2-3)
**Goal:** Integrated into daily workflows

**Steps:**
1. ☐ Add to agent startup routines (credential check)
2. ☐ Create integration examples with existing tools
3. ☐ Migrate API keys from plaintext configs
4. ☐ Monitor usage patterns

**Success Criteria:**
- All API keys stored in SecureVault
- No plaintext credentials in code/configs
- Daily usage by all agents

### Phase 3: Optimization (Week 4+)
**Goal:** Optimized and fully adopted

**Steps:**
1. ☐ Implement session-based unlocking
2. ☐ Add clipboard integration
3. ☐ Create BCH adapter (if needed)
4. ☐ Security audit

**Success Criteria:**
- Zero credential exposure incidents
- Positive feedback from all agents
- v1.1 improvements identified

---

## 📊 SUCCESS METRICS

**Security Metrics:**
- Credential exposure incidents: 0 (target)
- Plaintext credentials in codebase: 0 (target)
- Failed access attempts logged: Track

**Adoption Metrics:**
- Number of agents using tool: 5/5 (target)
- Services stored in vault: Track
- Daily access count: Track

**Efficiency Metrics:**
- Time to retrieve credential: < 5 seconds
- Vault unlock time: < 2 seconds
- Password generation time: < 1 second

---

## 🛠️ TECHNICAL INTEGRATION DETAILS

### Import Paths
```python
# Main import
from securevault import SecureVault

# Specific functions
from securevault import generate_password
```

### Environment Variables
```bash
# Master password (for automation ONLY)
export VAULT_MASTER_PASSWORD="your_secure_master_password"

# Custom vault location (optional)
export SECUREVAULT_PATH="~/.my_vault.enc"
```

### Error Handling
**Standardized Error Codes:**
- 0: Success
- 1: General error / wrong password
- 2: Vault not found
- 3: Service not found
- 4: Encryption error

### Security Best Practices

**DO:**
- Use strong master passwords (16+ characters)
- Store master password in secure location (not in code)
- Use environment variables for automation
- Rotate credentials periodically
- Backup vault file securely

**DON'T:**
- Hardcode master password
- Share vault file via insecure channels
- Log credentials
- Store vault in version control
- Use weak master passwords

---

## 🔧 MAINTENANCE & SUPPORT

### Update Strategy
- Minor updates (v1.x): As needed
- Security patches: Immediate
- Major updates (v2.0+): With migration guide

### Support Channels
- GitHub Issues: Bug reports
- Synapse: Team Brain discussions
- Direct to Builder: Security issues (private)

### Known Limitations
- Single vault file (no multi-vault support yet)
- No browser extension
- CLI only (no GUI)
- Requires master password for each operation

### Planned Improvements
- Session-based unlocking (unlock once, use multiple times)
- Clipboard auto-clear
- Multi-vault support
- Import from other password managers

---

## 📚 ADDITIONAL RESOURCES

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- Integration Examples: [INTEGRATION_EXAMPLES.md](INTEGRATION_EXAMPLES.md)
- GitHub: https://github.com/DonkRonk17/SecureVault

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
