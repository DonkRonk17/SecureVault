# SecureVault - Integration Examples

## 🎯 INTEGRATION PHILOSOPHY

SecureVault is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

**Security Note:** These examples demonstrate integration patterns. Never log or expose actual credentials!

---

## 📚 TABLE OF CONTENTS

1. [Pattern 1: SecureVault + AgentHealth](#pattern-1-securevault--agenthealth)
2. [Pattern 2: SecureVault + SynapseLink](#pattern-2-securevault--synapselink)
3. [Pattern 3: SecureVault + ConfigManager](#pattern-3-securevault--configmanager)
4. [Pattern 4: SecureVault + MemoryBridge](#pattern-4-securevault--memorybridge)
5. [Pattern 5: SecureVault + SessionReplay](#pattern-5-securevault--sessionreplay)
6. [Pattern 6: SecureVault + ErrorRecovery](#pattern-6-securevault--errorrecovery)
7. [Pattern 7: SecureVault + TokenTracker](#pattern-7-securevault--tokentracker)
8. [Pattern 8: SecureVault + TaskQueuePro](#pattern-8-securevault--taskqueuepro)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: SecureVault + AgentHealth

**Use Case:** Monitor credential access health and detect anomalies

**Why:** Track when and how often credentials are accessed for security auditing

**Code:**

```python
from agenthealth import AgentHealth
from securevault import SecureVault
import os

# Initialize both tools
health = AgentHealth()
vault = SecureVault()

# Start health monitoring session
session_id = health.start_session("ATLAS", task="credential_access")

try:
    # Get master password from secure source
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    if vault.unlock(master_pass):
        # Log successful unlock
        health.heartbeat("ATLAS", status="vault_unlocked")
        
        # Retrieve credential
        creds = vault.get_password("api_service")
        
        if creds:
            # Log success (without exposing credential!)
            health.heartbeat("ATLAS", status="credential_retrieved")
            print("[OK] Credential retrieved successfully")
        else:
            health.log_error("ATLAS", "Service not found in vault")
    else:
        health.log_error("ATLAS", "Vault unlock failed")
        
except Exception as e:
    health.log_error("ATLAS", f"Vault access error: {type(e).__name__}")
    
finally:
    health.end_session("ATLAS", session_id=session_id)
```

**Result:** Health monitoring tracks credential access patterns for security auditing

---

## Pattern 2: SecureVault + SynapseLink

**Use Case:** Notify team when credentials are modified

**Why:** Keep team informed of security-sensitive changes

**Code:**

```python
from synapselink import quick_send
from securevault import SecureVault
import os

vault = SecureVault()

def add_credential_with_notification(service_name, username, password):
    """Add credential and notify team."""
    
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    if vault.unlock(master_pass):
        # Add the credential
        vault.add_password(service_name, username, password)
        
        # Notify team (WITHOUT exposing the credential!)
        quick_send(
            "FORGE",
            f"[SecureVault] Credential Added: {service_name}",
            f"A new credential has been added to SecureVault.\n\n"
            f"**Service:** {service_name}\n"
            f"**Action:** Added\n"
            f"**Agent:** {os.environ.get('AGENT_NAME', 'UNKNOWN')}\n"
            f"**Time:** {datetime.now().isoformat()}\n\n"
            f"Review if unexpected.",
            priority="NORMAL"
        )
        
        return True
    return False

# Usage
add_credential_with_notification(
    "new_api_service",
    "api_key",
    "sk-generated-api-key"
)
```

**Result:** Team stays informed of credential changes without credential exposure

---

## Pattern 3: SecureVault + ConfigManager

**Use Case:** Centralize vault configuration settings

**Why:** Consistent vault settings across all Team Brain agents

**Code:**

```python
from configmanager import ConfigManager
from securevault import SecureVault
from pathlib import Path

config = ConfigManager()

# Load SecureVault settings from central config
vault_config = config.get("securevault", {
    "vault_location": str(Path.home() / ".securevault.enc"),
    "password_defaults": {
        "length": 24,
        "use_symbols": True,
        "use_numbers": True
    },
    "auto_lock_timeout": 300,  # 5 minutes
    "backup_enabled": True,
    "backup_location": str(Path.home() / ".securevault_backup")
})

# Initialize vault with config
vault = SecureVault(vault_path=vault_config["vault_location"])

# Use configured password defaults
def generate_password():
    """Generate password using configured defaults."""
    defaults = vault_config["password_defaults"]
    return vault.generate_password(
        length=defaults["length"],
        symbols=defaults["use_symbols"]
    )

# Save updated config if needed
config.set("securevault.last_access", datetime.now().isoformat())
config.save()
```

**Result:** Centralized, consistent vault configuration

---

## Pattern 4: SecureVault + MemoryBridge

**Use Case:** Persist vault metadata across sessions

**Why:** Remember vault state without storing sensitive data

**Code:**

```python
from memorybridge import MemoryBridge
from securevault import SecureVault
from datetime import datetime

memory = MemoryBridge()
vault = SecureVault()

def access_credential_with_memory(service_name, master_pass):
    """Access credential and update memory metadata."""
    
    # Load access history from memory
    access_log = memory.get("securevault_access_log", [])
    
    if vault.unlock(master_pass):
        creds = vault.get_password(service_name)
        
        if creds:
            # Update access log (NO credentials stored!)
            access_log.append({
                "service": service_name,
                "timestamp": datetime.now().isoformat(),
                "success": True
            })
            
            # Keep only last 100 entries
            access_log = access_log[-100:]
            memory.set("securevault_access_log", access_log)
            
            # Update last access metadata
            memory.set("securevault_last_access", {
                "service": service_name,
                "timestamp": datetime.now().isoformat()
            })
            
            memory.sync()
            return creds
    
    return None

# Usage
creds = access_credential_with_memory("api_openai", master_password)
```

**Result:** Vault access history persisted for auditing

---

## Pattern 5: SecureVault + SessionReplay

**Use Case:** Audit trail for credential operations

**Why:** Debug credential access issues and review security events

**Code:**

```python
from sessionreplay import SessionReplay
from securevault import SecureVault
import os

replay = SessionReplay()
vault = SecureVault()

def secure_operation_with_replay(operation, service_name):
    """Perform vault operation with full replay logging."""
    
    session_id = replay.start_session(
        "ATLAS",
        task=f"SecureVault:{operation}:{service_name}"
    )
    
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    try:
        # Log operation start (no sensitive data!)
        replay.log_input(session_id, f"Operation: {operation}")
        replay.log_input(session_id, f"Service: {service_name}")
        
        if vault.unlock(master_pass):
            replay.log_output(session_id, "Vault unlocked successfully")
            
            if operation == "get":
                result = vault.get_password(service_name)
                if result:
                    # Log success without credential
                    replay.log_output(session_id, 
                        f"Credential retrieved for {service_name}")
                    replay.end_session(session_id, status="COMPLETED")
                    return result
                else:
                    replay.log_error(session_id, "Service not found")
                    
            elif operation == "list":
                services = vault.list_services()
                replay.log_output(session_id, 
                    f"Listed {len(services)} services")
                replay.end_session(session_id, status="COMPLETED")
                return services
        else:
            replay.log_error(session_id, "Vault unlock failed")
            
    except Exception as e:
        replay.log_error(session_id, f"Error: {type(e).__name__}")
        
    replay.end_session(session_id, status="FAILED")
    return None

# Usage
creds = secure_operation_with_replay("get", "api_openai")
```

**Result:** Full audit trail for security review

---

## Pattern 6: SecureVault + ErrorRecovery

**Use Case:** Graceful error handling for vault operations

**Why:** Provide actionable recovery steps when errors occur

**Code:**

```python
from errorrecovery import ErrorRecovery
from securevault import SecureVault
import os

recovery = ErrorRecovery()
vault = SecureVault()

def safe_vault_access(service_name):
    """Access vault with comprehensive error handling."""
    
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    try:
        # Check vault exists
        if not vault.vault_exists():
            recovery.log_error(
                error_type="vault_not_found",
                message="SecureVault file not found",
                recovery_action="Create vault: python securevault.py init",
                severity="HIGH"
            )
            return None
            
        # Try unlock
        if not vault.unlock(master_pass):
            recovery.log_error(
                error_type="vault_auth_failed",
                message="Invalid master password",
                recovery_action="Verify VAULT_MASTER_PASSWORD is correct",
                severity="HIGH"
            )
            return None
            
        # Try get credential
        creds = vault.get_password(service_name)
        if not creds:
            recovery.log_error(
                error_type="service_not_found",
                message=f"Service '{service_name}' not in vault",
                recovery_action=f"Add: python securevault.py add {service_name}",
                severity="MEDIUM"
            )
            return None
            
        return creds
        
    except ImportError as e:
        recovery.log_error(
            error_type="dependency_missing",
            message="cryptography package not installed",
            recovery_action="pip install cryptography",
            severity="HIGH"
        )
        
    except PermissionError as e:
        recovery.log_error(
            error_type="permission_denied",
            message="Cannot access vault file",
            recovery_action="Check file permissions: chmod 600 ~/.securevault.enc",
            severity="HIGH"
        )
        
    except Exception as e:
        recovery.log_error(
            error_type="unknown_vault_error",
            message=str(e),
            recovery_action="Check logs and retry",
            severity="MEDIUM"
        )
    
    return None

# Usage
creds = safe_vault_access("api_openai")
if creds:
    print("[OK] Credential retrieved")
else:
    print("[X] Failed - check ErrorRecovery logs")
```

**Result:** Actionable error messages with recovery steps

---

## Pattern 7: SecureVault + TokenTracker

**Use Case:** Track vault operations for usage analytics

**Why:** Monitor security tool usage patterns

**Code:**

```python
from tokentracker import TokenTracker
from securevault import SecureVault
from datetime import datetime

tracker = TokenTracker()
vault = SecureVault()

def tracked_vault_operation(operation, service_name, master_pass):
    """Perform vault operation with usage tracking."""
    
    # Track operation (SecureVault is local, no tokens used)
    tracker.log_local_operation(
        tool="SecureVault",
        operation=operation,
        metadata={
            "service": service_name,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    if vault.unlock(master_pass):
        if operation == "get":
            result = vault.get_password(service_name)
            tracker.log_operation_complete(
                tool="SecureVault",
                success=result is not None
            )
            return result
            
        elif operation == "list":
            result = vault.list_services()
            tracker.log_operation_complete(
                tool="SecureVault",
                success=True,
                count=len(result)
            )
            return result
            
        elif operation == "generate":
            result = vault.generate_password()
            tracker.log_operation_complete(
                tool="SecureVault",
                success=True
            )
            return result
    
    return None

# Usage
creds = tracked_vault_operation("get", "api_openai", master_password)
```

**Result:** Vault usage tracked alongside API usage

---

## Pattern 8: SecureVault + TaskQueuePro

**Use Case:** Queue credential-dependent tasks

**Why:** Ensure credentials are available before task execution

**Code:**

```python
from taskqueuepro import TaskQueuePro
from securevault import SecureVault
import os

queue = TaskQueuePro()
vault = SecureVault()

def queue_task_with_credentials(task_name, required_service):
    """Queue task only if required credentials exist."""
    
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    # Verify credential exists before queueing
    if vault.unlock(master_pass):
        creds = vault.get_password(required_service)
        
        if creds:
            # Credential exists - queue the task
            task_id = queue.create_task(
                title=task_name,
                agent="ATLAS",
                priority=2,
                metadata={
                    "required_credential": required_service,
                    "credential_verified": True
                }
            )
            print(f"[OK] Task queued: {task_id}")
            return task_id
        else:
            print(f"[X] Cannot queue: credential '{required_service}' not found")
            return None
    else:
        print("[X] Cannot queue: vault access failed")
        return None

# Usage
task_id = queue_task_with_credentials(
    "Deploy to production",
    "prod_deploy_key"
)
```

**Result:** Tasks only queued when credentials are available

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete credential-dependent workflow

**Why:** Demonstrate real production scenario

**Code:**

```python
from taskqueuepro import TaskQueuePro
from sessionreplay import SessionReplay
from agenthealth import AgentHealth
from synapselink import quick_send
from securevault import SecureVault
import os

# Initialize all tools
queue = TaskQueuePro()
replay = SessionReplay()
health = AgentHealth()
vault = SecureVault()

def complete_secure_workflow(task_name, required_service):
    """Full workflow with credential access and monitoring."""
    
    # Start tracking
    task_id = queue.create_task(task_name, agent="ATLAS")
    session_id = replay.start_session("ATLAS", task=task_name)
    health.start_session("ATLAS", session_id=session_id)
    
    master_pass = os.environ.get('VAULT_MASTER_PASSWORD')
    
    try:
        # Mark task in progress
        queue.start_task(task_id)
        replay.log_input(session_id, f"Starting: {task_name}")
        health.heartbeat("ATLAS", status="starting")
        
        # Access credential
        if vault.unlock(master_pass):
            replay.log_output(session_id, "Vault unlocked")
            
            creds = vault.get_password(required_service)
            if creds:
                replay.log_output(session_id, "Credentials retrieved")
                health.heartbeat("ATLAS", status="credentials_ready")
                
                # Perform task with credentials
                # ... your task logic here ...
                result = do_task_with_credentials(creds)
                
                # Success
                queue.complete_task(task_id, result="success")
                replay.log_output(session_id, "Task completed")
                replay.end_session(session_id, status="COMPLETED")
                health.end_session("ATLAS", session_id=session_id, status="success")
                
                quick_send("TEAM", f"Task Complete: {task_name}", "Success!")
                return True
        
        # Failure path
        queue.fail_task(task_id, error="Credential access failed")
        replay.end_session(session_id, status="FAILED")
        health.end_session("ATLAS", session_id=session_id, status="failed")
        
        quick_send("FORGE", f"Task Failed: {task_name}", 
                   "Credential access failed", priority="HIGH")
        return False
        
    except Exception as e:
        queue.fail_task(task_id, error=str(e))
        replay.log_error(session_id, str(e))
        health.log_error("ATLAS", str(e))
        return False
```

**Result:** Fully instrumented, secure workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade secure operations

**Code:**

See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) for complete architecture example.

**Quick Summary:**
```python
# Full stack initialization
from securevault import SecureVault
from agenthealth import AgentHealth
from sessionreplay import SessionReplay
from synapselink import quick_send
from configmanager import ConfigManager
from errorrecovery import ErrorRecovery
from tokentracker import TokenTracker

# Initialize all
vault = SecureVault()
health = AgentHealth()
replay = SessionReplay()
config = ConfigManager()
recovery = ErrorRecovery()
tracker = TokenTracker()

# Use together for:
# - Secure credential access
# - Health monitoring
# - Audit trails
# - Error recovery
# - Usage tracking
# - Team notifications
```

---

## 📊 RECOMMENDED INTEGRATION PRIORITY

**Week 1 (Essential):**
1. ✓ ErrorRecovery - Handle vault errors gracefully
2. ✓ SessionReplay - Audit trail for security
3. ✓ SynapseLink - Notify on changes

**Week 2 (Productivity):**
4. ☐ AgentHealth - Monitor access patterns
5. ☐ ConfigManager - Centralize settings
6. ☐ MemoryBridge - Persist metadata

**Week 3 (Advanced):**
7. ☐ TokenTracker - Usage analytics
8. ☐ TaskQueuePro - Credential-dependent tasks
9. ☐ Full stack integration

---

## 🔧 TROUBLESHOOTING INTEGRATIONS

**Import Errors:**
```python
# Ensure all tools are in Python path
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from securevault import SecureVault
```

**Master Password Issues:**
```bash
# Set environment variable
export VAULT_MASTER_PASSWORD="your_password"

# Verify it's set
echo $VAULT_MASTER_PASSWORD
```

**Vault Not Found:**
```bash
# Check vault exists
ls -la ~/.securevault.enc

# Create if missing
python securevault.py init
```

---

**Last Updated:** January 28, 2026  
**Maintained By:** FORGE (Team Brain)
