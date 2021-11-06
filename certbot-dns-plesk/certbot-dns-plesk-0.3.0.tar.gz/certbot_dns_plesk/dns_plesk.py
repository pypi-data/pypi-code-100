"""DNS Authenticator for plesk."""

import logging

from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon

from lexicon.config import ConfigResolver
from lexicon.providers import plesk

logger = logging.getLogger(__name__)


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for plesk."""

    description = (
        "Obtain certificates using a DNS TXT record by using the plesk dns api."
    )

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=30)
        add("credentials", help="plesk dns credentials ini file.")

    def more_info(self):
        return """
            This plugin configures a DNS TXT record to respond to a dns-01 challenge using
            the plesk DNS API
            """

    def _setup_credentials(self):
        dns_common.validate_file_permissions(self.conf('credentials'))
        self.credentials = self._configure_credentials(
            'credentials',
            'plesk dns credentials ini file',
            {
                'username': 'Plesk API username',
                'password': 'Plesk API password',
                'api_url': 'URL to the Plesk Web UI, including the port (e.g. http://host:port)'
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_plesk_client(domain).add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_plesk_client(domain).del_txt_record(domain, validation_name, validation)

    def _get_plesk_client(self, domain):
        return _PleskLexiconClient(
            self.credentials.conf('username'),
            self.credentials.conf('password'),
            self.credentials.conf('api_url'),
            domain
        )


class _PleskLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with plesk API via Lexicon.
    """

    def __init__(self, username, password, api_url, domain):
        super(_PleskLexiconClient, self).__init__()

        config = {
            'provider_name': 'plesk',
            'domain': domain,
            'plesk': {
                'auth_username': username,
                'auth_password': password,
                'plesk_server': api_url,
            },
        }

        lexicon_config = ConfigResolver().with_dict(config)
        self.provider = plesk.Provider(lexicon_config)

    def _handle_general_error(self, e, domain_name):
        if 'Site does not exist' in str(e):
            return # There might no be a dedicated site for a given subdomain. Let LexiconClient.__find_domain_id do it's job
        return super(_PleskLexiconClient, self)._handle_general_error(e, domain_name)

    def _handle_http_error(self, e, domain_name):
        if domain_name in str(e) and str(e).startswith('422 Client Error: Unprocessable Entity for url:') :
            return  # Expected errors when zone name guess is wrong
        return super(_PleskLexiconClient, self)._handle_http_error(e, domain_name)

