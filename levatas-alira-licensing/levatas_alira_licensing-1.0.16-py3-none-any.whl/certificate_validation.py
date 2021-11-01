import datetime
import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography import x509
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class CertificateValidation:
    """
    Facilitates the loading and validation of SSL certificates.
    """

    def read_public_key_text(self, text):
        text_bytes = bytearray(text, "utf-8")
        return load_pem_public_key(text_bytes, backend=default_backend())

    def read_public_key_file(self, filename):
        """
        Loads an RSA Public Key from a file.
        
        :param filename: Path to file
        """
        
        with open(filename, "rb") as key_file:
            return load_pem_public_key(key_file.read(), backend=default_backend())

    def read_certificate_file(self, filename):
        """
        Load a Certificate from a file.
        
        :param filename: Path to file
        """
        
        with open(filename, "rb") as cert_file:
            return load_pem_x509_certificate(cert_file.read(), backend=default_backend())

    def verify_certificate_basic(self, public_key, x509_cert, verify_dates=True, current_datetime=datetime.datetime.utcnow()):
        """
        Verify that the Certificate came from the provided Public Key and that 
        the current time is between not_valid_before and not_valid_after.
        
        :param public_key: Public Key
        :param x509_cert: Certificate
        :param verify_dates: Run Validation on the Date Ranges for the Certificate
        """
        
        try:
            public_key.verify(
                x509_cert.signature,
                x509_cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                x509_cert.signature_hash_algorithm,
            )
            
            if verify_dates:
                are_dates_valid = x509_cert.not_valid_before < current_datetime and x509_cert.not_valid_after > current_datetime
                
                return are_dates_valid
            else:
                return True
        except InvalidSignature as err:
            logging.exception("There was an error verifying the certificate")
            return False

    def create_expected_levatas_attributes(self, organizational_unit_name):
        """
        Creates a list of issuer attributes we expect to see in a Levatas-generated Certificate.
        
        :param organizational_unit_name: Purpose of the Certificate
        """
        
        return [
            { "oid": NameOID.COUNTRY_NAME, "name": "Country", "expected": u"US" },
            { "oid": NameOID.STATE_OR_PROVINCE_NAME, "name": "State", "expected": u"Florida" },
            { "oid": NameOID.LOCALITY_NAME, "name": "City", "expected": u"West Palm Beach" },
            { "oid": NameOID.ORGANIZATION_NAME, "name": "Organization", "expected": u"Levatas" },
            { "oid": NameOID.ORGANIZATIONAL_UNIT_NAME, "name": "Organizational Unit", "expected": organizational_unit_name }
        ]
        
    def verify_levatas_certificate(self, organizational_unit_name, public_key, x509_cert, current_datetime=None):
        """
        Verifies the validity of a Levatas Certificate for the purposes provided.
        
        :param organizational_unit_name: Purpose of the Certificate
        :param public_key: Public Key
        :param x509_cert: Certificate
        """
        
        if self.verify_certificate_basic(public_key=public_key, x509_cert=x509_cert, current_datetime=current_datetime):
            exptected_attrs = self.create_expected_levatas_attributes(organizational_unit_name)
            
            for expected_attr in exptected_attrs:
                for value in x509_cert.issuer.get_attributes_for_oid(expected_attr["oid"]):
                    if value.value != expected_attr["expected"]:
                        return False
            
            return True
        else:
            return False

    def display_certificate_details(self, organizational_unit_name, public_key, x509_cert):
        """
        Sending logs about each attribute of the certificate and whether or not it is valid or invalid.

        This is for debugging purposes to provide insight into when the validation fails.

        :param organizational_unit_name: Purpose of the Certificate
        :param x509_cert: Certificate
        """

        if self.verify_certificate_basic(public_key=public_key, x509_cert=x509_cert, verify_dates=False):
            logging.info("Certificate Matches Public Key")
        else:
            logging.info("Certificate Does Not Match Public Key")

        for expected_attr in self.create_expected_levatas_attributes(organizational_unit_name):
            for value in x509_cert.issuer.get_attributes_for_oid(expected_attr["oid"]):
                if value.value == expected_attr["expected"]:
                    logging.info("{0:20s}: '{1:s}' [VALID]".format(expected_attr["name"], value.value))
                else:
                    logging.info("{0:20s}: '{1:s}' [INVALID: Expected '{2:s}']".format(
                        expected_attr["name"], value.value, expected_attr["expected"]))
                    
        utcnow = datetime.datetime.utcnow()
        date_valid = x509_cert.not_valid_before < utcnow and x509_cert.not_valid_after > utcnow
        date_valid_str = "VALID" if date_valid else "INVALID"
        logging.info("{0:20s}: {1:s} through {2:s} [{3:s}]".format("Valid Date Range", 
            str(x509_cert.not_valid_before), str(x509_cert.not_valid_after), date_valid_str))
