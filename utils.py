import pickle

import numpy as np

from Eisenstein import EisensteinElement
from EisensteinPolynomial import EisensteinPolynomial

N = 251

def message_to_poly(input_str: str) -> EisensteinPolynomial:
    '''
    Convert message to Eisenstein Polynomial
    '''
    # Convert every character in the string to its ASCII number
    # input_arr = np.array([ord(char) for char in input_str])
    input_arr = np.fromiter((ord(char) for char in input_str), dtype=np.int64)

    # Remove 0 in the beginning or ending
    input_arr = np.trim_zeros(input_arr)

    if len(input_arr) % 2:
        input_arr = np.append(input_arr, 0)

    input_arr = input_arr.reshape(-1, 2).astype(np.int)
    if len(input_arr) > N:
        raise OverflowError("Input String is too large for current N, use block mode")
    # print(input_arr)

    coefficients = [EisensteinElement(x, y) for x, y in input_arr]
    poly = EisensteinPolynomial(coefficients)
    # print(poly)

    return poly

def message_to_poly(input_str: str) -> EisensteinPolynomial:
    """
    Convert message to Eisenstein Polynomial
    """
    input_arr = [ord(char) for char in input_str]

    # Remove 0 in the beginning or ending
    while len(input_arr) > 0 and input_arr[0] == 0:
        input_arr.pop(0)
    while len(input_arr) > 0 and input_arr[-1] == 0:
        input_arr.pop()

    if len(input_arr) % 2:
        input_arr.append(0)

    input_arr = [input_arr[i:i+2] for i in range(0, len(input_arr), 2)]
    if len(input_arr) > N:
        raise OverflowError("Input String is too large for current N, use block mode")

    coefficients = [EisensteinElement(x, y) for x, y in input_arr]
    poly = EisensteinPolynomial(coefficients)

    return poly

def poly_to_message(poly: EisensteinPolynomial) -> str:
    '''
    Convert Eisenstein Polynomial to String
    '''
    coeffients = poly.coefficients
    input_arr = np.array([(coeff.x, coeff.y) for coeff in coeffients])
    input_arr = np.array(input_arr).flatten().tolist()
    input_str = ''.join(np.char.mod('%c', input_arr))
    # print(input_str)

    return input_str

def poly_to_message(poly: EisensteinPolynomial) -> str:
    """
    Convert Eisenstein Polynomial to String
    """
    coefficients = poly.coefficients

    input_arr = [(coeff.x, coeff.y) for coeff in coefficients]
    input_arr = [item for sublist in input_arr for item in sublist]
    input_str = ''.join(chr(x) for x in input_arr)

    return input_str

def padding_encode(input_arr, block_size):
    n = block_size - len(input_arr) % block_size
    if n == block_size:
        return np.pad(input_arr, (0, n), 'constant')
    last_block = np.pad(np.ones(n), (block_size - n, 0), 'constant')
    return np.concatenate((np.pad(input_arr, (0, n), 'constant'), last_block))


def padding_decode(input_arr, block_size):
    last_block = input_arr[-block_size:]
    zeros_to_remove = len(np.trim_zeros(last_block))
    return input_arr[:-(block_size + zeros_to_remove)]


def save_dict_with_pickle(dictionary, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(dictionary, file)