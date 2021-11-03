from typing import List, Optional

def binary_recursive(
    arr: List[int], 
    left: int, 
    right: int, 
    item: int
) -> Optional[int]:
    """Binary search algorithm, recursive version.

    Args:
        arr: Sorted collection.
        left: Starting in 0.
        right: Starting in len(arr)-1
        item: Item value to search.
    
    Retuns:
        int: Index of found value.
    """
    if right >= left:
        mid = left + (right - left) // 2
        if arr[mid] == item:
            return mid
        elif arr[mid] > item:
            return binary_recursive(arr, left, mid-1, item)
        else:
            return binary_recursive(arr, mid+1, right, item )
    else:
        return -1

def binary_search(arr: List[int], item: int) -> Optional[int]:
    """Binary search algorithm.

    Args:
        arr: Sorted collection.
        item: Item value to search.

    Returns:
        int: Index of found item.
    """
    left = 0
    right = len(arr) - 1 
    while left <= right:
        middle = left + (right - 1) // 2
        if arr[middle] == item:
            return middle
        elif item < arr[middle]:
            right = middle - 1
        else:
            left = middle + 1
    return None


def bubble_sort(arr: List[int]) -> List[int]:
    """Bubble sort.

    Args:
        arr: Collection.

    Returns:
        Sorted collection.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if swapped == False:
            break
    return arr

def fibonacci(n, cache={0:0, 1:1}):
    """Recursive Fibonacci using cache.
    """
    if n not in cache:
        cache[n] = fibonacci(n-1, cache) + fibonacci(n-2, cache)
    return cache[n]

def fibo_generator(M):
    """Fibonacci generator.
    """
    f, f_ = 0, 1
    while f < M:
        yield f
        f, f_ = f_, f + f_

def find_all(s: str, t: str) -> int:
    """Returns all indexes where substring 't' occurs in string 's'.
    """
    indices = []
    i = s.find(t)
    while i > -1:
        indices.append(i)
        i = s.find(t, i+1)
    return indices

def is_prime(n: int) -> bool:
    """Determines if a numbers is prime or not.

    Args:
        n (int): Number.

    Returns:
        bool: Is prime or not.
    """
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

def pigeon_hole(arr):
    """Pigeon Hole algorithm.
    
    Args:
        arr: Matrix.
    """
    min_ = min(arr)
    max_ = max(arr)
    size = max_ - min_ + 1
    holes = [0] * size
    for x in arr:
        holes[x - min_] += 1
    i = 0
    for k in range(size):
        while holes[k] > 0:
            holes[k] -= 1
            arr[i] = k + min_
            i += 1
    return arr


def sieve_of_eratosthenes(n: int) -> int:
    """Determines if a number is prime or not using Sieve of Eratosthenes.
    """
    prime = [True for i in range(n+1)]
    p = 2
    while p * p <= n:
        if prime[p] == True:
            for i in range(p*p, n+1, p):
                prime[i] = False
        p += 1
    c = 0
    for p in range(2, n):
        if prime[p]:
            c += 1
    return c

def sieve(n):
    p = [True] * n
    for i in range(3, int(n**0.5)+1, 2):
        if p[i]:
            p[i*i::2*i] = [False] * int((n-i*i-1)/(2*i) + 1)
    return [2] + [i for i in range(3, n, 2) if p[i]]