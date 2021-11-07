import copy
import pickle
from typing import Union

STATE_KEY = 'state'
STATE_DATA_KEY = 'data'
STATE_BUCKET_KEY = 'bucket'


class BaseStorage:
    def set_state(self, key, state: Union[str, int]):
        raise NotImplementedError

    def get_state(self, key):
        raise NotImplementedError

    def update_data(self, key, data: dict):
        raise NotImplementedError

    def resolve(self, key, state=None):
        raise NotImplementedError

    def get_record(self, key):
        raise NotImplementedError

    def get_data(self, key):
        raise NotImplementedError

    def finish(self, key, clear=False):
        raise NotImplementedError

    def get_bucket(self, key):
        raise NotImplementedError

    def set_bucket(self, key, bucket: dict):
        raise NotImplementedError

    def update_bucket(self, key, bucket: dict):
        raise NotImplementedError


class MemoryStorage(BaseStorage):

    def __init__(self):
        self._current_states = {}

    def set_state(self, key, state: Union[str, int]):
        if isinstance(state, int):
            state = str(state)
        if key in self._current_states:
            self._current_states[key][STATE_KEY] = state
        else:
            self.resolve(key, state)

    def get_state(self, key):
        try:
            return self._current_states[key][STATE_KEY]
        except KeyError:
            self.resolve(key)
            return None

    def update_data(self, key, data: dict):
        self._current_states[key][STATE_DATA_KEY].update(data)

    def resolve(self, key, state=None):
        data = {}
        if state:
            data[STATE_KEY] = state
        else:
            data[STATE_KEY] = None
        data.update({STATE_DATA_KEY: {}, STATE_BUCKET_KEY: {}})
        self._current_states[key] = data

    def finish(self, key, clear=False):
        if clear:
            del self._current_states[key]
        else:
            self._current_states[key] = dict(state=None, data={})

    def get_record(self, key):
        if key in self._current_states:
            return copy.deepcopy(self._current_states[key])
        else:
            self.resolve(key)
            return {STATE_KEY: {}, STATE_DATA_KEY: {}, STATE_BUCKET_KEY: {}}

    def get_data(self, key):
        record = self.get_record(key)
        return copy.deepcopy(record[STATE_DATA_KEY])

    def get_bucket(self, key):
        record = self.get_record(key)
        return copy.deepcopy(record[STATE_BUCKET_KEY])

    def set_bucket(self, key, bucket: dict):
        record = self.get_record(key)
        record[STATE_BUCKET_KEY] = bucket
        self._current_states[key] = record

    def update_bucket(self, key, bucket: dict):
        record = self.get_record(key)
        record[STATE_BUCKET_KEY].update(bucket)
        self._current_states[key] = record


class RedisStorage(BaseStorage):

    def __init__(self, host: str = "localhost", port: int = 6379, db=0, prefix="djbot"):
        from redis import Redis, ConnectionPool
        self.redis = Redis(connection_pool=ConnectionPool(host=host, port=port, db=db))
        self.prefix = prefix

    def _key(self, key):
        return ':'.join((self.prefix, str(key)))

    def set_state(self, key, state: Union[str, int]):
        key = self._key(key)
        if isinstance(state, int):
            state = str(state)
        if self.redis.exists(key):
            data = pickle.loads(self.redis.get(key))
            data[STATE_KEY] = state
            self.redis.set(key, pickle.dumps(data))
        else:
            self.resolve(key, state)

    def resolve(self, key, state=None):
        data = {}
        if state:
            data[STATE_KEY] = state
        else:
            data[STATE_KEY] = None
        data.update({STATE_DATA_KEY: {}, STATE_BUCKET_KEY: {}})
        self.redis.set(key, pickle.dumps(data))

    def get_state(self, key):
        key = self._key(key)
        if self.redis.exists(key):
            return pickle.loads(self.redis.get(key))[STATE_KEY]
        else:
            self.resolve(key)
            return None

    def get_record(self, key):
        key = self._key(key)
        if self.redis.exists(key):
            return pickle.loads(self.redis.get(key))
        else:
            self.resolve(key)
            return {STATE_KEY: None, STATE_DATA_KEY: {}, STATE_BUCKET_KEY: {}}

    def get_data(self, key):
        record = self.get_record(key)
        return record[STATE_DATA_KEY]

    def update_data(self, key, data: dict):
        record = self.get_record(key)
        record[STATE_DATA_KEY].update(data)
        self.redis.set(self._key(key), pickle.dumps(record))

    def finish(self, key, clear=False):
        key = self._key(key)
        if clear:
            self.redis.delete(key)
        else:
            self.resolve(key)

    def get_bucket(self, key):
        record = self.get_record(key)
        return record[STATE_BUCKET_KEY]

    def set_bucket(self, key, bucket: dict):
        record = self.get_record(key)
        record[STATE_BUCKET_KEY] = bucket
        self.redis.set(self._key(key), record)

    def update_bucket(self, key, bucket: dict):
        record = self.get_record(key)
        record[STATE_BUCKET_KEY].update(bucket)
        self.redis.set(self._key(key), pickle.dumps(record))


class FileStorage(BaseStorage):

    def resolve(self, key, state=None):
        pass

    def get_data(self, key):
        pass

    def set_state(self, key, state: Union[str, int]):
        pass

    def get_state(self, key):
        pass

    def update_data(self, key, data: dict):
        pass

    def get_record(self, key):
        pass

    def finish(self, key, clear=False):
        pass

    def get_bucket(self, key):
        pass

    def set_bucket(self, key, bucket: dict):
        pass

    def update_bucket(self, key, bucket: dict):
        pass
