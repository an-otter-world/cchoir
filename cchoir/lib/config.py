"""Config helpers."""
from pathlib import Path
from socket import gethostname

from OpenSSL.crypto import FILETYPE_PEM
from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA
from OpenSSL.crypto import X509
from OpenSSL.crypto import dump_certificate
from OpenSSL.crypto import dump_privatekey
from appdirs import user_config_dir
from pofy import PathField
from pofy import load

class Config:
    class Schema:
        """Pofy fields."""

        client_certificate = PathField()
        client_key = PathField()

    @staticmethod
    def load() -> 'Config':
        """Loads the user-defined config."""
        config_file_path = Config._get_config_dir() / 'config.yaml'
        if config_file_path.exists():
            config = load(config_file_path, Config)
        else:
            config = Config()
        config.initialize()
        return config

    def __init__(self):
        self.client_certificate: Path = self._get_config_dir() / 'client.cert'
        self.client_key: Path = self._get_config_dir() / 'client.key'

    def initialize(self) -> None:
        self._generate_certificate_if_not_present()

    def _generate_certificate_if_not_present(self) -> None:
        cert_path = self.client_certificate
        key_path = self.client_key

        if cert_path.exists() and key_path.exists():
            return

        cert_path.parent.mkdir(parents=True, exist_ok=True)
        key_path.parent.mkdir(parents=True, exist_ok=True)

        key = PKey()
        key.generate_key(TYPE_RSA, 1024)

        with open(self.client_key, 'wb') as key_file:
            key_bytes = dump_privatekey(FILETYPE_PEM, key)
            key_file.write(key_bytes)

        cert = X509()
        subject = cert.get_subject()
        subject.C = "FR"
        subject.ST = "IDF"
        subject.L = "Paris"
        subject.O = "CCHOIR"
        subject.OU = "CCHOIR"
        subject.CN = gethostname()
        cert.set_issuer(subject)
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)
        cert.set_pubkey(key)
        cert.sign(key, 'sha256')
    
        with open(self.client_certificate, 'wb') as cert_file:
            cert_bytes = dump_certificate(FILETYPE_PEM, cert)
            cert_file.write(cert_bytes)

    @staticmethod
    def _get_config_dir() -> Path:
        return Path(user_config_dir('cchoir'))
