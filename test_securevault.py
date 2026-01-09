"""
SecureVault - Automated Test Script
Tests all functionality without user interaction
"""

import os
import sys
import io
import subprocess
import tempfile
from pathlib import Path

# Fix Unicode output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Use temporary vault file for testing
test_vault = Path(tempfile.gettempdir()) / "test_securevault.enc"
os.environ['HOME'] = tempfile.gettempdir()  # Redirect vault location

print("🧪 SECUREVAULT AUTOMATED TESTING\n")
print("="*60)

# Test master password
MASTER_PASSWORD = "TestMasterPass123!"

def run_command(cmd, input_text=""):
    """Run securevault command with input"""
    try:
        result = subprocess.run(
            f"python securevault.py {cmd}",
            shell=True,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -1, "", str(e)

# Clean up old test vault
if test_vault.exists():
    test_vault.unlink()

# TEST 1: Initialize vault
print("\n[TEST 1] Creating vault...")
returncode, stdout, stderr = run_command(
    "init",
    f"{MASTER_PASSWORD}\n{MASTER_PASSWORD}\n"
)
if returncode == 0 and test_vault.exists():
    print("✅ PASS: Vault created successfully")
else:
    print(f"❌ FAIL: Vault creation failed")
    print(f"   Return code: {returncode}")
    print(f"   stderr: {stderr}")
    sys.exit(1)

# TEST 2: Add password
print("\n[TEST 2] Adding password...")
returncode, stdout, stderr = run_command(
    "add testservice",
    f"{MASTER_PASSWORD}\ntestuser\ntestpass123\n"
)
if returncode == 0:
    print("✅ PASS: Password added")
else:
    print(f"❌ FAIL: Failed to add password")
    print(f"   Return code: {returncode}")
    print(f"   stderr: {stderr}")
    sys.exit(1)

# TEST 3: List passwords
print("\n[TEST 3] Listing passwords...")
returncode, stdout, stderr = run_command(
    "list",
    f"{MASTER_PASSWORD}\n"
)
if returncode == 0 and "testservice" in stdout:
    print("✅ PASS: Service listed correctly")
else:
    print(f"❌ FAIL: List failed or service not found")
    print(f"   Return code: {returncode}")
    print(f"   Output: {stdout}")
    sys.exit(1)

# TEST 4: Retrieve password
print("\n[TEST 4] Retrieving password...")
returncode, stdout, stderr = run_command(
    "get testservice",
    f"{MASTER_PASSWORD}\n"
)
if returncode == 0 and "testuser" in stdout and "testpass123" in stdout:
    print("✅ PASS: Password retrieved correctly")
else:
    print(f"❌ FAIL: Failed to retrieve password")
    print(f"   Return code: {returncode}")
    print(f"   Output: {stdout}")
    sys.exit(1)

# TEST 5: Generate password
print("\n[TEST 5] Generating password...")
returncode, stdout, stderr = run_command(
    "generate --length 16",
    f"{MASTER_PASSWORD}\n"
)
if returncode == 0 and "Generated password:" in stdout:
    print("✅ PASS: Password generated")
else:
    print(f"❌ FAIL: Failed to generate password")
    print(f"   Return code: {returncode}")
    print(f"   Output: {stdout}")
    sys.exit(1)

# TEST 6: Delete password
print("\n[TEST 6] Deleting password...")
returncode, stdout, stderr = run_command(
    "delete testservice",
    f"{MASTER_PASSWORD}\nyes\n"
)
if returncode == 0:
    print("✅ PASS: Password deleted")
else:
    print(f"❌ FAIL: Failed to delete password")
    print(f"   Return code: {returncode}")
    print(f"   stderr: {stderr}")
    sys.exit(1)

# TEST 7: Verify deletion
print("\n[TEST 7] Verifying deletion...")
returncode, stdout, stderr = run_command(
    "list",
    f"{MASTER_PASSWORD}\n"
)
if returncode == 0 and "empty" in stdout.lower():
    print("✅ PASS: Vault is empty after deletion")
else:
    print(f"❌ FAIL: Vault should be empty")
    print(f"   Output: {stdout}")
    sys.exit(1)

# TEST 8: Wrong password handling
print("\n[TEST 8] Testing wrong password...")
returncode, stdout, stderr = run_command(
    "list",
    "WrongPassword123\n"
)
if returncode != 0 or "Invalid master password" in stdout:
    print("✅ PASS: Wrong password rejected")
else:
    print(f"❌ FAIL: Should reject wrong password")
    sys.exit(1)

# Clean up
if test_vault.exists():
    test_vault.unlink()

print("\n" + "="*60)
print("🎉 ALL TESTS PASSED!")
print("="*60)
print("\n✅ SecureVault is working correctly!\n")
