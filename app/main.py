from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import time
import logging

from app.crypto_utils import load_private_key, decrypt_seed
from app.totp_utils import generate_totp_code, verify_totp_code

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

DATA_DIR = Path("/data")
SEED_FILE = DATA_DIR / "seed.txt"


class SeedRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


# POST /decrypt-seed
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: SeedRequest):
    try:
        logger.info("Attempting to decrypt seed")
        private_key = load_private_key()
        seed = decrypt_seed(req.encrypted_seed, private_key)
        
        # Create data directory and write seed
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SEED_FILE.write_text(seed)
        logger.info("Seed decrypted and written successfully")
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Decryption error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})


# GET /generate-2fa
@app.get("/generate-2fa")
def generate_2fa():
    try:
        if not SEED_FILE.exists():
            logger.error("Seed file not found")
            raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
        
        seed = SEED_FILE.read_text().strip()
        code = generate_totp_code(seed)
        period = 30
        remaining = period - (int(time.time()) % period)
        
        return {"code": code, "valid_for": remaining}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TOTP generation error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Failed to generate 2FA code"})


# POST /verify-2fa
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    try:
        if not req.code:
            raise HTTPException(status_code=400, detail={"error": "Missing code"})
        
        if not SEED_FILE.exists():
            logger.error("Seed file not found for verification")
            raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
        
        seed = SEED_FILE.read_text().strip()
        is_valid = verify_totp_code(seed, req.code)
        
        return {"valid": is_valid}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TOTP verification error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Failed to verify 2FA code"})
