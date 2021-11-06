from gevent.pool import Pool as BasePoll
import gevent.monkey
gevent.monkey.patch_all()


class Pool(BasePoll):
    '''routine pool'''

    def apply_async(self, func, args=None, kwds=None, callback=None):
        return BasePoll().apply_async(func, args=(), kwds={}, callback=callback)

    def close(self):
        pass
