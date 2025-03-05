import json
import base64
import os
from getpass import getpass
from typing import Dict, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class PasswordManager:
    def __init__(self, storage_file: str = "passwords.json"):
        self.storage_file = storage_file
        self.fernet = None
        self.credentials = {}
        self._salt = None

    def _generate_key(self, master_password: str, salt: Optional[bytes] = None) -> bytes:
        """Generate encryption key from master password using PBKDF2."""
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt

    def initialize(self, master_password: str) -> None:
        """Initialize or unlock the password manager."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self._salt = base64.b64decode(data.get('salt', ''))
                    key, _ = self._generate_key(master_password, self._salt)
                    self.fernet = Fernet(key)
                    # Try to decrypt to verify master password
                    encrypted_test = data.get('test')
                    if encrypted_test:
                        self.fernet.decrypt(encrypted_test.encode())
                    self.credentials = {
                        site: encrypted
                        for site, encrypted in data.get('credentials', {}).items()
                    }
            else:
                # First time setup
                key, salt = self._generate_key(master_password)
                self.fernet = Fernet(key)
                self._salt = salt
                self._save_data()
        except Exception as e:
            raise ValueError("Invalid master password or corrupted data")

    def add_credential(self, site: str, username: str, password: str) -> None:
        """Add or update credentials for a website."""
        if not self.fernet:
            raise ValueError("Password manager not initialized")
        
        credential_data = json.dumps({"username": username, "password": password})
        encrypted_data = self.fernet.encrypt(credential_data.encode()).decode()
        self.credentials[site] = encrypted_data
        self._save_data()

    def get_credential(self, site: str) -> Dict[str, str]:
        """Retrieve credentials for a website."""
        if not self.fernet:
            raise ValueError("Password manager not initialized")
        
        encrypted_data = self.credentials.get(site)
        if not encrypted_data:
            raise KeyError(f"No credentials found for {site}")
        
        decrypted_data = self.fernet.decrypt(encrypted_data.encode()).decode()
        return json.loads(decrypted_data)

    def list_sites(self) -> list:
        """List all stored website names."""
        return list(self.credentials.keys())

    def delete_credential(self, site: str) -> None:
        """Delete credentials for a website."""
        if site in self.credentials:
            del self.credentials[site]
            self._save_data()

    def _save_data(self) -> None:
        """Save encrypted data to file."""
        if not self.fernet:
            raise ValueError("Password manager not initialized")
        
        # Save a test string to verify master password on next unlock
        test_encrypted = self.fernet.encrypt(b"test").decode()
        
        data = {
            'salt': base64.b64encode(self._salt).decode(),
            'test': test_encrypted,
            'credentials': self.credentials
        }
        
        with open(self.storage_file, 'w') as f:
            json.dump(data, f)

def main():
    pm = PasswordManager()
    
    while True:
        print("\nSOManager - Password Manager")
        print("1. Initialize/Unlock")
        print("2. Add Credential")
        print("3. Get Credential")
        print("4. List Sites")
        print("5. Delete Credential")
        print("6. Exit")
        
        choice = input("\nChoice (1-6): ")
        
        try:
            if choice == "1":
                master_pass = getpass("Enter master password: ")
                pm.initialize(master_pass)
                print("Password manager unlocked!")
                
            elif choice == "2":
                site = input("Website: ")
                username = input("Username: ")
                password = getpass("Password: ")
                pm.add_credential(site, username, password)
                print(f"Credentials for {site} saved!")
                
            elif choice == "3":
                site = input("Website: ")
                cred = pm.get_credential(site)
                print(f"\nUsername: {cred['username']}")
                print(f"Password: {cred['password']}")
                
            elif choice == "4":
                sites = pm.list_sites()
                print("\nStored sites:")
                for site in sites:
                    print(f"- {site}")
                    
            elif choice == "5":
                site = input("Website to delete: ")
                pm.delete_credential(site)
                print(f"Credentials for {site} deleted!")
                
            elif choice == "6":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice!")
                
        except ValueError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
