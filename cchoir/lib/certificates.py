"""Certificate management helpers."""
from pathlib import Path
from typing import Tuple

from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA
from OpenSSL.crypto import X509
from OpenSSL.crypto import dump_certificate
from OpenSSL.crypto import dump_privatekey

from appdirs import user_config_dir

from cchoir.lib.config import config_file_path

def get_certificates() -> Tuple[Path, Path]:
    cert_path, key_path = _get_certificate_paths()

    if not cert_path.exists() or not key_path.exists():
        _generate_certificate(cert_path, key_path)

    assert cert_path.exists() and key_path.exists()

def _get_certificate_paths() -> Tuple[Path, Path]:
    cert_path = config_file_path('client.crt')
    key_path = config_file_path('client.key')

    return (cert_path, key_path)

def _generate_certificate():
    cert_path, key_path = _get_certificate_paths()

    key = PKey()
    key.generate_key(TYPE_RSA, 1024)

    with open(key_path, 'w') as key_file:
        dump_privatekey(FILETYPE_PEM, key)

    cert = X509()
    cert.set_pubkey(key)
    cert.sign(key, 'sha1')
 
    with open(cert_path, 'w') as cert_file:
        dump_certificate(FILETYPE_PEM, cert)
