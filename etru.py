#!/usr/bin/env python3
'''ETRU v1.0

Usage:
  etru.py [options] enc PUB_KEY_FILE [FILE]
  etru.py [options] dec PRIV_KEY_FILE [FILE]
  etru.py [options] gen PRIV_KEY_FILE PUB_KEY_FILE
  etru.py (-h | --help)

Options:
  -b, --block        Interpret input/output as
                       block stream.
  -i, --poly-input   Interpret input as polynomial
                       represented by integer array.
  -o, --poly-output  Interpret output as polynomial
                       represented by integer array.
  -h, --help         Show this screen.
  -d, --debug        Debug mode.
'''
import sys

from docopt import docopt
import helpers
from classETRU import ETRU, _generate_random_ploy
from utils import *

Debug = False  # DeBug Mode


def generate(N, p, q, priv_key: object, pub_key):
    etru = ETRU(N, p, q)
    etru.generate_random_keys()
    if Debug:
        etru.verify()
    h = np.array(etru.h_poly.coefficients)
    f = np.array(etru.f_poly.coefficients)
    f_p = np.array(etru.f_p_poly.coefficients)
    g = np.array(etru.g_poly.coefficients)
    f_q = np.array(etru.f_q_poly.coefficients)
    # save_dict_with_pickle({N: N, p: p, q: q, f: f, f_p: f_p}, priv_key)
    # save_dict_with_pickle({N: N, p: p, q: q, h: h}, pub_key)
    if Debug:
        np.savez_compressed(priv_key, N=N, p=p, q=q, f=f, f_p=f_p, g=g, f_q=f_q)
    else:
        np.savez_compressed(priv_key, N=N, p=p, q=q, f=f, f_p=f_p)
    np.savez_compressed(pub_key, N=N, p=p, q=q, h=h)


def encrypt(pub_key, input_str: str, block=False) -> np.array:
    pub_key = np.load(pub_key, allow_pickle=True)
    p = EisensteinElement(pub_key['p'].item().x, pub_key['p'].item().y)
    q = EisensteinElement(pub_key['q'].item().x, pub_key['q'].item().y)
    etru = ETRU(int(pub_key['N']), p, q)
    etru.h_poly = EisensteinPolynomial(list(pub_key['h']))
    if not block:
        try:
            msg_poly = eisenstein_encode(input_str)
            msg_poly = EisensteinPolynomial(msg_poly)
        except OverflowError:
            raise OverflowError("Input String is too large for current N, use block mode")
        output = etru.encrypt(msg_poly, EisensteinPolynomial(_generate_random_ploy(etru.N // 8))).coefficients
    else:
        input_arr = np.fromiter((ord(char) for char in input_str), dtype=np.int64)
        input_arr = np.trim_zeros(input_arr)
        input_arr = padding_encode(input_arr, 2 * etru.N)
        # Reshape it into a two-dimensional array with a shape of (n, N),
        # where n is automatically determined based on the number of elements in the array and the value of N
        input_arr = input_arr.reshape((-1, etru.N))
        output = np.array([])
        block_count = input_arr.shape[0]
        for i, b in enumerate(input_arr, start=1):
            block_output = etru.encrypt(EisensteinPolynomial(list(b)),
                                        EisensteinPolynomial(_generate_random_ploy(etru.N // 8))).coefficients
            if len(block_output) < 2 * etru.N:
                block_output = np.pad(block_output, (0, 2 * etru.N - len(block_output)), 'constant')
            output = np.concatenate((output, block_output))
    return np.array(output).flatten()


def decrypt(priv_key_file, input_arr: list, block=False):
    priv_key = np.load(priv_key_file, allow_pickle=True)
    p = EisensteinElement(priv_key['p'].item().x, priv_key['p'].item().y)
    q = EisensteinElement(priv_key['q'].item().x, priv_key['q'].item().y)
    etru = ETRU(int(priv_key['N']), p, q)
    etru.f_poly = EisensteinPolynomial(list(priv_key['f']))
    etru.f_p_poly = EisensteinPolynomial(list(priv_key['f_p']))
    # input_arr = np.fromiter((ord(char) for char in input_str), dtype=np.int64)
    # input_arr = np.trim_zeros(input_arr)

    if not block:
        if 2 * etru.N < len(input_arr):
            raise OverflowError("Input is too large for current N")
        input = EisensteinPolynomial(input_arr)
        return etru.decrypt(input).coefficients
    else:
        input = input.reshape((-1, etru.N))
        output = np.array([])
        block_count = input.shape[0]
        for i, b in enumerate(input, start=1):
            block_output = etru.decrypt(EisensteinPolynomial(list(b))).coefficients
            if len(block_output) < etru.N:
                block_output = np.pad(block_output, (0, etru.N - len(block_output)), 'constant')
            output = np.concatenate((output, block_output))
        return padding_decode(output, etru.N)


def verify():
    if not Debug:
        raise NotImplementedError("Verify is specially designed for Debug mode")


if __name__ == "__main__":
    args = docopt(__doc__)
    # Had better not change these constant. Possibly lead to decryption failure
    # See chapter 3.1.5 in paper
    N = 251
    p = EisensteinElement(2, 3)
    q = EisensteinElement(0, 167)
    if args['--debug']:
        Debug = True

    if Debug:
        # poly = message_to_poly("My name is Maozihao")
        # string=poly_to_message(poly)
        # generate(N, p, q, 'key_priv', 'key_pub')
        pub_key = np.load('key_pub.npz', allow_pickle=True)
        message = "I am Maozihao"
        input_poly = EisensteinPolynomial(eisenstein_encode(message))
        print(f"input poly = {input_poly}")
        output1 = encrypt('key_pub.npz', message)
        encrypt_poly = EisensteinPolynomial(list(output1))
        print(f"encrypt poly = {encrypt_poly}")
        priv_key = np.load('key_priv.npz', allow_pickle=True)
        etru = ETRU(int(priv_key['N']), p, q)
        etru.f_poly = EisensteinPolynomial(list(priv_key['f']))
        etru.f_p_poly = EisensteinPolynomial(list(priv_key['f_p']))
        decrypt_poly = etru.decrypt(encrypt_poly)
        print(f"decrypt poly = {decrypt_poly}")
        print(f"decrypt_poly-input_poly={decrypt_poly - input_poly}")
        print(eisenstein_decode(decrypt_poly.coefficients))

    else:
        # poly_input = bool(args['--poly-input'])
        poly_output = bool(args['--poly-output'])
        block = bool(args['--block'])
        input_str, output = None, None
        if not args['gen']:
            if args['FILE'] is None or args['FILE'] == '-':
                input_str = sys.stdin.read()  # if poly_input else sys.stdin.buffer.read()
            else:
                with open(args['FILE'], 'rb') as file:
                    input_str = file.read()
                    input_str = input_str.decode()
            # if poly_input:
            # input_arr = np.array(eval(input_str))
            # pass
            # else:
            # pass
            # input_arr = np.trim_zeros(input_arr, 'b')

        if args['gen']:
            generate(N, p, q, args['PRIV_KEY_FILE'], args['PUB_KEY_FILE'])

        elif args['enc']:
            output = encrypt(args['PUB_KEY_FILE'], input_str, block=block)
            # output type: <class 'numpy.ndarray'>
            if poly_output:
                print(EisensteinPolynomial(list(output)))
            else:
                output = output.tolist()
                o = [item for out in output for item in (out.x, out.y)]
                print(o)
                output_string = ''.join(chr(0x10000 + num) if num < 0 else chr(num) for num in o)
                with open("ciphertext.txt", "w") as file:
                    file.write(output_string)
                sys.stdout.buffer.write(output_string.encode())

        elif args['dec']:
            # input_str = input_str.decode()
            input_arr = [ord(char) - 0x10000 if ord(char) >= 0x10000 else ord(char)
                         for char in input_str]
            input_arr = list(map(lambda x: x - 65536 if x > 10000 else x, input_arr))
            print("-----------------------------")
            #print(input_arr)
            input_arr = [EisensteinElement(input_arr[i], input_arr[i + 1])
                         for i in range(0, len(input_arr), 2)]
            output = decrypt(args['PRIV_KEY_FILE'], input_arr, block=block)
            if poly_output:
                print(EisensteinPolynomial(list(output)))
            else:
                print(eisenstein_decode(list(output)))
        '''
        if not args['gen']:
            # output type: <class 'numpy.ndarray'>
            if poly_output:
                print(EisensteinPolynomial(list(output)))
            else:
                o = [item for out in output for item in (out.x, out.y)]
                # print(o)
                output_string = ''.join(chr(0x10000 + num) if num < 0 else chr(num) for num in o)
                sys.stdout.buffer.write(output_string.encode())
        '''
# echo "hello!" | ./etru.py enc keypub.npz
# ./etru.py gen 251 (2,3) (1,-1) key_priv key_pub
# echo "I am Maozihao" | python etru.py -i -o enc key_pub.npz
# echo "I am Maozihao" | python etru.py -i enc key_pub.npz
