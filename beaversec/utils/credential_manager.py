"""Secure credential management for BeaverSec."""

import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from beaversec.core.exceptions import CredentialError
from beaversec.utils.audit_logger import AuditLogger


class CredentialManager:
    """
    Secure credential storage and retrieval.

    Uses Fernet symmetric encryption with PBKDF2 key derivation.
    """

    _instance = None

    def __new__(cls):
        """Singleton pattern for CredentialManager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize credential manager."""
        self.logger = AuditLogger.get_logger("credentials")
        self.credential_dir = Path.home() / ".beaversec" / "credentials"
        self.credential_dir.mkdir(parents=True, exist_ok=True)

        self._key_file = self.credential_dir / "key.enc"
        self._credentials_file = self.credential_dir / "credentials.enc"

        self._fernet = None
        self._load_key()

    def _load_key(self):
        """Load or generate encryption key."""
        try:
            if self._key_file.exists():
                with open(self._key_file, "rb") as f:
                    key_data = f.read()
                    decoded_key = base64.b64decode(key_data)
                    self._fernet = Fernet(decoded_key)
            else:
                # Generate new key
                key = Fernet.generate_key()
                with open(self._key_file, "wb") as f:
                    f.write(base64.b64encode(key))
                os.chmod(self._key_file, 0o600)
                self._fernet = Fernet(key)
        except Exception as e:
            raise CredentialError(f"Failed to load encryption key: {e}")

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive encryption key from password.

        Args:
            password: Password string
            salt: Salt bytes

        Returns:
            bytes: Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def set_credential(self, service: str, key: str, value: str) -> None:
        """
        Store a credential securely.

        Args:
            service: Service name
            key: Credential key
            value: Credential value

        Raises:
            CredentialError: If storage fails
        """
        try:
            credentials = self._load_credentials()

            if service not in credentials:
                credentials[service] = {}

            credentials[service][key] = value

            self._save_credentials(credentials)
            self.logger.info(f"Credential stored for service: {service}")

        except Exception as e:
            raise CredentialError(f"Failed to store credential: {e}")

    def get_credential(self, service: str, key: str) -> Optional[str]:
        """
        Retrieve a credential.

        Args:
            service: Service name
            key: Credential key

        Returns:
            Optional[str]: Credential value or None if not found

        Raises:
            CredentialError: If retrieval fails
        """
        try:
            credentials = self._load_credentials()

            if service not in credentials:
                return None

            return credentials[service].get(key)

        except Exception as e:
            raise CredentialError(f"Failed to retrieve credential: {e}")

    def get_service_credentials(self, service: str) -> Dict[str, str]:
        """
        Get all credentials for a service.

        Args:
            service: Service name

        Returns:
            Dict[str, str]: Service credentials

        Raises:
            CredentialError: If retrieval fails
        """
        try:
            credentials = self._load_credentials()
            return credentials.get(service, {})

        except Exception as e:
            raise CredentialError(f"Failed to retrieve service credentials: {e}")

    def _load_credentials(self) -> Dict[str, Dict[str, str]]:
        """
        Load and decrypt credentials.

        Returns:
            Dict[str, Dict[str, str]]: Credentials dictionary

        Raises:
            CredentialError: If loading fails
        """
        if not self._credentials_file.exists():
            return {}

        try:
            with open(self._credentials_file, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = self._fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())

        except Exception as e:
            raise CredentialError(f"Failed to load credentials: {e}")

    def _save_credentials(self, credentials: Dict[str, Dict[str, str]]) -> None:
        """
        Encrypt and save credentials.

        Args:
            credentials: Credentials dictionary

        Raises:
            CredentialError: If saving fails
        """
        try:
            json_data = json.dumps(credentials)
            encrypted_data = self._fernet.encrypt(json_data.encode())

            with open(self._credentials_file, "wb") as f:
                f.write(encrypted_data)

            os.chmod(self._credentials_file, 0o600)

        except Exception as e:
            raise CredentialError(f"Failed to save credentials: {e}")

    def delete_credential(self, service: str, key: str) -> bool:
        """
        Delete a credential.

        Args:
            service: Service name
            key: Credential key

        Returns:
            bool: True if deleted, False if not found

        Raises:
            CredentialError: If deletion fails
        """
        try:
            credentials = self._load_credentials()

            if service not in credentials:
                return False

            if key not in credentials[service]:
                return False

            del credentials[service][key]

            if not credentials[service]:
                del credentials[service]

            self._save_credentials(credentials)
            self.logger.info(f"Credential deleted: {service}.{key}")
            return True

        except Exception as e:
            raise CredentialError(f"Failed to delete credential: {e}")