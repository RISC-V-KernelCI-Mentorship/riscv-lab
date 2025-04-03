import sys
import time
import jwt

def generate_jwt(pem_path, client_id):
    with open(pem_path, "rb") as f:
        signing_key = f.read()
    now = int(time.time())
    payload = {
            "iat": now,
            "exp": now + 60*10, # Ten minutes
            "iss": client_id
    }
    enc_jwt = jwt.encode(payload, signing_key, algorithm="RS256")
    return enc_jwt

