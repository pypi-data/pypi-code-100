'''

Algop

2021 - Isa Haji - MIT License 

'''

def bubbleSort(array, say=False):
    try:
        # We go through the list as many times as there are elements
        for i in range(len(array)):
            # We want the last pair of adjacent elements to be (n-2, n-1)
            for j in range(len(array) - 1):
                if array[j] > array[j+1]:
                    # Swap
                    array[j], array[j+1] = array[j+1], array[j]
    except:
        print("Not a Valid Data Type")

    if say:
        print(array)
        return array
    else:
        return array


def insertionSort(array, say=False):
    try:
        # We start from 1 since the first element is trivially sorted
        for index in range(1, len(array)):
            currentValue = array[index]
            currentPosition = index

            # As long as we haven't reached the beginning and there is an element
            # in our sorted array larger than the one we're trying to insert - move
            # that element to the right
            while currentPosition > 0 and array[currentPosition - 1] > currentValue:
                array[currentPosition] = array[currentPosition - 1]
                currentPosition = currentPosition - 1

            # we're trying to insert at index currentPosition - 1.
            # Either way - we insert the element at currentPosition
            array[currentPosition] = currentValue
    except:
        print("Not a Valid Data Type")

    if say:
        print(array)
        return array
    else:
        return array


def twoNumberSum(array, target, say=False):
    nums = {}
    try:
        for num in array:
            potentialMatch = target - num
            if potentialMatch in nums:
                if say:
                    print(potentialMatch, num)
                    return [potentialMatch, num]
                else:
                    return [potentialMatch, num]
            else:
                nums[num] = True
        return 'No Match Found'
    except:
        print("Not a Valid Data Type")




