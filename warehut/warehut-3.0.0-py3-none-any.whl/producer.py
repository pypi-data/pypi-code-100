from multiprocessing import Value
from functools import cache

from typing import Any, Sequence

from .worker import Worker
from .consumer import Consumer
from .packet import Packet



class Producer(Worker):
    """Generic producer class"""
    
    consumers: list[Consumer]


    def __init__(self, consumers: list[Consumer]):
        super().__init__()
        self.consumers = consumers
        

    def forward(self, event: str, data: Any):
        """Insert data into the queues of consumers
        with event listeners of the specified event type
        
        Data must be pickleable
        """

        packet = Packet(event, data)
        for queue in self._get_queues(event):
            queue.put(packet)

    @cache
    def _get_queues(self, event: str):
        """Get all queues of consumers that have
        an event listener of the specified event type
        """
        return tuple(consumer.queue for consumer in self.consumers
                        if event in consumer.listeners.keys())


    async def update(self):
        """Generate data and forward packets to consumers"""
        raise NotImplementedError()

    async def _mainloop(self):
        while self.status.value:
            await self.update()