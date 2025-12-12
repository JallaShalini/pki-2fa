from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import time

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

DATA_DIR = Path("/data")
SEED_FILE = DATA_DIR / "seed.txt"

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str


# ---------------------------
# POST /decrypt-seed
# ---------------------------
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: SeedRequest):
    try:
        private_key = load_private_key()
        seed = decrypt_seed(req.encrypted_seed, private_key)

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SEED_FILE.write_text(seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})


# ---------------------------
# GET /generate-2fa
# ---------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    seed = SEED_FILE.read_text().strip()
    code = generate_totp_code(seed)

    period = 30
    remaining = period - (int(time.time()) % period)

    return {"code": code, "valid_for": remaining}


# ---------------------------
# POST /verify-2fa
# ---------------------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})

    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})

    seed = SEED_FILE.read_text().strip()
    is_valid = verify_totp_code(seed, req.code)

    return {"valid": is_valid}
