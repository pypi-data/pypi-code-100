from extras.plugins import PluginConfig


class SLMConfig(PluginConfig):
    name = 'netbox_slm'
    verbose_name = 'Software Lifecycle Management Netbox Plugin'
    description = 'Software Lifecycle Management Netbox Plugin'
    version = '0.1'
    author = 'Hedde van der Heide'
    author_email = 'hedde.vanderheide@ictu.nl'
    base_url = 'software-lifecycle-management'
    required_settings = []
    default_settings = {
        'version_info': False
    }

config = SLMConfig