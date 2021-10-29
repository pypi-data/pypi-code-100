"""
Application settings
"""


class Default():
    """
    Parameters and settings used by default
    
    Args:
        LOG_PATH: Path to runtime log file
        EXPORT_FORMAT: Format for export file
        EXPORT_PATH: Path to export file
        API_V: Defines which version of vkAPI will be used by app
        FIELDS: Additional user info to get
        CLIENT_ID: App id
        SCOPE: App permissions scope
        RETRIES: requests.Session max retries on error
        BACKOFF: Backoff_factor between retries
        TIMEOUT: Time to wait for response
    """
    LOG_PATH = './logs.log'
    EXPORT_FORMAT = 'csv'
    EXPORT_PATH = './report'
    API_V = '5.131'
    FIELDS = 'bdate,sex,city,country'
    BASE_URL = 'https://api.vk.com/method/'
    CLIENT_ID = 7124393
    SCOPE = 'friends'
    RETRIES = 3
    BACKOFF = 0.5
    TIMEOUT = 5