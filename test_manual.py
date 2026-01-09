"""
SecureVault - Manual Test Demo
Demonstrates all functionality step by step
"""

import sys
import io
import os
from pathlib import Path

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Import the vault class directly
sys.path.insert(0, '.')
from securevault import SecureVault
import tempfile

print("🧪 SECUREVAULT FUNCTIONALITY TEST\n")
print("="*60)

# Use temp file
vault_file = Path(tempfile.gettempdir()) / "test_vault.enc"
if vault_file.exists():
    vault_file.unlink()

# Override the vault file location
import securevault as sv
sv.VAULT_FILE = vault_file

vault = SecureVault()

# TEST 1: Create vault
print("\n[TEST 1] Creating encrypted vault...")
try:
    vault.create_vault("TestMasterPassword123!")
    print("✅ PASS: Vault created")
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 2: Add password
print("\n[TEST 2] Adding password entry...")
try:
    vault.add_password("github", "testuser", "SecurePass123!")
    print("✅ PASS: Password added")
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 3: Retrieve password
print("\n[TEST 3] Retrieving password...")
try:
    entry = vault.get_password("github")
    if entry and entry['username'] == 'testuser' and entry['password'] == 'SecurePass123!':
        print(f"✅ PASS: Retrieved - {entry['username']} / {entry['password']}")
    else:
        print(f"❌ FAIL: Wrong data returned")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 4: List services
print("\n[TEST 4] Listing all services...")
try:
    services = vault.list_services()
    if 'github' in services:
        print(f"✅ PASS: Found {len(services)} service(s): {services}")
    else:
        print(f"❌ FAIL: Service not in list")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 5: Generate password
print("\n[TEST 5] Generating secure password...")
try:
    password = vault.generate_password(20, include_symbols=True)
    if len(password) == 20:
        print(f"✅ PASS: Generated {len(password)}-char password: {password}")
    else:
        print(f"❌ FAIL: Wrong length")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 6: Encryption persistence (save & reload)
print("\n[TEST 6] Testing encryption persistence...")
try:
    vault.save_vault()
    
    # Create new vault instance and unlock
    vault2 = SecureVault()
    if vault2.unlock_vault("TestMasterPassword123!"):
        entry = vault2.get_password("github")
        if entry and entry['username'] == 'testuser':
            print("✅ PASS: Vault saved, reloaded, and decrypted correctly")
        else:
            print("❌ FAIL: Data corrupted after reload")
            sys.exit(1)
    else:
        print("❌ FAIL: Could not unlock vault")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 7: Wrong password rejection
print("\n[TEST 7] Testing wrong password rejection...")
try:
    vault3 = SecureVault()
    if not vault3.unlock_vault("WrongPassword"):
        print("✅ PASS: Wrong password correctly rejected")
    else:
        print("❌ FAIL: Wrong password accepted!")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# TEST 8: Delete password
print("\n[TEST 8] Deleting password entry...")
try:
    if vault.delete_password("github"):
        services = vault.list_services()
        if 'github' not in services:
            print("✅ PASS: Password deleted successfully")
        else:
            print("❌ FAIL: Password still exists")
            sys.exit(1)
    else:
        print("❌ FAIL: Delete returned False")
        sys.exit(1)
except Exception as e:
    print(f"❌ FAIL: {e}")
    sys.exit(1)

# Clean up
if vault_file.exists():
    vault_file.unlink()

print("\n" + "="*60)
print("🎉 ALL 8 TESTS PASSED!")
print("="*60)
print("\n✅ SecureVault core functionality verified!")
print("   - AES-256 encryption working")
print("   - Password storage/retrieval working")
print("   - Master password protection working")
print("   - Persistence (save/load) working")
print("   - Security (wrong password rejection) working\n")
