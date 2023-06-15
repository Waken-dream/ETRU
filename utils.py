import binascii
import pickle
import helpers
import numpy as np

from Eisenstein import EisensteinElement
from EisensteinPolynomial import EisensteinPolynomial

N = 251


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

    input_arr = [input_arr[i:i + 2] for i in range(0, len(input_arr), 2)]
    if len(input_arr) > N:
        raise OverflowError("Input String is too large for current N, use block mode")

    coefficients = [EisensteinElement(x, y) for x, y in input_arr]
    poly = EisensteinPolynomial(coefficients)

    return poly


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


def message_to_binary(meaaage: str) -> str:
    my_bytes = meaaage.encode('utf-8')
    my_binary_string = bin(int(binascii.hexlify(my_bytes), 16))[2:]
    return my_binary_string


def binary_to_message(binary):
    return binascii.unhexlify(hex(int(binary, 2))[2:]).decode('utf-8')


def convert_to_base7(number):
    '''Can also be called by "helpers.convertToBase7(number)" .'''
    if number == 0:
        return '0'

    result = ''
    is_negative = False

    if number < 0:
        is_negative = True
        number = abs(number)

    while number > 0:
        remainder = number % 7
        result = str(remainder) + result
        number = number // 7

    if is_negative:
        result = '-' + result

    return result


def eisenstein_encode(Message: str) -> list:
    """
    Convert String to a list, which elements are EisensteinElements
    Specially designed for R_p = {0, ±1, ±ω, ±ω^2}
    """
    rp_elements = [
        EisensteinElement(0, 0),
        EisensteinElement(1, 0),
        EisensteinElement(-1, 0),
        EisensteinElement(0, 1),
        EisensteinElement(0, -1),
        EisensteinElement(1, 1),
        EisensteinElement(-1, -1),
    ]
    Message = Message.encode('utf-8')  # -> bit string
    Message = int(binascii.hexlify(Message), 16)  # -> int
    Message = helpers.convertToBase7(f"{Message}")  # -> str
    # The following line is equal to the line above.
    # message = str(convert_to_base7(message))

    if len(Message) > N:
        raise OverflowError(f"Input String is too large({len(Message)}) for current N, use block mode")
    encoded_list = []
    for s in Message:
        encoded_list.append(rp_elements[int(s)])

    return encoded_list


def eisenstein_decode(EncodedList: list) -> str:
    """Inverse function of eisenstein_encode()"""
    rp_elements = [
        EisensteinElement(0, 0),
        EisensteinElement(1, 0),
        EisensteinElement(-1, 0),
        EisensteinElement(0, 1),
        EisensteinElement(0, -1),
        EisensteinElement(1, 1),
        EisensteinElement(-1, -1),
    ]
    message = ''
    for e in EncodedList:
        index = rp_elements.index(e)
        message += str(index)
    message = helpers.convertFromBase7(message)
    hex_str = hex(int(message))[2:]
    if len(hex_str)%2 != 0:
        hex_str+=b'0'
    byte_str = binascii.unhexlify(hex_str)
    decoded_message = byte_str.decode('utf-8')
    return decoded_message


if __name__ == "__main__":
    message = "I am Maozihao"
    b_message = message_to_binary(message)
    print(f"b_message = {b_message}")
    message = binary_to_message(b_message)
    print(f"message = {message}")
    # e_message=eisenstein_encode(message)
    encoded_list = eisenstein_encode("I am Maozihao")
    decoded_message = eisenstein_decode(encoded_list)
    print(decoded_message)
