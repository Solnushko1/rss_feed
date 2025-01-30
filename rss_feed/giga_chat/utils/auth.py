import requests
from environs import Env
from starlette import status

env = Env()
env.read_env()


def check_auth(giga_jwt_token: str) -> bool:
    url = env.str("GIGA_CHECK_AUTH")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {giga_jwt_token}",
    }

    response = requests.request("GET", url, headers=headers, data={}, verify=False, timeout=5)
    return response.status_code == status.HTTP_200_OK
