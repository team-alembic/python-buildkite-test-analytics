from random import randint
from uuid import uuid4
import os
import pytest
import mock

from bkta.api.run_env import UnknownEnvironmentError, detect_env


def test_detect_env_with_no_env_vars_raises_an_error():
    with mock.patch.dict(os.environ, {}):
        with pytest.raises(UnknownEnvironmentError):
            detect_env()


def test_detect_env_with_buildkite_api_env_vars_returns_the_correct_environment():
    id = str(uuid4())
    commit = uuid4().hex
    number = str(randint(0, 1000))
    job_id = str(randint(0, 1000))

    env = {
        "BUILDKITE_BUILD_ID": id,
        "BUILDKITE_BUILD_URL": "https://example.test/buildkite",
        "BUILDKITE_BRANCH": "rufus",
        "BUILDKITE_COMMIT": commit,
        "BUILDKITE_BUILD_NUMBER": number,
        "BUILDKITE_JOB_ID": job_id,
        "BUILDKITE_MESSAGE": "All we are is dust in the wind, dude.",
    }
    with mock.patch.dict(os.environ, env):
        runtime_env = detect_env()

        assert runtime_env.ci == "buildkite"
        assert runtime_env.key == id
        assert runtime_env.url == "https://example.test/buildkite"
        assert runtime_env.branch == "rufus"
        assert runtime_env.commit_sha == commit
        assert runtime_env.number == number
        assert runtime_env.job_id == job_id
        assert runtime_env.message == "All we are is dust in the wind, dude."
