from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from .payload import Payload


@dataclass(frozen=True)
class ApiResponse:
    id: str
    run_id: str
    queued: int
    skipped: int
    errors: List[str]


def submit(payload: Payload) -> ApiResponse:
    # do the thing
    pass
