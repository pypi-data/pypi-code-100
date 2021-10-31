def bubble_sort(array):
    # We go through the list as many times as there are elements
    for i in range(len(array)):
        # We want the last pair of adjacent elements to be (n-2, n-1)
        for j in range(len(array) - 1):
            if array[j] > array[j+1]:
                # Swap
                array[j], array[j+1] = array[j+1], array[j]