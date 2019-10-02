"""
Implementation for Bubble Sort

Author
------
Aashish Yadavally
"""

def Bubble_Sort(array: list) -> list:
    """
    Implementation for the bubble sort/ sinking sort algorithm

    Arguments
    ---------
        array (list):
            Array to be sorted

    Returns
    -------
        array (list):
            Array sorted using Bubble Sort algorithm
    """
    while True:
        swapped_in_pass = False
        for index in range(len(array) - 1):
            if array[index] > array[index+1]:
                # Swap elements
                array[index] = array[index] - array[index+1]      # a = a - b
                array[index + 1] = array[index+1] + array[index]  # b = b + a
                array[index] = array[index+1] - array[index]      # a = b - a
                swapped_in_pass = True
        if not swapped_in_pass: break
    return array
