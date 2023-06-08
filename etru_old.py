#!/usr/bin/env python3
"""
ETRU v0.1

Usage:
  etru.py [options] enc PUB_KEY_FILE [FILE]
  etru.py [options] dec PRIV_KEY_FILE [FILE]
  etru.py [options] gen N P Q PRIV_KEY_FILE PUB_KEY_FILE
  etru.py (-h | --help)
  etru.py --version

Options:
  -b, --block        Interpret input/output as
                       block stream.
  -i, --poly-input   Interpret input as polynomial
                       represented by integer array.
  -o, --poly-output  Interpret output as polynomial
                       represented by integer array.
  -h, --help         Show this screen.
  --version          Show version.
  -d, --debug        Debug mode.
  -v, --verbose      Verbose mode.

"""

from docopt import docopt
from etrucipher import EtruCipher
from ntru.mathutils import random_e_poly, EIR
from sympy.abc import x
from sympy import ZZ, Poly
import numpy as np
import sys
import logging
import math
import time

from utils import padding_decode, padding_encode

log = logging.getLogger("etru")

debug = False
verbose = False

def generate(N, p, q, priv_key_file, pub_key_file):
    #start_time = time.time()
    etru = EtruCipher(N, p, q)
    etru.generate_random_keys()
    h = np.array(etru.h_poly.all_coeffs()[::-1])
    f, f_p = etru.f_poly.all_coeffs()[::-1], etru.f_p_poly.all_coeffs()[::-1]
    #end_time = time.time()
    #run_time = end_time - start_time
    #log.info("程序运行时间为：%.2f秒" % run_time)
    np.savez_compressed(priv_key_file, N=N, p=p, q=q, f=f, f_p=f_p)
    log.info("Private key saved to {} file".format(priv_key_file))
    np.savez_compressed(pub_key_file, N=N, p=p, q=q, h=h)
    log.info("Public key saved to {} file".format(pub_key_file))


def encrypt(pub_key_file, input_arr, bin_output=False, block=False):
    pub_key = np.load(pub_key_file, allow_pickle=True)
    etru = EtruCipher(int(pub_key['N']), int(pub_key['p']), int(pub_key['q']))
    etru.h_poly = Poly(pub_key['h'].astype(int)[::-1], x).set_domain(EIR)
    if not block:
        if etru.N < len(input_arr):
            raise Exception("Input is too large for current N")
        output = (etru.encrypt(Poly(input_arr[::-1], x).set_domain(EIR),
                               random_e_poly(etru.N, int(math.sqrt(etru.q)))).all_coeffs()[::-1])
    else:
        input_arr = padding_encode(input_arr, etru.N)
        input_arr = input_arr.reshape((-1, etru.N))
        output = np.array([])
        block_count = input_arr.shape[0]
        for i, b in enumerate(input_arr, start=1):
            log.info("Processing block {} out of {}".format(i, block_count))
            next_output = (etru.encrypt(Poly(b[::-1], x).set_domain(EIR),
                                        random_e_poly(etru.N, int(math.sqrt(etru.q)))).all_coeffs()[::-1])
            if len(next_output) < etru.N:
                next_output = np.pad(next_output, (0, etru.N - len(next_output)), 'constant')
            output = np.concatenate((output, next_output))

    if bin_output:
        k = int(math.log2(etru.q))
        output = [[0 if c == '0' else 1 for c in np.binary_repr(n, width=k)] for n in output]
    return np.array(output).flatten()


def decrypt(priv_key_file, input_arr, bin_input=False, block=False):
    priv_key = np.load(priv_key_file, allow_pickle=True)
    etru = EtruCipher(int(priv_key['N']), int(priv_key['p']), int(priv_key['q']))
    etru.f_poly = Poly(priv_key['f'].astype(int)[::-1], x).set_domain(EIR)
    etru.f_p_poly = Poly(priv_key['f_p'].astype(int)[::-1], x).set_domain(EIR)

    if bin_input:
        k = int(math.log2(etru.q))
        pad = k - len(input_arr) % k
        if pad == k:
            pad = 0
        input_arr = np.array([int("".join(n.astype(str)), 2) for n in
                              np.pad(np.array(input_arr), (0, pad), 'constant').reshape((-1, k))])
    if not block:
        if etru.N < len(input_arr):
            raise Exception("Input is too large for current N")
        log.info("POLYNOMIAL DEGREE: {}".format(max(0, len(input_arr) - 1)))
        return etru.decrypt(Poly(input_arr[::-1], x, domain=EIR)).all_coeffs()[::-1]

    input_arr = input_arr.reshape((-1, etru.N))
    output = np.array([])
    block_count = input_arr.shape[0]
    for i, b in enumerate(input_arr, start=1):
        log.info("Processing block {} out of {}".format(i, block_count))
        next_output = etru.decrypt(Poly(b[::-1], x, domain=EIR)).all_coeffs()[::-1]
        if len(next_output) < etru.N:
            next_output = np.pad(next_output, (0, etru.N - len(next_output)), 'constant')
        output = np.concatenate((output, next_output))
    return padding_decode(output, etru.N)


if __name__ == '__main__':
    args = docopt(__doc__, version='ETRU v0.1')
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    if args['--debug']:
        ch.setLevel(logging.DEBUG)
    elif args['--verbose']:
        ch.setLevel(logging.INFO)
    else:
        ch.setLevel(logging.WARN)
    root.addHandler(ch)

    log.debug(args)
    poly_input = bool(args['--poly-input'])
    poly_output = bool(args['--poly-output'])
    block = bool(args['--block'])
    input_arr, output = None, None
    if not args['gen']:
        if args['FILE'] is None or args['FILE'] == '-':
            input = sys.stdin.read() if poly_input else sys.stdin.buffer.read()
        else:
            with open(args['FILE'], 'rb') as file:
                input = file.read()
        log.info("---INPUT---")
        log.info(input)
        log.info("-----------")
        if poly_input:
            input_arr = np.array(eval(input))
        else:
            input_arr = np.unpackbits(np.frombuffer(input, dtype=np.uint8))
        input_arr = np.trim_zeros(input_arr, 'b')
        log.info("POLYNOMIAL DEGREE: {}".format(max(0, len(input_arr) - 1)))
        log.debug("BINARY: {}".format(input_arr))

    if args['gen']:
        generate(int(args['N']), int(args['P']), int(args['Q']), args['PRIV_KEY_FILE'], args['PUB_KEY_FILE'])
    elif args['enc']:
        output = encrypt(args['PUB_KEY_FILE'], input_arr, bin_output=not poly_output, block=block)
    elif args['dec']:
        output = decrypt(args['PRIV_KEY_FILE'], input_arr, bin_input=not poly_input, block=block)

    if not args['gen']:
        if poly_output:
            print(list(output.astype(int)))
        else:
            sys.stdout.buffer.write(np.packbits(np.array(output).astype(int)).tobytes())
