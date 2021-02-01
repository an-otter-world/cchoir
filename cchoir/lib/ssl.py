"""Various helpers to deal with OpenSSL certificates & keys."""
from pathlib import Path
from random import randrange
from socket import gethostname

from OpenSSL import crypto
from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA
from OpenSSL.crypto import X509
from OpenSSL.crypto import dump_certificate
from OpenSSL.crypto import dump_privatekey
from OpenSSL.crypto import FILETYPE_PEM


def gen_certificate(key_path: Path, cert_path: Path, size: int) -> None:
    """Generate and save a key / certificate pair at the given locations.

    Args:
        key_path: Destination file for the certificate key.
        cert_path: Destination file for the certificate.
        size: Certificate key size, in bytes.

    """
    pkey = PKey()
    pkey.generate_key(TYPE_RSA, size)

    x509 = X509()
    subject = x509.get_subject()
    subject.commonName = gethostname()
    x509.set_issuer(subject)
    x509.gmtime_adj_notBefore(0)
    x509.gmtime_adj_notAfter(5 * 365 * 24 * 60 * 60)
    x509.set_pubkey(pkey)
    x509.set_serial_number(randrange(100000))
    x509.set_version(2)
    x509.add_extensions([
        crypto.X509Extension(b"basicConstraints", True, b"CA:false")
    ])
    x509.sign(pkey, 'SHA256')

    with open(key_path, 'wb') as key_file:
        key_content = dump_privatekey(FILETYPE_PEM, pkey)
        key_file.write(key_content)

    with open(cert_path, 'wb') as cert_file:
        cert_content = dump_certificate(FILETYPE_PEM, x509)
        cert_file.write(cert_content)
