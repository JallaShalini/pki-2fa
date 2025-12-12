import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key):
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = plaintext.decode("utf-8")

    if len(seed) != 64 or any(c not in "0123456789abcdef" for c in seed.lower()):
        raise ValueError("Invalid seed format")

    return seed


def load_private_key(path="student_private.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


if __name__ == "__main__":
    private_key = load_private_key()

    with open("encrypted_seed.txt", "r") as f:
        encrypted_seed = f.read().strip()

    seed = decrypt_seed(encrypted_seed, private_key)

    with open("seed.txt", "w") as f:
        f.write(seed)

    print("Decrypted seed:", seed)
