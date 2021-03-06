import pytest

from datetime import datetime, timedelta
from uuid import uuid4
from random import randint
from dataclasses import replace

from buildkite_test_collector.collector.payload import TestData, TestResultPassed, TestHistory, Payload, TestResultFailed, TestResultSkipped
from buildkite_test_collector.collector.run_env import RuntimeEnvironment


@pytest.fixture
def successful_test(history_finished) -> TestData:
    return TestData(
        id=uuid4(),
        scope="wyld stallyns",
        name="san dimas meltdown",
        identifier="wyld stallyns :: san dimas meltdown",
        location="san_dimas_meltdown.py:1",
        result=TestResultPassed(),
        history=history_finished
    )


@pytest.fixture
def failed_test(successful_test) -> TestData:
    return replace(successful_test, result=TestResultFailed("bogus"))


@pytest.fixture
def skipped_test(successful_test) -> TestData:
    return replace(successful_test, result=TestResultSkipped())


@pytest.fixture
def incomplete_test(history_started) -> TestData:
    return TestData(
        id=uuid4(),
        scope="wyld stallyns",
        name="san dimas meltdown",
        identifier="wyld stallyns :: san dimas meltdown",
        location="san_dimas_meltdown.py:1",
        result=None,
        history=history_started
    )


@pytest.fixture
def history_started() -> TestHistory:
    return TestHistory(
        section="top",
        start_at=datetime.utcnow(),
        end_at=None,
        duration=None,
        children=[]
    )


@pytest.fixture
def history_finished() -> TestHistory:
    start_at = datetime.utcnow()
    duration = timedelta(minutes=2, seconds=18)
    end_at = start_at + duration

    return TestHistory(
        section="top",
        start_at=start_at,
        end_at=end_at,
        duration=duration,
        children=[]
    )


@pytest.fixture
def fake_env() -> RuntimeEnvironment:
    return RuntimeEnvironment(
        ci="example",
        key=str(uuid4()),
        number=str(randint(0, 1000)),
        job_id=str(randint(0, 1000)),
        branch="rufus",
        commit_sha=uuid4().hex,
        message="Be excellent to each other",
        url="https://example.test/buildkite")


@pytest.fixture
def payload(fake_env) -> Payload:
    return Payload.started(Payload.init(fake_env))
