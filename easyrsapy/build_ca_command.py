import subprocess
from typing import NamedTuple


class BuildCARequest(NamedTuple):
    req_cn: str
    env_var_ca_cert_pwd: str
    pki_dir: str


class BuildCAResponse(NamedTuple):
    notice: str


class BuildCACommand:
    def __init__(self, easy_rsa_path):
        self.easy_rsa_path = easy_rsa_path

    def execute(self, request: BuildCARequest) -> BuildCAResponse:
        args = [
            self.easy_rsa_path,
            "--batch",
            f"--passin=env:{request.env_var_ca_cert_pwd}",
            f"--passout=env:{request.env_var_ca_cert_pwd}",
            f"--pki-dir={request.pki_dir}",
            f"--req-cn={request.req_cn}",
            "build-ca",
        ]
        cp = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
        )
        return BuildCAResponse(notice=cp.stdout)
