import base64
import os
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def load_private_key(path=None):
    """Load private key from file.
    Tries multiple common locations if path is not specified.
    """
    if path is None:
        # Try to find the key in common locations
        possible_paths = [
            Path("/app/student_private.pem"),
            Path("student_private.pem"),
            Path("../student_private.pem"),
            Path(__file__).parent.parent / "student_private.pem",
        ]
        for possible_path in possible_paths:
            if possible_path.exists():
                path = str(possible_path)
                break
        if path is None:
            raise FileNotFoundError(
                f"Could not find student_private.pem in any expected location"
            )
    
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def decrypt_seed(encrypted_seed_b64: str, private_key):
    """Decrypt seed using RSA private key with OAEP padding."""
    ciphertext = base64.b64decode(encrypted_seed_b64)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    seed = plaintext.decode("utf-8").strip()
    if len(seed) != 64 or any(c not in "0123456789abcdef" for c in seed.lower()):
        raise ValueError("Invalid seed format")
    return seed
