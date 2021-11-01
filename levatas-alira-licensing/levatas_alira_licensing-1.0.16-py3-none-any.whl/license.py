import os
import logging
import json

from cryptography import x509
from datetime import datetime
from pathlib import Path
from alira_licensing.certificate_validation import CertificateValidation

logger = logging.getLogger(__name__)


METADATA_EXTENSION_OID = x509.ObjectIdentifier("1.2.3.4.5.6.7.8.9.10")


def verify(
    directory=Path(os.path.abspath("")),
    current_datetime=datetime.utcnow()
):
    try:
        cert_validator = CertificateValidation()
        public_key = cert_validator.read_public_key_text(_get_public_key(directory))
        certificate = cert_validator.read_certificate_file(
            os.path.join(directory, "license.pem")
        )

        is_valid = cert_validator.verify_levatas_certificate(
            "Alira Platform", public_key, certificate, current_datetime
        )

        metadata = json.loads(
            certificate.extensions.get_extension_for_oid(
                METADATA_EXTENSION_OID
            ).value.value.decode("utf-8")
        )

        return {
            "not_valid_before": certificate.not_valid_before,
            "not_valid_after": certificate.not_valid_after,
            "metadata": metadata,
            "active": is_valid,
        }
    except Exception as e:
        logger.exception("There was an error processing the license.")

        return {
            "not_valid_before": None,
            "not_valid_after": None,
            "metadata": None,
            "active": False,
        }

def _get_public_key(directory):
    with open(os.path.join(directory, "public_key"), "r") as stream:
        return stream.read()


