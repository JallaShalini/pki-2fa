import base64
import pyotp

def hex_to_base32(hex_seed: str) -> str:
    raw = bytes.fromhex(hex_seed)
    return base64.b32encode(raw).decode().replace("=", "")

def generate_totp_code(hex_seed: str) -> str:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32)
    return totp.verify(code, valid_window=valid_window)
