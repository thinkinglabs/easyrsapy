import textwrap

from .context import easyrsapy  # noqa: F401
from easyrsapy.init_pki_command import InitPkiCommand, InitPkiRequest, InitPkiStdOutParser


def teardown_function():
    # clean up the pki dir after each test
    import shutil

    shutil.rmtree("/tmp/pki", ignore_errors=True)


def test_init_pki():
    pki_dir = "/tmp/pki"
    parser = InitPkiStdOutParser()
    command = InitPkiCommand(parser=parser, easy_rsa_path="easyrsa")
    request = InitPkiRequest(pki_dir=pki_dir)
    response = command.execute(request)
    assert pki_dir == response.pki_dir


def test_init_pki_parser():
    parser = InitPkiStdOutParser()
    notice = """
             Notice
             ------
             'init-pki' complete; you may now create a CA or requests.
                  
             Your newly created PKI dir is:
             * /tmp/pki
             """  # noqa: W293
    response = parser.parse(textwrap.dedent(notice))
    assert response.pki_dir == "/tmp/pki"
