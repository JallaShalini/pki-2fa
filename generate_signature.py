#!/usr/bin/env python3
"""
Generate encrypted signature for commit proof
Run this script in your local repository to generate the new encrypted signature
"""

import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import subprocess
import sys

def load_private_key(key_path="student_private.pem"):
    """Load student private key from PEM file"""
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key(key_path="instructor_public.pem"):
    """Load instructor public key from PEM file"""
    with open(key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def get_commit_hash():
    """Get the latest commit hash from git"""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting commit hash: {e}")
        print("Make sure you're in a git repository")
        sys.exit(1)

def sign_message(message, private_key):
    """Sign message using RSA-PSS with SHA-256"""
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_signature(signature, public_key):
    """Encrypt signature using RSA/OAEP with SHA-256"""
    encrypted = public_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def main():
    print("\n=== PKI-2FA Signature Generator ===")
    print("\n1. Getting commit hash...")
    commit_hash = get_commit_hash()
    print(f"   Commit hash: {commit_hash}")
    
    print("\n2. Loading student private key...")
    private_key = load_private_key()
    print("   ✓ Private key loaded")
    
    print("\n3. Signing commit hash with RSA-PSS-SHA256...")
    signature = sign_message(commit_hash, private_key)
    print(f"   ✓ Signature created ({len(signature)} bytes)")
    
    print("\n4. Loading instructor public key...")
    public_key = load_public_key()
    print("   ✓ Public key loaded")
    
    print("\n5. Encrypting signature with RSA/OAEP-SHA256...")
    encrypted_signature = encrypt_signature(signature, public_key)
    print(f"   ✓ Encryption done ({len(encrypted_signature)} bytes)")
    
    print("\n6. Base64 encoding encrypted signature...")
    encrypted_b64 = base64.b64encode(encrypted_signature).decode('utf-8')
    print("   ✓ Encoding complete")
    
    print("\n7. Saving to encrypted_signature.b64...")
    with open("encrypted_signature.b64", "w") as f:
        f.write(encrypted_b64)
    print("   ✓ File saved")
    
    print("\n" + "="*50)
    print("SUCCESS! Signature generated.")
    print("="*50)
    print(f"\nCommit Hash: {commit_hash}")
    print(f"\nEncrypted Signature (first 50 chars):")
    print(f"{encrypted_b64[:50]}...")
    print(f"\nFull encrypted signature saved to: encrypted_signature.b64")
    print(f"\nTotal length: {len(encrypted_b64)} characters")
    print("\n⚠️  NEXT STEPS:")
    print(f"1. Copy the commit hash: {commit_hash}")
    print(f"2. Copy the encrypted signature from encrypted_signature.b64")
    print("3. Use these in your Partnr submission")
    print("\n")

if __name__ == "__main__":
    main()
