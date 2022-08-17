import jwt
import os
from dotenv import load_dotenv

load_dotenv()


def generate_token(payload: dict):
    encoded_jwt = jwt.encode(
        payload,
        os.environ.get("JWT_SECRET"),
        algorithm=os.environ.get("JWT_ALGORITHMS"),
    )

    return encoded_jwt


def decode(encoded_jwt):
    result = jwt.decode(
        encoded_jwt,
        os.environ.get("JWT_SECRET"),
        algorithms=os.environ.get("JWT_ALGORITHMS"),
    )
    return result


if __name__ == "__main__":
    a = generate_token(payload={"sub": "user_jwt"})
    print(a)
    b = decode(a)
    print(b)
