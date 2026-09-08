import logging
import os
import sys

import certifi
from PySide6.QtWidgets import QApplication

from src.gui.main_window import MainWindow

logger = logging.getLogger(__name__)

"""
Building the binary on GitHub Actions causes a certificate error to appear because it
bundles the certificates for that specific machine which does not work on all
environemnts
"""


def configure_ssl_certs():
    system_paths = [
        "/etc/ssl/certs/ca-certificates.crt",
        "/etc/pki/tls/certs/ca-bundle.crt",
        "/etc/ssl/ca-bundle.pem",
        "/etc/pki/tls/cacert.pem",
        "/etc/ssl/cert.pem",
    ]
    # Try host system CA stores first
    logger.debug("Checking for valid local certificates")
    for path in system_paths:
        if os.path.exists(path):
            os.environ["SSL_CERT_FILE"] = path
            logger.info("Found local certificate")
            return

    # 2. Fall back to bundled certifi if host system has no detectable CA store
    os.environ["SSL_CERT_FILE"] = certifi.where()
    logger.info("Local certificate not found, falling back to certifi")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    configure_ssl_certs()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
