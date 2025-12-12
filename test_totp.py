from totp_utils import generate_totp_code, verify_totp_code

seed = "54db96cc33a6fa25d2763f3add0a392d8e3a4874c95b9eb8786cc160064b0b04"

code = generate_totp_code(seed)
print("TOTP:", code)

print("Valid?", verify_totp_code(seed, code))
