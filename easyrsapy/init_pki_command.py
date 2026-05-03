import subprocess
from typing import NamedTuple


class InitPkiRequest(NamedTuple):
    pki_dir: str


class InitPkiResponse(NamedTuple):
    notice: str
    pki_dir: str


class InitPkiCommand:
    def __init__(self, easy_rsa_path):
        self.easy_rsa_path = easy_rsa_path

    def execute(self, request: InitPkiRequest) -> InitPkiResponse:
        cp = subprocess.run(
            [self.easy_rsa_path, "--batch", f"--pki-dir={request.pki_dir}", "init-pki"],
            check=True,
            capture_output=True,
            text=True,
        )
        return InitPkiResponse(pki_dir=request.pki_dir, notice=cp.stdout)
