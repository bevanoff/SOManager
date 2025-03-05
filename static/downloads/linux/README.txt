SOManager Password Manager
========================

Thank you for downloading SOManager! This package includes both a command-line interface (CLI) and a graphical user interface (GUI) version of the password manager.

Files Included:
- password_manager.py: Command-line interface version
- password_manager_gui.py: Graphical user interface version

System Requirements:
- Python 3.8 or newer
- 2GB RAM minimum
- 100MB free disk space
- Required Python packages: cryptography, tkinter

Installation:
1. Make sure Python 3.8 or newer is installed on your system
2. Install required package using pip:
   pip install cryptography

Usage:
1. GUI Version:
   - Run: python password_manager_gui.py
   - Enter a master password to create or unlock your password vault
   - Use the interface to add, view, or delete credentials

2. CLI Version:
   - Run: python password_manager.py
   - Follow the menu prompts to:
     1. Initialize/Unlock with master password
     2. Add credentials
     3. Retrieve credentials
     4. List saved sites
     5. Delete credentials
     6. Exit

Security Features:
- Military-grade encryption (AES-256)
- Master password protection
- Secure storage of multiple website credentials
- Completely offline operation for maximum security

For support or to report issues, visit our website: https://somanager.replit.app
