import sys
import asyncio
import aiohttp
import json
from . import async_safe_requests
from . import logger_pack
from . import db_pack
from . import services_pack
import traceback
import os

class AsyncParserApp:
    def __init__(self,config_dir=None):
        if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
            policy = asyncio.WindowsSelectorEventLoopPolicy()
            asyncio.set_event_loop_policy(policy)

        self.initConfig(config_dir)
        self.logger = logger_pack.get_logger(self.config['source'])
        # self.proxy_dispatcher = proxy_pack.ProxyDispatcher(self.config["channel"], self.config["source"])
        self.db = db_pack.Database(out_conn_config=self.config["out_conn"],
                                   monitoring_conn_config=self.config["monitoring_conn"],
                                   monitoring_source_name=self.config["source"],
                                   logger=self.logger)

        self.safe_requests=None
        self.services=None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.asyncInit())

    def initConfig(self,config_dir):
        if config_dir is None:
            dirname = os.getcwd()
            config_dir = os.path.join(dirname, 'config.json')

        if not os.path.exists(config_dir):
            raise Exception(f"Config file directory does not exist: {config_dir}")

        required_keys = [
            "out_conn",
            "monitoring_conn",
            "channel",
            "source",
        ]

        self.config = self.get_config_from_json(config_dir)

        if 'debug_mode' not in self.config:
            self.config['debug_mode'] = False

        # Ignored keys on debug mode
        if self.config['debug_mode']:
            if 'out_conn' not in self.config:
                self.config['out_conn'] = None
            if 'monitoring_conn' not in self.config:
                self.config['monitoring_conn'] = None

        self.check_config_keys(required_keys)

    def __del__(self):
        if hasattr(self, 'loop'):
            self.loop.run_until_complete(self.asyncDel())


    async def asyncInit(self):
        self.session = aiohttp.ClientSession()
        self.safe_requests = async_safe_requests.AsyncSafeRequests(
            session=self.session,
            logger=self.logger,
            ATTEMPTS=5,
            ATTEMPT_DELAY=3,
            proxy_channel=self.config['channel'],
            proxy_source=self.config['source'],
            )
        self.services = services_pack.Services(app=self)


    async def asyncDel(self):
        await self.session.close()


    def get_config_from_json(self,config_dir):
        with open(config_dir, 'r') as f:
            config = json.loads(f.read())
        return config

    def check_config_keys(self,required_keys):
        for key in self.config:
            if key in required_keys:
                required_keys.remove(key)

        if required_keys:
            raise Exception("Add following keys to config file: "+", ".join(required_keys))

    def log_config(self):
        config_log_text="CONFIG:\n"+"\n".join([f"{key}: {self.config[key]}" for key in self.config])
        self.logger.info(config_log_text)

    def debug_run(self,main):
        try:
            self.log_config()
            self.logger.info('Parser started in DEBUG MODE')

            self.loop.run_until_complete(main())

            self.logger.info('Parser finished in DEBUG MODE')
        except Exception as e:
            self.logger.error(e, traceback.format_exc())

    def prod_run(self,main):
        try:
            self.log_config()
            monitoring_status = self.db.getParserStatus()[0]
            if monitoring_status is None:
                self.logger.info('Parser already in progress')

            elif not monitoring_status:
                self.logger.info('Parser started')
                self.db.updateParserStatus(None)

                self.loop.run_until_complete(main())

                self.db.updateParserStatus(True)
                self.logger.info('Parser finished')
            else:
                self.logger.info('Information parsed before')
        except Exception as e:
            self.logger.error(e, traceback.format_exc())
            self.db.updateParserStatus(False)

    def run(self,main):
        if self.config['debug_mode']:
            self.debug_run(main)
        else:
            self.prod_run(main)
