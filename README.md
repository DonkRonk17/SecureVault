# 🔐 SecureVault - Local Encrypted Password Manager

**Simple. Secure. Local.**

A command-line password manager with military-grade AES-256 encryption. Store passwords securely on YOUR computer—no cloud, no subscriptions, no tracking.

---

## 🎯 Why SecureVault?

**Problem:** Most password managers require:
- ☁️ Cloud services (privacy risk)
- 💰 Subscriptions ($36-60/year)
- 📱 Complex GUIs and sync setup
- 🔐 Trust in third-party encryption

**Solution:** SecureVault gives you:
- ✅ **Local storage** - Your passwords never leave your computer
- ✅ **AES-256 encryption** - Military-grade security
- ✅ **Free & open-source** - No subscriptions, no tracking
- ✅ **Simple CLI** - Fast and lightweight
- ✅ **Cross-platform** - Works on Windows, macOS, Linux
- ✅ **Secure password generator** - Create strong passwords instantly

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download
cd SecureVault

# Install dependencies
pip install -r requirements.txt

# Run directly
python securevault.py init
```

### First Time Setup

```bash
# Create your encrypted vault
python securevault.py init

# You'll be prompted to create a master password
# ⚠️  REMEMBER THIS PASSWORD - it cannot be recovered!
```

---

## 📖 Usage Guide

### Add a Password

```bash
# Interactive add
python securevault.py add github
# Enter username: your_username
# Enter password: ******** (or leave blank to generate)

# Password is encrypted and saved locally
```

### Retrieve a Password

```bash
# Get password (copies to clipboard automatically)
python securevault.py get github

# Output:
# Service:  github
# Username: your_username
# Password: your_secure_password
# Created:  2026-01-09 16:30:00
#
# ✅ Password copied to clipboard (will clear in 15 seconds)
```

### List All Passwords

```bash
# View all stored services
python securevault.py list

# Output:
# 📋 Stored passwords (3):
#
#   1. github
#      Username: your_username
#      Created:  2026-01-09 16:30:00
#
#   2. email
#      Username: you@example.com
#      Created:  2026-01-09 16:35:00
```

### Generate Strong Password

```bash
# Generate 20-character password (default)
python securevault.py generate

# Custom length
python securevault.py generate --length 32

# Without symbols (alphanumeric only)
python securevault.py generate --no-symbols

# Output:
# 🔑 Generated password: K#9mP$2vL@4xN&8wQ!1z
#    Length: 20 characters
#
# ✅ Password copied to clipboard
```

### Delete a Password

```bash
# Remove password entry
python securevault.py delete github

# You'll be asked to confirm before deletion
```

---

## 🔒 Security Features

### Military-Grade Encryption
- **AES-256-CBC** encryption algorithm
- **PBKDF2** key derivation with 100,000 iterations
- **Random salt** for each vault (prevents rainbow table attacks)
- **Random IV** for each encryption operation

### Secure Storage
- Vault file: `~/.securevault.enc`
- **Permissions:** Owner-only access (Unix/Linux/Mac)
- **No plaintext:** Passwords never stored unencrypted
- **Master password:** Never stored anywhere

### Safe Password Generation
- Uses Python's `secrets` module (cryptographically secure)
- Not `random` module (which is predictable)
- Configurable length and character sets

### Clipboard Security
- Auto-clear clipboard after 15 seconds
- Prevents password leakage to clipboard history
- Works cross-platform (optional dependency)

---

## 💡 Examples

### Example 1: Complete Workflow

```bash
# 1. Create vault
$ python securevault.py init
🔐 Creating new SecureVault...
Create master password: ********
Confirm master password: ********
✅ Vault created: /home/user/.securevault.enc
⚠️  IMPORTANT: Remember your master password!

# 2. Add GitHub password
$ python securevault.py add github
Enter master password: ********
✅ Vault unlocked

Username for github: octocat
Password for github (leave blank to generate):
🔑 Generated password: X#9mK$2vL@4zN&8wP!1q
   (Copy this now - it won't be shown again)

✅ Password saved for: github

# 3. Later, retrieve it
$ python securevault.py get github
Enter master password: ********
✅ Vault unlocked

Service:  github
Username: octocat
Password: X#9mK$2vL@4zN&8wP!1q
Created:  2026-01-09 16:30:00

✅ Password copied to clipboard (will clear in 15 seconds)
```

### Example 2: Migrate Existing Passwords

```bash
# Add all your existing passwords
python securevault.py add email
python securevault.py add bank
python securevault.py add work-vpn
python securevault.py add aws-console

# List to verify
python securevault.py list
```

### Example 3: Generate Passwords for New Accounts

```bash
# Create strong password for new service
python securevault.py generate --length 24

# Copy the generated password
# Use it to sign up for new account

# Then save it to vault
python securevault.py add new-service
# Paste the password when prompted
```

---

## 🛠️ Advanced Usage

### Optional: Install Clipboard Support

For automatic clipboard copy/paste:

```bash
pip install pyperclip
```

Without `pyperclip`, passwords are displayed on screen (you can copy manually).

### Custom Vault Location

Set environment variable:

```bash
# Linux/Mac
export SECUREVAULT_PATH="/path/to/vault.enc"

# Windows
set SECUREVAULT_PATH=C:\path\to\vault.enc
```

(Note: This requires modifying the script to read from environment variable)

### Backup Your Vault

```bash
# The vault file is a single encrypted file
# Back it up regularly:

# Linux/Mac
cp ~/.securevault.enc ~/backups/securevault-$(date +%Y%m%d).enc

# Windows
copy %USERPROFILE%\.securevault.enc %USERPROFILE%\backups\securevault-20260109.enc
```

**⚠️  IMPORTANT:** You need BOTH:
1. The vault file (`.securevault.enc`)
2. Your master password

Without the master password, the vault file is useless (which is good for security!).

---

## 🔧 Requirements

- **Python 3.6+**
- **cryptography** package (for encryption)
- **pyperclip** package (optional, for clipboard support)

Install with:
```bash
pip install -r requirements.txt
```

---

## ❓ FAQ

### Q: What if I forget my master password?
**A:** There is NO way to recover it. The vault uses strong encryption with NO backdoors. This is by design for maximum security. **Back up your master password securely!**

### Q: Where is my vault stored?
**A:** In your home directory: `~/.securevault.enc` (or `%USERPROFILE%\.securevault.enc` on Windows)

### Q: Is this safe to use for real passwords?
**A:** Yes! SecureVault uses:
- AES-256 encryption (same as military/government)
- PBKDF2 key derivation (industry standard)
- Secure random generation (cryptographically strong)
- No network access (fully offline)

However, like any security tool, you should:
- Use a STRONG master password
- Keep your vault file backed up
- Keep your computer secure (antivirus, updates, etc.)

### Q: Can I use this on multiple computers?
**A:** Yes! Copy your `.securevault.enc` file to another computer (via USB drive, secure file transfer, etc.). Then use the same master password.

### Q: How is this different from LastPass/1Password?
**A:** 
- ✅ **Free & open-source** (no $36-60/year subscription)
- ✅ **Local only** (no cloud sync = better privacy)
- ✅ **CLI interface** (faster for power users)
- ❌ No browser integration (manual copy/paste)
- ❌ No automatic sync (manual file transfer)
- ❌ No mobile app (desktop only)

SecureVault is for users who want maximum privacy, control, and simplicity.

---

## 📋 Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Create new encrypted vault | `python securevault.py init` |
| `add <service>` | Add/update password entry | `python securevault.py add github` |
| `get <service>` | Retrieve password (copies to clipboard) | `python securevault.py get github` |
| `list` | List all stored services | `python securevault.py list` |
| `generate` | Generate strong random password | `python securevault.py generate --length 24` |
| `delete <service>` | Delete password entry | `python securevault.py delete github` |

---

## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - see LICENSE file for details.

**TL;DR:** Free to use, modify, and distribute. No warranty provided.

---

## ⚠️ Security Notice

- **Never** share your master password
- **Never** commit `.securevault.enc` to Git/GitHub
- **Always** use strong master passwords (12+ characters, mixed case, symbols)
- **Regularly** back up your vault file
- **Keep** your computer secure (antivirus, firewall, updates)

---

## 🎖️ Credits

Created with ❤️ as part of the Holy Grail Automation project.

**Technology:**
- Python 3
- cryptography (PyCA) library
- AES-256-CBC encryption
- PBKDF2 key derivation

---

**🔐 Your passwords. Your computer. Your control.**
