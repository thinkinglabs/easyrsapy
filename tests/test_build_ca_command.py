import os
import textwrap

from .context import easyrsapy  # noqa: F401
from easyrsapy.build_ca_command import (
    BuildCACommand,
    BuildCARequest,
    BuildCAStdOutParser,
)
from easyrsapy.init_pki_command import (
    InitPkiCommand,
    InitPkiRequest,
    InitPkiStdOutParser,
)


def setup_function():
    pki_dir = "/tmp/pki"
    parser = InitPkiStdOutParser()
    command = InitPkiCommand(parser=parser, easy_rsa_path="easyrsa")
    request = InitPkiRequest(pki_dir=pki_dir)
    command.execute(request)


def teardown_function():
    # clean up the pki dir after each test
    import shutil

    shutil.rmtree("/tmp/pki", ignore_errors=True)


def test_build_ca():
    expected = "/tmp/pki/ca.crt"
    pki_dir = "/tmp/pki"
    os.environ["EASYRSA_CA_PWD"] = "test123"
    parser = BuildCAStdOutParser()
    command = BuildCACommand(parser=parser, easy_rsa_path="easyrsa")
    request = BuildCARequest(
        req_cn="Test CA", env_var_ca_cert_pwd="EASYRSA_CA_PWD", pki_dir=pki_dir
    )
    response = command.execute(request)
    actual = response.ca_path
    assert textwrap.dedent(expected) in actual


def test_build_ca_parser():
    parser = BuildCAStdOutParser()
    notice = """
             Notice
             ------
             CA creation complete. Your new CA certificate is at:
             * /tmp/pki/ca.crt

             Build-ca completed successfully.

             """  # noqa: W293
    response = parser.parse(textwrap.dedent(notice))
    assert response.ca_path == "/tmp/pki/ca.crt"
