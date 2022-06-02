from dataclasses import dataclass
from typing import List

import os
import requests

from .payload import Payload


@dataclass(frozen=True)
class ApiResponse:
    id: str
    run_id: str
    queued: int
    skipped: int
    errors: List[str]


class MissingTokenError(Exception):
    pass


def __get_token() -> str:
    token = os.environ.get("BUILDKITE_ANALYTICS_API_TOKEN")

    if (token is None or token == ''):
        raise MissingTokenError(
            "Please set the BUILDKITE_ANALYTICS_API_TOKEN environment variable")

    return token


def submit(payload: Payload) -> ApiResponse:
    token = __get_token()

    return requests.post("https://analytics-api.buildkite.com/v1/uploads", json=payload.as_json(), headers={
        "Content-Type": "application/json",
        "Authorization": f"Token token=\"{token}\""
    })
