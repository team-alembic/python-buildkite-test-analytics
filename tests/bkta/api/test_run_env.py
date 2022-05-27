from cProfile import run
from random import randint
from uuid import uuid4, UUID
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


def test_detect_env_with_github_actions_env_vars_returns_the_correct_environment():
    run_number = str(randint(0, 1000))
    run_attempt = str(randint(0, 1000))
    run_id = str(uuid4())
    commit = uuid4().hex

    env = {
        "GITHUB_ACTION": "bring-about-world-peace",
        "GITHUB_RUN_NUMBER": run_number,
        "GITHUB_RUN_ATTEMPT": run_attempt,
        "GITHUB_REPOSITORY": "bill-and-ted/phone-booth",
        "GITHUB_RUN_ID": run_id,
        "GITHUB_REF": "rufus",
        "GITHUB_SHA": commit,
    }

    with mock.patch.dict(os.environ, env):
        runtime_env = detect_env()

        assert runtime_env.ci == "github_actions"
        assert runtime_env.key == "bring-about-world-peace-{}-{}".format(
            run_number, run_attempt)
        assert runtime_env.url == "https://github.com/bill-and-ted/phone-booth/actions/runs/{}".format(
            run_id)
        assert runtime_env.branch == "rufus"
        assert runtime_env.commit_sha == commit
        assert runtime_env.number == run_number
        assert runtime_env.job_id == None
        assert runtime_env.message == None


def test_detect_env_with_circle_ci_env_vars_returns_the_correct_environment():
    build_num = str(randint(0, 1000))
    workflow_id = str(uuid4())
    commit = uuid4().hex

    env = {
        "CIRCLE_BUILD_NUM": build_num,
        "CIRCLE_WORKFLOW_ID": workflow_id,
        "CIRCLE_BUILD_URL": "https://example.test/circle",
        "CIRCLE_BRANCH": "rufus",
        "CIRCLE_SHA1": commit
    }

    with mock.patch.dict(os.environ, env):
        runtime_env = detect_env()

        assert runtime_env.ci == "circleci"
        assert runtime_env.key == "{}-{}".format(workflow_id, build_num)
        assert runtime_env.url == "https://example.test/circle"
        assert runtime_env.branch == "rufus"
        assert runtime_env.commit_sha == commit
        assert runtime_env.number == build_num
        assert runtime_env.job_id == None
        assert runtime_env.message == None


def test_detect_env_with_generic_env_vars():
    env = {
        "CI": "true"
    }

    with mock.patch.dict(os.environ, env):
        runtime_env = detect_env()

        assert runtime_env.ci == "generic"
        assert UUID(runtime_env.key)
        assert runtime_env.url == None
        assert runtime_env.branch == None
        assert runtime_env.commit_sha == None
        assert runtime_env.number == None
        assert runtime_env.job_id == None
        assert runtime_env.message == None
