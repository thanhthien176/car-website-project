"""
Symmetric encryption (Fernet) + SHA-256 hashing utilities for sensitive fields.

Design decisions:
- Fernet: AES-128-CBC + HMAC-SHA256, provides authenticated encryption.
  Tampered ciphertext raises InvalidToken instead of silently returning garbage.
- SHA-256 hash with SALT: used for lookups (phone, cccd) without decrypting.
  Salt prevents rainbow table attacks — same value produces different hash
  across projects even if they share the same plaintext.
- Key lives in environment variable only — never in code or database.
  If DB is compromised without the key, ciphertext is useless to attacker.

Usage:
    from users.encryption import encrypt, decrypt, make_hash

    encrypted = encrypt("0901234567")
    original  = decrypt(encrypted)
    hashed    = make_hash("0901234567")  # for DB lookup
"""
import hashlib
import hmac
import os

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def _get_fernet():
    """
    Load the Fernet instance from settings.

    ENCRYPTION_KEY must be a valid Fernet key (32 url-safe base64 bytes).
    Generate one with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
    """
    key = getattr(settings, "ENCRYPTION_KEY", None)
    if not key:
        raise ValueError(
            "ENCRYPTION_KEY is not set in settings."
            "Generate one with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return Fernet(key.encode() if isinstance(key, str) else key)

def encrypt(value: str) -> str:
    """
    Encrypt a plaintext string. Returns ciphertext as a UTF-8 string.
    Returns empty string if value is empty - avoids encrypting blank fields.
    """
    if not value:
        return ""
    fernet = _get_fernet()
    
    return fernet.encrypt(value.encode()).decode()

def decrypt(ciphertext: str) -> str:
    """
    Decrypt a ciphertext string back to plaintext.
    Returns empty string if ciphertext is empty or decryption fails.
    
    Why catch InvalidToken silently?
    - Corrupted data in DB should not crash the entire page render.
    - Admin will see empty field instead of 500 error.
    - Real errors are logged for investigation.
    """
    if not ciphertext:
        return ""
    
    try:
        fernet = _get_fernet()
        return fernet.decrypt(ciphertext.encode()).decode()
    except (InvalidToken, Exception):
        logger.error("Failed to decrypt value - data may be corrupted or key mismatch")
        return ""
    
def make_hash(value: str) -> str:
    """
    Create a SHA-256 HMAC hash of value using ENCRYPTION_HASH_SALT.
    Used for database lookups without decrypting (searchable encryption pattern).

    HMAC vs plain SHA-256:
    - Plain SHA-256: hash("0901234567") — attacker with salt can precompute rainbow table
    - HMAC-SHA256:  hmac(key, "0901234567") — requires knowing the secret key to attack
    Returns empty string if value is empty.
    """
    if not value:
        return ""
    
    salt = getattr(settings, "ENCRYPTION_HASH_SALT", None)
    if not salt:
        raise ValueError("ENCRYPTION_HASH_SALT is not set in settings.")
    
    return hmac.new(
        salt.encode(),
        value.encode(),
        hashlib.sha256
    ).hexdigest()