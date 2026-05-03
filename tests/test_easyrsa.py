import textwrap

from .context import easyrsapy  # noqa: F401
from easyrsapy.easyrsa import EasyRSA

EASYRSA_PATH = "/opt/homebrew/bin/easyrsa"


def test_init_pki():
    expected = """
                  Notice
                  ------
                  'init-pki' complete; you may now create a CA or requests.
                  
                  Your newly created PKI dir is:
                  * /tmp/test_pki
                  
                  """  # noqa: W293
    easyrsa = EasyRSA(EASYRSA_PATH)
    actual = easyrsa.init_pki("/tmp/test_pki")
    assert textwrap.dedent(expected) == actual
