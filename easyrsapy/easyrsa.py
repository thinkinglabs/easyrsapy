
class EasyRSA:
    def __init__(self, path):
        self.path = path

    def init_pki(self, pki_dir):
        import subprocess

        cp = subprocess.run(
            [self.path, "--batch", f"--pki-dir={pki_dir}", "init-pki"],
            check=True,
            capture_output=True,
            text=True,
        )
        return cp.stdout
