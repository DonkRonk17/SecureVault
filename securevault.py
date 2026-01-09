#!/usr/bin/env python3
"""
SecureVault - Local Encrypted Password Manager
A simple, secure, command-line password manager with AES-256 encryption.
Zero cloud dependencies - all data stored locally.
"""

import os
import sys
import io
import json
import hashlib
import secrets
import string
import getpass
import time
from base64 import b64encode, b64decode
from pathlib import Path

# Fix Unicode output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
except ImportError:
    print("❌ Error: cryptography package required")
    print("Install: pip install cryptography")
    sys.exit(1)

# --- Config ---
VAULT_FILE = Path.home() / ".securevault.enc"
SALT_SIZE = 32
IV_SIZE = 16
KEY_SIZE = 32  # AES-256

class SecureVault:
    """Local encrypted password manager"""
    
    def __init__(self):
        self.master_key = None
        self.vault_data = {}
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from master password using PBKDF2"""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, KEY_SIZE)
    
    def encrypt_data(self, data: str, key: bytes) -> tuple:
        """Encrypt data with AES-256-CBC"""
        # Generate random IV
        iv = os.urandom(IV_SIZE)
        
        # Pad data to block size
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        
        # Encrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        return iv, encrypted
    
    def decrypt_data(self, iv: bytes, encrypted_data: bytes, key: bytes) -> str:
        """Decrypt data with AES-256-CBC"""
        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode()
    
    def create_vault(self, master_password: str):
        """Create new encrypted vault"""
        print("\n🔐 Creating new SecureVault...")
        
        # Generate random salt
        salt = os.urandom(SALT_SIZE)
        
        # Derive key from master password
        key = self.derive_key(master_password, salt)
        
        # Create empty vault
        vault_json = json.dumps({"passwords": {}})
        iv, encrypted = self.encrypt_data(vault_json, key)
        
        # Save vault file
        vault_content = {
            "salt": b64encode(salt).decode(),
            "iv": b64encode(iv).decode(),
            "data": b64encode(encrypted).decode()
        }
        
        with open(VAULT_FILE, 'w') as f:
            json.dump(vault_content, f)
        
        # Set file permissions (owner only)
        if os.name != 'nt':  # Unix/Linux/Mac
            os.chmod(VAULT_FILE, 0o600)
        
        print(f"✅ Vault created: {VAULT_FILE}")
        print("⚠️  IMPORTANT: Remember your master password!")
        print("   There is NO way to recover it if forgotten.\n")
        
        self.master_key = key
        self.vault_data = {"passwords": {}}
    
    def unlock_vault(self, master_password: str) -> bool:
        """Unlock existing vault with master password"""
        if not VAULT_FILE.exists():
            return False
        
        try:
            # Load vault file
            with open(VAULT_FILE, 'r') as f:
                vault_content = json.load(f)
            
            # Extract components
            salt = b64decode(vault_content["salt"])
            iv = b64decode(vault_content["iv"])
            encrypted_data = b64decode(vault_content["data"])
            
            # Derive key and decrypt
            key = self.derive_key(master_password, salt)
            decrypted_json = self.decrypt_data(iv, encrypted_data, key)
            
            # Parse vault data
            self.vault_data = json.loads(decrypted_json)
            self.master_key = key
            
            return True
        
        except Exception as e:
            return False
    
    def save_vault(self):
        """Save vault with current encryption"""
        if not self.master_key:
            print("❌ Error: Vault not unlocked")
            return
        
        # Load salt from existing vault
        with open(VAULT_FILE, 'r') as f:
            vault_content = json.load(f)
        salt = b64decode(vault_content["salt"])
        
        # Encrypt current data
        vault_json = json.dumps(self.vault_data)
        iv, encrypted = self.encrypt_data(vault_json, self.master_key)
        
        # Save
        vault_content = {
            "salt": b64encode(salt).decode(),
            "iv": b64encode(iv).decode(),
            "data": b64encode(encrypted).decode()
        }
        
        with open(VAULT_FILE, 'w') as f:
            json.dump(vault_content, f)
    
    def add_password(self, service: str, username: str, password: str):
        """Add password entry to vault"""
        self.vault_data["passwords"][service] = {
            "username": username,
            "password": password,
            "created": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_vault()
        print(f"✅ Password saved for: {service}")
    
    def get_password(self, service: str) -> dict:
        """Retrieve password entry from vault"""
        return self.vault_data["passwords"].get(service)
    
    def list_services(self) -> list:
        """List all services in vault"""
        return sorted(self.vault_data["passwords"].keys())
    
    def delete_password(self, service: str) -> bool:
        """Delete password entry from vault"""
        if service in self.vault_data["passwords"]:
            del self.vault_data["passwords"][service]
            self.save_vault()
            return True
        return False
    
    def generate_password(self, length: int = 20, include_symbols: bool = True) -> str:
        """Generate cryptographically secure random password"""
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Use secrets module for cryptographically strong randomness
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password


def copy_to_clipboard(text: str):
    """Copy text to clipboard (cross-platform)"""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        # Fallback: just print (user can copy manually)
        return False


def clear_clipboard():
    """Clear clipboard (cross-platform)"""
    try:
        import pyperclip
        pyperclip.copy("")
    except ImportError:
        pass


def print_banner():
    """Print SecureVault banner"""
    print("\n" + "="*60)
    print("🔐 SECUREVAULT - Local Encrypted Password Manager")
    print("="*60 + "\n")


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SecureVault - Local Encrypted Password Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  securevault add github                    # Add new password
  securevault get github                    # Retrieve password
  securevault list                          # List all services
  securevault generate                      # Generate random password
  securevault delete github                 # Delete password entry
        """
    )
    
    parser.add_argument('command', choices=['add', 'get', 'list', 'generate', 'delete', 'init'],
                       help='Command to execute')
    parser.add_argument('service', nargs='?', help='Service name')
    parser.add_argument('--length', type=int, default=20, help='Password length (for generate)')
    parser.add_argument('--no-symbols', action='store_true', help='Exclude symbols from generated password')
    
    args = parser.parse_args()
    
    vault = SecureVault()
    
    # Init command - create new vault
    if args.command == 'init':
        print_banner()
        if VAULT_FILE.exists():
            confirm = input("⚠️  Vault already exists. Overwrite? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Aborted")
                return
        
        password1 = getpass.getpass("Create master password: ")
        password2 = getpass.getpass("Confirm master password: ")
        
        if password1 != password2:
            print("❌ Passwords don't match")
            return
        
        if len(password1) < 8:
            print("❌ Master password must be at least 8 characters")
            return
        
        vault.create_vault(password1)
        return
    
    # All other commands require unlocked vault
    print_banner()
    
    if not VAULT_FILE.exists():
        print("❌ No vault found. Create one with: securevault init")
        return
    
    # Unlock vault
    master_password = getpass.getpass("Enter master password: ")
    
    if not vault.unlock_vault(master_password):
        print("❌ Invalid master password")
        return
    
    print("✅ Vault unlocked\n")
    
    # Execute command
    if args.command == 'add':
        if not args.service:
            print("❌ Error: Service name required")
            print("Usage: securevault add <service>")
            return
        
        # Check if service exists
        existing = vault.get_password(args.service)
        if existing:
            confirm = input(f"⚠️  Password for '{args.service}' already exists. Overwrite? (yes/no): ")
            if confirm.lower() != 'yes':
                print("❌ Aborted")
                return
        
        username = input(f"Username for {args.service}: ")
        password = getpass.getpass(f"Password for {args.service} (leave blank to generate): ")
        
        if not password:
            password = vault.generate_password()
            print(f"\n🔑 Generated password: {password}")
            print("   (Copy this now - it won't be shown again)\n")
            time.sleep(3)
        
        vault.add_password(args.service, username, password)
    
    elif args.command == 'get':
        if not args.service:
            print("❌ Error: Service name required")
            print("Usage: securevault get <service>")
            return
        
        entry = vault.get_password(args.service)
        if not entry:
            print(f"❌ No password found for: {args.service}")
            return
        
        print(f"Service:  {args.service}")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"Created:  {entry['created']}")
        
        # Try to copy to clipboard
        if copy_to_clipboard(entry['password']):
            print("\n✅ Password copied to clipboard (will clear in 15 seconds)")
            time.sleep(15)
            clear_clipboard()
            print("🔒 Clipboard cleared")
        else:
            print("\n💡 Tip: Install 'pyperclip' for auto-clipboard copy")
    
    elif args.command == 'list':
        services = vault.list_services()
        if not services:
            print("📭 Vault is empty")
            return
        
        print(f"📋 Stored passwords ({len(services)}):\n")
        for i, service in enumerate(services, 1):
            entry = vault.get_password(service)
            print(f"  {i}. {service}")
            print(f"     Username: {entry['username']}")
            print(f"     Created:  {entry['created']}\n")
    
    elif args.command == 'generate':
        password = vault.generate_password(args.length, not args.no_symbols)
        print(f"🔑 Generated password: {password}")
        print(f"   Length: {len(password)} characters")
        
        if copy_to_clipboard(password):
            print("\n✅ Password copied to clipboard")
        else:
            print("\n💡 Tip: Install 'pyperclip' for auto-clipboard copy")
    
    elif args.command == 'delete':
        if not args.service:
            print("❌ Error: Service name required")
            print("Usage: securevault delete <service>")
            return
        
        entry = vault.get_password(args.service)
        if not entry:
            print(f"❌ No password found for: {args.service}")
            return
        
        print(f"Service:  {args.service}")
        print(f"Username: {entry['username']}")
        confirm = input(f"\n⚠️  Delete this entry? (yes/no): ")
        
        if confirm.lower() == 'yes':
            vault.delete_password(args.service)
            print(f"✅ Deleted password for: {args.service}")
        else:
            print("❌ Aborted")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🔒 SecureVault locked")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
