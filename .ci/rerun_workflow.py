import json
from os import environ
from sys import exit
from urllib import request


def get_runs():
    req = request.Request(url="https://api.github.com/repos/microsoft/LightGBM/actions/workflows/test_main.yml/runs",
                          headers={"accept": "application/vnd.github.v3+json"})
    with request.urlopen(req) as url:
        data = json.loads(url.read().decode())
    pr_runs = [i for i in data['workflow_runs']
               if i['event'] == 'pull_request' and
               (i.get('pull_requests') and
                i['pull_requests'][0]['number'] == int(environ.get("GITHUB_REF").split('/')[-2]) or
                i['head_branch'] == environ.get("GITHUB_HEAD_REF").split('/')[-1])]
    return sorted(pr_runs, key=lambda i: i['run_number'], reverse=True)


def rerun_workflow(runs):
    if runs:
        req = request.Request(url="https://api.github.com/repos/microsoft/LightGBM/actions/runs/{}/rerun".format(runs[0]["id"]),
                              headers={"accept": "application/vnd.github.v3+json"})
        try:
            if request.urlopen(req).getcode() != 201:
                exit(1)
        except Exception:
            exit(1)


if __name__ == "__main__":
    status = rerun_workflow(get_runs())