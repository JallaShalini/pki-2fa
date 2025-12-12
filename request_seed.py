import json
import requests

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str, public_key_file: str = "student_public.pem"):
    with open(public_key_file, "r") as f:
        public_key = f.read()

    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    response = requests.post(API_URL, json=payload, timeout=20)
    data = response.json()
    print(data)

    if data.get("status") != "success":
        return

    encrypted_seed = data["encrypted_seed"]

    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    return encrypted_seed


if __name__ == "__main__":
    student_id = "YOUR_STUDENT_ID"
    github_repo_url = "https://github.com/yourusername/pki-2fa"

    request_seed(student_id, github_repo_url)
