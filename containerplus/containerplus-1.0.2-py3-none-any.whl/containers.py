from typing import Iterable, Any
from .errors import StackEmptyException, QueueEmptyException

__all__ = [
  "Queue", "Stack"
]

class Queue(list):
  def __init__(self, _: Iterable = []):
    super(Queue, self).__init__(_)

  def __getattribute__(self, name):
    if name in ['append', 'index', 'remove']:
      raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    return super(list, self).__getattribute__(name)

  def enqueue(self, item: Any):
    """Add an item to the beginning of the queue."""
    self.insert(0, item)

    return self

  def dequeue(self):
    """Removes the topmost item in the queue and returns it."""
    try:
      return self.pop(len(self) - 1)
    except:
      raise QueueEmptyException("Queue is empty")

  def peek(self):
    """Returns the topmost item in the queue without removing it."""
    try:
      return self[len(self) - 1]
    except:
      raise QueueEmptyException("Queue is empty")

  @property
  def empty(self):
    """A boolean property indicating whether the queue is empty or not."""
    return len(self) == 0

  def __iter__(self):
    for i in self.__reversed__():
      yield i

  def extend(self, iterable: Iterable):
    for i in iterable:
      self.enqueue(i)

class Stack(list):
  def __init__(self, _: Iterable = []):
    super(Stack, self).__init__(_)
    self._representation = _

  def __getattribute__(self, name):
    if name in ['append', 'index', 'remove']:
      raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    return super(list, self).__getattribute__(name)

  def push(self, item: Any):
    """Add an item to the end of the stack."""
    self.append(item)
    self._representation.append(item)

    return self

  def pop(self):
    """Removes the last added item in the list and returns it."""
    try:
      self._representation.pop(len(self) - 1)
      return self.pop(len(self) - 1)
    except:
      raise StackEmptyException("Stack is empty")

  def peek(self):
    """Returns the topmost item in the stack without removing it."""
    try:
      return self[len(self) - 1]
    except:
      raise StackEmptyException("Stack is empty")

  @property
  def empty(self):
    """A boolean property indicating whether the stack is empty or not."""
    return len(self) == 0

  def search(self, o: Any) -> int:
    """Returns the 1-based position where an object is on this stack. If the object o occurs as an item in this stack, this method returns the distance from the top of the stack of the occurrence nearest the top of the stack; the topmost item on the stack is considered to be at distance 1. The equals method is used to compare o to the items in this stack."""

    index = 0

    for i in self.__reversed__():
      index += 1
      if o == i:
        return index

    return -1

  def __iter__(self):
    for i in self.__reversed__():
      yield i

  def __repr__(self):
    return f"<Stack {self._representation}>"

  def extend(self, iterable: Iterable):
    for i in iterable:
      self.push(i)