from datetime import datetime, timedelta
from uuid import uuid4

import os
import pytest
import mock
import responses

from buildkite_test_collector.api.api import submit, MissingTokenError
from buildkite_test_collector.api.payload import Payload, TestData, TestResultPassed, TestHistory


def test_submit_with_missing_api_key_environment_variable():
    with mock.patch.dict(os.environ, {"CI": "true"}):
        with pytest.raises(MissingTokenError):
            payload = Payload.init()

            submit(payload)


@responses.activate
def test_submit_with_payload_returns_an_api_response():
    responses.add(
        responses.POST,
        "https://analytics-api.buildkite.com/v1/uploads",
        json={'id': str(uuid4()),
              'run_id': str(uuid4()),
              'queued': 1,
              'skipped': 0,
              'errors': [],
              'run_url': 'https://buildkite.com/organizations/alembic/analytics/suites/test/runs/52c5d9f6-a4f2-4a2d-a1e6-993335789c92'},
        status=202)

    with mock.patch.dict(os.environ, {"CI": "true", "BUILDKITE_ANALYTICS_API_TOKEN": str(uuid4())}):
        payload = Payload.init()

        payload = payload.push_test_data(__successful_test())

        result = submit(payload)

        assert result.status_code >= 200
        assert result.status_code < 300

        json = result.json()
        assert len(json["errors"]) == 0
        assert json['queued'] == 1


def __successful_test() -> TestData:
    start_at = datetime.utcnow()
    duration = timedelta(minutes=2, seconds=18)
    end_at = start_at + duration

    return TestData(
        id=str(uuid4()),
        scope="wyld stallyns",
        name="san dimas meltdown",
        identifier="wyld stallyns :: san dimas meltdown",
        result=TestResultPassed(),
        history=TestHistory(
            section="top",
            start_at=start_at,
            end_at=end_at,
            duration=duration,
            children=[]
        )
    )
