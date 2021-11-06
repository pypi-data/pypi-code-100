from sknrf.tutorial.cythonwrapper.cwrapper import cwrapper
from sknrf.tutorial.cythonwrapper.cwrapper.cwrapper import Queue

if __name__ == "__main__":
    print("Calling built-in wrapped C functions")
    print("cdef strlen cannot be called from python")
    print("def get_len: " + str(cwrapper.get_len(b"Hello")))

    print("Calling user-defined wrapped C functions")
    queue = Queue()
    queue.append(1)
    queue.extend([2,3,4])
    print(queue.pop())
    print(queue.peek())
    print(queue)
