import uuid
from http.client import HTTPException

import requests
from environs import Env

env = Env()
env.read_env()


def get_jwt_token(auth_token: str, scope: str = "GIGACHAT_API_PERS") -> str:
    """Function that sends a request and returns token."""
    rq_uid = str(uuid.uuid4())
    url = env.str("GIGA_AUTH_URL")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": rq_uid,
        "Authorization": f"Basic {auth_token}",
    }
    payload = {
        "scope": scope,
    }

    try:
        request = requests.post(url, headers=headers, data=payload, verify=False, timeout=5)  # noqa: S501
        return request.json()["access_token"]
    except requests.RequestException as e:
        msg = f"Error sending request: {e}"
        raise HTTPException(msg) from e
