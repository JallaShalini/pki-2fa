import time
from datetime import datetime, timezone
from pathlib import Path

from app.totp_utils import generate_totp_code

seed_file = Path("/data/seed.txt")

if not seed_file.exists():
    print("Seed not found")
    exit(1)

seed = seed_file.read_text().strip()

code = generate_totp_code(seed)

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

print(f"{timestamp} - 2FA Code: {code}")
