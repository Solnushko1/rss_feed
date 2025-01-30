import json
from http.client import HTTPException
from typing import Any

import requests
from environs import Env

env = Env()
env.read_env()


def generate_prompt_with_user_text(user_text: str) -> str:
    """Compound user text and prompt."""
    prompt_text = "Перескажи данный текст в стиле опытного журналиста"
    return prompt_text + "\n" + user_text


def generate_payload(user_message: str) -> str:
    """Function that generates Payload."""
    return json.dumps(
        {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": generate_prompt_with_user_text(user_text=user_message),
                },
            ],
            "temperature": 1,
            "top_p": 0.1,
            "n": 1,
            "stream": False,
            "max_tokens": 512,
            "repetition_penalty": 1,
            "update_interval": 0,
        },
    )


def generate_header(auth_token: str) -> dict[str, str]:
    """Function that generates Header."""
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {auth_token}",
    }


def send_request(url: str, header: dict[str, str], payload: str) -> dict[str, Any]:
    """Function that sends request."""
    try:
        return requests.request("POST", url, headers=header, data=payload, verify=False, timeout=10).json()
    except requests.RequestException as e:
        msg = f"Error sending request: {e}"
        raise HTTPException(msg) from e


def json_transformation(response: dict[str, Any]) -> str:
    """Function that transforms json data."""
    return str(response["choices"][0]["message"]["content"])


def get_answer(auth_token: str, user_message: str) -> str:
    """A function that returns the generated response from AI."""
    url = env.str("GIGA_ANSWER_URL")
    payload = generate_payload(user_message=user_message)
    header = generate_header(auth_token=auth_token)
    response = send_request(url=url, header=header, payload=payload)
    return json_transformation(response=response)
