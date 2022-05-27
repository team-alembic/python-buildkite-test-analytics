from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from .run_env import RuntimeEnvironment, detect_env

import json

JsonValue = Union[str, int, float, bool, 'JsonDict', List['JsonValue']]
JsonDict = Dict[str, JsonValue]


@dataclass(frozen=True)
class TestResult:
    pass


@dataclass(frozen=True)
class TestResultPassed(TestResult):
    pass


@dataclass(frozen=True)
class TestResultFailed(TestResult):
    failure_reason: Optional[str]


@dataclass(frozen=True)
class TestHistory:
    section: str
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    duration: Optional[timedelta]
    children: List['TestHistory']

    def is_finished(self) -> bool:
        self.end_at != None

    def as_json(self) -> JsonDict:
        attrs = {
            "section": self.section,
            "children": self.children.map(lambda child: child.as_json())
        }

        if (self.start_at is not None):
            attrs["start_at"] = self.start_at.microsecond() / 1_000_000.0

        if (self.end_at is not None):
            attrs["end_at"] = self.end_at.microsecond() / 1_000_000.0

        if (self.duration is not None):
            attrs["duration"] = self.duration.microsecond() / 1_000_000.0

        return attrs


@dataclass(frozen=True)
class TestData:
    id: str
    scope: str
    name: str
    identifier: str
    result: Optional[TestResult]
    history: TestHistory

    def is_finished(self) -> bool:
        self.history.is_finished()

    def as_json(self) -> JsonDict:
        attrs = {
            "id": self.id,
            "scope": self.scope,
            "name": self.name,
            "identifier": self.identifier,
            "history": self.history.to_json()
        }

        if (self.result is TestResultPassed):
            attrs["result"] = "passed"

        if (self.result is TestResultFailed):
            attrs["result"] = "failed"
            if (self.result.failure_reason is not None):
                attrs["failure_reason"] = self.result.failure_reason

        return attrs


@dataclass(frozen=True)
class Payload:
    run_env: RuntimeEnvironment
    data: List[TestData]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    @classmethod
    def init(_cls) -> 'Payload':
        return Payload(
            run_env=detect_env(),
            data=[],
            started_at=datetime.now(),
            finished_at=None
        )

    def as_json(self) -> JsonDict:
        finished_data = filter(
            self.data, lambda test_data: test_data.is_finished())

        attrs = {
            "format": "json",
            "run_env": self.run_env.as_json(),
            "data": list(finished_data),
        }

    def to_json(self) -> str:
        return json.dumps(self.as_json())
