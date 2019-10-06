class InputSizeException(Exception):
   """
   Raised when the input arrays are of different dimensions
   """
   pass


def Add_Two_Binary(A: list, B: list) -> list:
    """
    Adds two n-bit binary integers stored in arrays A and B

    Arguments
    ---------
        A (list):
            n-bit binary integer representation
        B (list):
            n-bit binary integer representation

    Returns
    -------
        C (list):
            (n+1)-bit binary integer representation
    """
    try:
        if len(A) != len(B):
            raise InputSizeException
        else:
            carry = 0
            n = len(A)
            C = [0] * (n + 1)
            for index in range(n):
                bit_sum = A[n - index - 1] + B[n - index - 1] + carry
                if bit_sum == 0:
                    carry = 0
                    C[n - index] = 0
                elif bit_sum == 1:
                    carry = 0
                    C[n - index] = 1
                elif bit_sum == 2:
                    carry = 1
                    C[n - index] = 0
                elif bit_sum == 3:
                    carry = 1
                    C[n -index] = 1
            if carry == 1:
                C[0] = 1
            return C

    except:
        print('Input arrays are of different sizes.')
