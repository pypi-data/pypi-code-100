#! /usr/bin/env python
# -*- coding:utf-8 -*-

from . import env
from retry import retry
import traceback
import logging
import pika


class BaseMq(object):
    def __init__(self, options):
        self.options = dict()
        if options: self.options = dict(self.options, **options)

    @staticmethod
    def get_config(**kwargs):
        if 'config' in kwargs:
            conf = kwargs['config']
        else:
            conf = 'queue'
        if 'driver' in kwargs:
            driver = kwargs['driver']
        else:
            driver = env.get(conf + '.driver')
        if not driver: driver = 'Rabbitmq'  # 未定义，默认为rabbitmq
        driver = driver.capitalize()
        return env.get(conf), driver

    def option(self, key, default=None):
        if key.find('.') < 0:
            if key in self.options:
                return self.options[key]
            else:
                return default
        else:
            keys = key.split('.')
            if keys[0] in self.options and keys[1] in self.options[keys[0]]:
                return self.options[keys[0]][keys[1]]
            else:
                return default

    def publish(self, message, *args, **kwargs):
        raise NotImplementedError

    def consume(self, queue, callback, *args, **kwargs):
        raise NotImplementedError


class Rabbitmq(BaseMq):
    def __init__(self, options):
        super().__init__(options)
        self.options = {
            'host': 'localhost',
            'port': 5672,
            'user': 'admin',
            'pass': 'admin',
            'keep_alive': True,  # //保持链接
            'heartbeat': 600,  # //心跳检测
            'prefetch_count': 250,  # //心跳检测
            'vhost': '/',
            'exchange': 'exchange',
            'exchange_type': 'topic',
            'routing_key': None,
            'queue': None,
            'durable': True,  # //消息队列持久化
            'auto_delete': False,
            'auto_declare': False,
            'auto_bind': False,
            'retries': 2,  # //最大消费次数
            'auto_ack': True,  # //自动提交ack

        }
        if options: self.options = dict(self.options, **options)
        self.connection = None

    def init_config(self, **kwargs):
        options = self.options
        if 'exchange' in kwargs:
            options['exchange'] = kwargs['exchange']
        else:
            options['exchange'] = self.option('exchange')

        if 'exchange_type' in kwargs:
            options['exchange_type'] = kwargs['exchange_type']
        else:
            options['exchange_type'] = self.option('exchange_type')

        if 'routing_key' in kwargs:
            options['routing_key'] = kwargs['routing_key']
        else:
            options['routing_key'] = self.option('routing_key')

        if 'queue' in kwargs:
            options['queue'] = kwargs['queue']
        else:
            options['queue'] = self.option('queue')

        if 'durable' in kwargs:
            options['durable'] = kwargs['durable']
        else:
            options['durable'] = self.option('durable')

        if 'retries' in kwargs:
            options['retries'] = kwargs['retries']
        else:
            options['retries'] = self.option('retries')
        options['retries'] = int(options['retries'])

        options['durable'] = str(options['durable'])
        options['durable'] = True if options['durable'].lower() == 'true' or options[
            'durable'].lower() == '1' else False

        if 'auto_declare' in kwargs:
            options['auto_declare'] = kwargs['durable']
        else:
            options['auto_declare'] = self.option('auto_declare')
        options['auto_declare'] = str(options['auto_declare'])
        options['auto_declare'] = True if options['auto_declare'].lower() == 'true' or options[
            'auto_declare'].lower() == '1' else False

        if 'auto_ack' in kwargs:
            options['auto_ack'] = kwargs['auto_ack']
        else:
            options['auto_ack'] = self.option('auto_ack')
        options['auto_ack'] = str(options['auto_ack'])
        options['auto_ack'] = True if options['auto_ack'].lower() == 'true' or options[
            'auto_ack'].lower() == '1' else False

        if 'auto_delete' in kwargs:
            options['auto_delete'] = kwargs['auto_delete']
        else:
            options['auto_delete'] = self.option('auto_delete')
        options['auto_delete'] = str(options['auto_delete'])
        options['auto_delete'] = True if options['auto_delete'].lower() == 'true' or options[
            'auto_delete'].lower() == '1' else False

        if 'auto_bind' in kwargs:
            options['auto_bind'] = kwargs['auto_bind']
        else:
            options['auto_bind'] = self.option('auto_bind')
        options['auto_bind'] = str(options['auto_bind'])
        options['auto_bind'] = True if options['auto_bind'].lower() == 'true' or options[
            'auto_bind'].lower() == '1' else False

        return options

    def channel(self):
        self.conn()
        return self.connection.channel()

    def conn(self):
        if not self.connection or not self.connection.is_open:
            username = self.option('user')
            password = self.option('pass')
            host = self.option('host')
            port = self.option('port')
            vhost = self.option('vhost')
            heartbeat = int(self.option('heartbeat'))
            credentials = pika.PlainCredentials(username=username, password=password)  # mq用户名和密码
            params = pika.ConnectionParameters(host=host, port=port, virtual_host=vhost, credentials=credentials,
                                               heartbeat=heartbeat)
            self.connection = pika.BlockingConnection(params)
            logging.getLogger(__name__).info("Rabbitmq connected.")


class Channel(object):
    def __init__(self, rabbitmq):
        self.rabbitmq = rabbitmq
        self.rabbitmq.conn()
        self.channel = None
        self.options = None
        self.callback = None

    def exchange_declare(self):
        if not self.channel or not self.channel.is_open:
            self.channel = self.rabbitmq.channel()
        if self.options['auto_declare']:
            result = self.channel.exchange_declare(exchange=self.options['exchange'],
                                                   exchange_type=self.options['exchange_type'],
                                                   durable=self.options['durable'])

    def queue_declare(self):
        if not self.channel or not self.channel.is_open:
            self.channel = self.rabbitmq.channel()
        if self.options['auto_declare']:
            result = self.channel.queue_declare(queue=self.options['queue'], durable=self.options['durable'],
                                                auto_delete=self.options['auto_delete'])
        if self.options['auto_bind']:
            result = self.channel.queue_bind(queue=self.options['queue'], exchange=self.options['exchange'],
                                             routing_key=self.options['routing_key'])


class Producer(Channel):
    # @retry(pika.exceptions.AMQPConnectionError, tries=20, delay=1, max_delay=5, jitter=1)
    @retry(exceptions=Exception, tries=20, delay=1, max_delay=5, jitter=1)
    def publish(self, message, *args, **kwargs):
        self.options = self.rabbitmq.init_config(**kwargs)
        self.rabbitmq.conn()
        self.exchange_declare()
        self.queue_declare()
        # 向队列插入数值
        try:
            self.channel.basic_publish(exchange=self.options['exchange'], routing_key=self.options['routing_key'],
                                       body=message)
            self.channel.close()
            self.channel = None
            # 关闭链接
            if not self.options['keep_alive']:
                self.rabbitmq.connection.close()
                self.rabbitmq.connection = None
                self.rabbitmq = None
        except pika.exceptions.ConnectionClosedByBroker:
            pass


class Consumer(Channel):
    __exchange = None
    __routing_key = None
    __queue = None
    __auto_ack = None
    __retries = 0

    @retry(exceptions=Exception, tries=20, delay=1, max_delay=5, jitter=1)
    def consume(self, callback, queue=None, *args, **kwargs):
        self.options = self.rabbitmq.init_config(**kwargs)
        if queue: self.options['queue'] = queue
        self.rabbitmq.conn()
        self.exchange_declare()
        self.queue_declare()
        self.callback = callback
        self.callback = callback

        # 传递到on_message_callback
        Consumer.__exchange = self.options['exchange']
        Consumer.__routing_key = self.options['routing_key']
        Consumer.__queue = self.options['queue']
        Consumer.__auto_ack = self.options['auto_ack']
        Consumer.__retries = self.options['retries']

        prefetch_count = int(self.options['prefetch_count'])

        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.channel.basic_consume(queue=Consumer.__queue, on_message_callback=self.on_message_callback,
                                   auto_ack=Consumer.__auto_ack)

        # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
        logging.getLogger(__name__).info("start_consuming queue=%s" % Consumer.__queue)
        self.channel.start_consuming()

    def on_message_callback(self, ch, method, properties, body):
        message = body.decode()
        headers = properties.headers
        attempts = 0
        committed = False
        if headers and 'attempts' in headers:
            attempts = int(headers['attempts'])
        try:
            res = self.callback(ch, method, properties, message)
        except Exception as e:
            traceback.print_exc()
            logging.getLogger(__name__).error("consume failure.message=>%s error=>%s" % (message, e))
            retries = int(Consumer.__retries)
            if attempts < retries - 1:
                attempts = attempts + 1
                if properties.headers is None: properties.headers = {}
                properties.headers['attempts'] = attempts
                properties.attempts = attempts
                try:
                    self.channel.basic_publish(exchange=Consumer.__exchange,
                                               routing_key=Consumer.__routing_key,
                                               body=message, properties=properties)
                    logging.getLogger(__name__).info("republish message success attempts=>%s" % attempts)
                except Exception as e:
                    # 重新发布失败，不在finally提交ack
                    committed = True
                    logging.getLogger(__name__).error(
                        "republish failure:message=>%s error=>%s" % (message, e))
            # 非自动提交ack才可以执行basic_reject
            elif not Consumer.__auto_ack:
                # 不在finally提交ack
                committed = True
                # requeue=False才会进入死信队列
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                logging.getLogger(__name__).info("basic_reject message success retries=>%s" % retries)
        finally:
            # 手动提交ack
            if not Consumer.__auto_ack and not committed:
                try:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    logging.getLogger(__name__).info("basic_ack message success")
                except Exception as e:
                    logging.getLogger(__name__).error("commit ack failure:%s" % e)


class MqException(Exception):
    pass
