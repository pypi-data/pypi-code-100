import os
import pytest

from vkinfo.vk_api import VkApiSess
from vkinfo.config import Default


@pytest.fixture
def vk():
    """create session fixture"""

    token = os.environ.get('ACCESS_TOKEN') or "BANBANBANBA"
    vk = VkApiSess(access_token=token,
                   api_version=Default.API_V,
                   app_id=Default.CLIENT_ID,
                   base_url=Default.BASE_URL)
    return vk
