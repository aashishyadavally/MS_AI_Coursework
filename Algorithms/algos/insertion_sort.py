"""
Implementation for Insertion Sort

Author
------
Aashish Yadavally
"""

def get_reverse_condition(a, b, reverse):
    """
    Get condition for while-loop

    Arguments
    ---------
        a (float):
            While-condition argument
        b (float):
            While-condition argument
        reverse (bool):
            True, indicates sorting in non-increasing order
            False, indicates sorting in non-increading order

    Returns
    -------
        (bool):
            a < b if reverse is True, else a > b        
    """
    if reverse == True:
        return a < b
    else:
        return a > b


def Insertion_Sort(array: list, reverse: bool=False) -> list:
    """
    Implementation for the insertion sort algorithm

    Arguments
    ---------
        array (list):
            Array to be sorted
        reverse (bool):
            True, indicates sorting in non-increasing order
            False, indicates sorting in non-increading order

    Returns
    -------
        array (list):
            Array sorted using Insertion Sort algorithm
    """
    for j in range(1, len(array)):
        # Current comparison element
        key = array[j]
        i = j - 1

        while i >= 0 and get_reverse_condition(array[i], key, reverse):
            # Movement or shift to right
            array[i + 1] = array[i]
            i = i - 1
        array[i + 1] = key
    return array
