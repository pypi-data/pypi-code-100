import logging

from ruteni import configuration

logger = logging.getLogger(__name__)

configuration.add_static_resource_mount("blaze", __name__)

logger.info("loaded")
