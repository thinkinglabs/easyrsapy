import os
import textwrap

from .context import easyrsapy  # noqa: F401
from easyrsapy.build_ca_command import BuildCACommand, BuildCARequest


def test_build_ca():
    expected = """
                  Notice
                  ------
                  CA creation complete. Your new CA certificate is at:
                  * /tmp/pki/ca.crt

                  Build-ca completed successfully.

                  """  # noqa: W293
    pki_dir = "/tmp/pki"
    os.environ["EASYRSA_CA_PWD"] = "test123"
    command = BuildCACommand(easy_rsa_path="easyrsa")
    request = BuildCARequest(req_cn="Test CA", env_var_ca_cert_pwd="EASYRSA_CA_PWD", pki_dir=pki_dir)
    response = command.execute(request)
    actual = response.notice
    assert textwrap.dedent(expected) in actual
