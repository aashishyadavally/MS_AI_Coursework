"""
Implementation for Insertion Sort

Author
------
Aashish Yadavally
"""

def Insertion_Sort(array: list) -> list:
    """
    Implementation for the insertion sort algorithm

    Arguments
    ---------
        array (list):
            Array to be sorted

    Returns
    -------
        array (list):
            Array sorted using Insertion Sort algorithm
    """
    for j in range(1, len(array)):
        # Current comparison element
        key = array[j]
        i = j - 1
        while i >= 0 and array[i] > key:
            # Movement or shift to right
            array[i + 1] = array[i]
            i = i - 1
        array[i + 1] = key
    return array

