import os

from pi18n import TranslationService
from telebotify.services.http_client import HttpClient
from telebotify.utils.file_utils import get_resource_path

translation_service = TranslationService(get_resource_path('telebotify.resources', 'i18n'), os.environ.get("LOCALE", "es"))
