import textwrap

from .context import easyrsapy  # noqa: F401
from easyrsapy.init_pki_command import InitPkiCommand, InitPkiRequest


def teardown_function():
    # clean up the pki dir after each test
    import shutil

    shutil.rmtree("/tmp/pki", ignore_errors=True)


def test_init_pki():
    expected = """
                  Notice
                  ------
                  'init-pki' complete; you may now create a CA or requests.
                  
                  Your newly created PKI dir is:
                  * /tmp/pki

                  """  # noqa: W293
    pki_dir = "/tmp/pki"
    command = InitPkiCommand(easy_rsa_path="easyrsa")
    request = InitPkiRequest(pki_dir=pki_dir)
    response = command.execute(request)
    actual = response.notice
    assert textwrap.dedent(expected) in actual
    assert pki_dir == response.pki_dir
