import argparse
import datetime
import sys
import time
from collections import defaultdict
from typing import List, Optional

import termcolor

from duckietown_challenges.rest import ServerIsDown
from duckietown_challenges.rest_methods import dtserver_get_info, dtserver_get_user_submissions
from duckietown_challenges import ChallengeName, SubmissionID
from duckietown_challenges_runner.exceptions import UserError
from . import logger
from .cli_common import ChallengeEnvironment, wrap_server_operations

usage = """

To follow the fate of the submission, use:

    %(prog)s --submission ID


"""

__all__ = ["dt_challenges_cli_follow"]


def dt_challenges_cli_follow(args: List[str], environment: ChallengeEnvironment):
    """Follows the fate of a submission."""
    prog = "dts challenges follow"

    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--submission", type=int)
    parser.add_argument("--label", type=str)
    parser.add_argument("--challenge", type=str)
    parser.add_argument("--exit-when-complete", default=False, action="store_true")
    parsed = parser.parse_args(args)

    token = environment.token

    submission_id = parsed.submission
    user_label = parsed.label
    challenge_name = parsed.challenge

    # if submission_id is None and label is None and challenge is None:
    #     msg = "Must give either submission_id or label or challenge is None. "
    #     raise UserError(msg)
    exit_when_complete = parsed.exit_when_complete
    with wrap_server_operations():
        follow_submission(
            token,
            submission_id=submission_id,
            user_label=user_label,
            challenge_name=challenge_name,
            exit_when_complete=exit_when_complete,
        )


def follow_submission(
    token: str,
    submission_id: Optional[SubmissionID],
    user_label: Optional[str],
    challenge_name: Optional[ChallengeName],
    exit_when_complete: bool,
):
    step2job_seen = {}
    step2status_seen = defaultdict(lambda: "")

    print("")

    # 137: {
    #     'submission_id': 137, 'complete': False, 'status': None,
    #     'date_submitted': datetime.datetime(2021, 10, 19, 9, 47, 18),
    #     'last_status_change': datetime.datetime(2021, 10, 19, 9, 47, 48),
    #     'parameters': {'hash': 'sha256:b011ca9a95a481e0f0aac9e9d300d99f7c5d1187a406c301a5b4815d41e75d6f'},
    #     'challenge_id': 35, 'challenge_name': 'aido-LF-sim-testing', 'challenge_is_open': 1,
    #     'user_label': 'baseline-duckietown', 'user_metadata': {}
    # }

    if submission_id is None:
        choices = {}
        results = dtserver_get_user_submissions(token, challenge_name=challenge_name)
        for k, v in results.items():
            if user_label is not None:
                if v["user_label"] != user_label:
                    continue
            if challenge_name is not None:
                if v["challenge_name"] != challenge_name:
                    continue
            choices[int(k)] = v

        if not choices:
            msg = "Cannot find any matching submission"
            raise UserError(msg)

        if len(choices) > 1:
            msg = f"Found more than one matching submission: {list(choices)}. Choosing the first. "
            logger.warning(msg)

        submission_id = list(choices)[0]

    i = 0
    while True:
        try:
            data = dtserver_get_info(token, submission_id)
        except ServerIsDown:
            print(termcolor.colored("Server is down - please wait.", "red"))
            time.sleep(60)
            continue
        except BaseException as e:
            print(termcolor.colored(str(e), "red"))
            time.sleep(60)
            continue
        # print(json.dumps(data, indent=4))

        status_details = data["status-details"]
        if i == 0 and status_details:
            write_status_line(f"Complete: {status_details['complete']}")
            if status_details["complete"]:
                write_status_line(f"Result: {status_details['result']}")

        i += 1
        if status_details is None:
            write_status_line("Not processed yet.")
        else:

            complete = status_details["complete"]
            # result = status_details["result"]
            step2status = status_details["step2status"]
            step2status.pop("START", None)

            step2job = status_details["step2job"]
            for k, v in step2job.items():
                if k not in step2job_seen or step2job_seen[k] != v:
                    step2job_seen[k] = v

                    write_status_line(f'Job "{v}" created for step {k}')

            for k, v in step2status.items():
                if k not in step2status_seen or step2status_seen[k] != v:
                    step2status_seen[k] = v

                    write_status_line(f'Step "{k}" is in state {v}')

            next_steps = status_details["next_steps"]

            # if complete:
            #     msg = 'The submission is complete with result "%s".' % result
            #     print(msg)
            #     break
            cs = []

            if complete:
                cs.append("complete")
            else:
                cs.append("please wait")

            cs.append(f"status: {color_status(status_details['result'])}")

            if step2status:

                for step_name, step_state in step2status.items():
                    cs.append(f"{step_name}: {color_status(step_state)}")

            if next_steps:
                cs.append(f"  In queue: {' '.join(map(str, next_steps))}")

            s = "  ".join(cs)
            write_status_line(s)

            if complete and exit_when_complete:
                result = status_details["result"]
                if result == "success":
                    write_status_line("exiting with 0 because of success")
                    sys.exit(0)
                else:
                    write_status_line(f"exiting with 0 because result = {result}")
                    sys.exit(1)

        time.sleep(30)


class Storage:
    previous = None


def write_status_line(x):
    # print(x)
    # return
    # fancy=  False
    # if fancy:
    #
    #     if x == Storage.previous:
    #         sys.stdout.write("\r" + " " * 80 + "\r")
    #     else:
    #         sys.stdout.write("\n")
    # else:
    #     sys.stdout.write("\n")

    now = datetime.datetime.now()
    n = termcolor.colored(now.isoformat()[-15:-7], "blue", attrs=["dark"])
    s = " - " + n + "   " + x
    print(s)
    # if not fancy:
    #     sys.stdout.write("\n")
    sys.stdout.flush()
    Storage.previous = x


def color_status(x: str):
    status2color = {
        "failed": dict(color="red", on_color=None, attrs=None),
        "error": dict(color="red", on_color=None, attrs=None),
        "success": dict(color="green", on_color=None, attrs=None),
        "evaluating": dict(color="blue", on_color=None, attrs=None),
        "aborted": dict(color="cyan", on_color=None, attrs=["dark"]),
        "timeout": dict(color="cyan", on_color=None, attrs=["dark"]),
    }

    if x in status2color:
        return termcolor.colored(x, **status2color[x])
    else:
        return x
