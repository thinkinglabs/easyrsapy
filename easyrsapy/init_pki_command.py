import re
import subprocess
from typing import NamedTuple


class InitPkiRequest(NamedTuple):
    pki_dir: str


class InitPkiResponse(NamedTuple):
    pki_dir: str


class InitPkiCommand:
    def __init__(self, parser: InitPkiStdOutParser, easy_rsa_path: str):
        self.parser = parser
        self.easy_rsa_path = easy_rsa_path

    def execute(self, request: InitPkiRequest) -> InitPkiResponse:
        args = [
            self.easy_rsa_path,
            "--batch",
            f"--pki-dir={request.pki_dir}",
            "init-pki",
        ]
        cp = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
        )
        print(cp.stdout)
        return self.parser.parse(cp.stdout)


class InitPkiStdOutParser:
    """
    Parses the stdout output of the 'init-pki' command to extract the pki_dir.

    Example stdout output:
    ---
    Notice
    ------
    'init-pki' complete; you may now create a CA or requests.

    Your newly created PKI dir is:
    * /tmp/pki
    ---
    """

    def parse(self, response: str) -> InitPkiResponse:
        pattern = re.compile(r"^\*\s*(?P<path>(/[a-zA-Z0-9-_]+)+|/)$")
        lines = response.splitlines()
        pki_dir = None
        for line in lines:
            match = pattern.match(line)
            if match:
                pki_dir = match.group("path")
                break
        return InitPkiResponse(pki_dir=pki_dir)
