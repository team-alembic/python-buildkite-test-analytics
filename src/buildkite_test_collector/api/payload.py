from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

from .run_env import RuntimeEnvironment, detect_env

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
        return self.end_at is not None

    def as_json(self, started_at: datetime) -> JsonDict:
        attrs = {
            "section": self.section,
            "children": list(map(lambda child: child.as_json(), self.children))
        }

        if self.start_at is not None:
            attrs["start_at"] = (self.start_at - started_at).total_seconds()

        if self.end_at is not None:
            attrs["end_at"] = (self.end_at - started_at).total_seconds()

        if self.duration is not None:
            attrs["duration"] = self.duration.total_seconds()

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
        return self.history and self.history.is_finished()

    def as_json(self, started_at: datetime) -> JsonDict:
        attrs = {
            "id": self.id,
            "scope": self.scope,
            "name": self.name,
            "identifier": self.identifier,
            "history": self.history.as_json(started_at)
        }

        if self.result is TestResultPassed:
            attrs["result"] = "passed"

        if self.result is TestResultFailed:
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
    def init(cls) -> 'Payload':
        return cls(
            run_env=detect_env(),
            data=[],
            started_at=datetime.now(),
            finished_at=None
        )

    def as_json(self) -> JsonDict:
        finished_data = filter(
            lambda td: td.is_finished(),
            self.data
        )

        return {
            "format": "json",
            "run_env": self.run_env.as_json(),
            "data": list(map(lambda td: td.as_json(self.started_at), finished_data)),
        }

    def push_test_data(self, report: TestData) -> 'Payload':
        return self.__class__(
            run_env=self.run_env,
            started_at=self.started_at,
            finished_at=self.finished_at,
            data=self.data + [report]
        )
