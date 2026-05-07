import re
import subprocess
from typing import NamedTuple


class BuildCARequest(NamedTuple):
    req_cn: str
    env_var_ca_cert_pwd: str
    pki_dir: str


class BuildCAResponse(NamedTuple):
    ca_path: str


class BuildCACommand:
    def __init__(self, parser: BuildCAStdOutParser, easy_rsa_path: str):
        self.parser = parser
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
        print(cp.stdout)
        return self.parser.parse(cp.stdout)


class BuildCAStdOutParser:
    """
    Parses the stdout notice from the 'build-ca' command to extract the CA certificate path.

    Example stdout notice:
    ---
    Notice
    ------
    CA creation complete. Your new CA certificate is at:
    * /tmp/pki/ca.crt

    Build-ca completed successfully.

    ---
    """

    def parse(self, notice: str) -> BuildCAResponse:
        pattern = re.compile(r"^\*\s*(?P<path>(/[a-zA-Z0-9-_]+)*/ca\.crt)$")
        lines = notice.splitlines()
        ca_path = None
        for line in lines:
            match = pattern.match(line)
            if match:
                ca_path = match.group("path")
                break
        return BuildCAResponse(ca_path=ca_path)
