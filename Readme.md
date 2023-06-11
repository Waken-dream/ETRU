# ETRU Implementation via Python

ETRU is an NTRU-like cryptosystem based on the Eisenstein integers Z[ω] where ω is a primitive cube root of unity. (The NTRU public key cryptosystem was proposed by J. Hoffstein, J. Pipher and J. H. Silverman in 1996. NTRU keys are truncated polynomials with integer coefficients.)

Should have Python 3.x installed on your system.

## Disclaimer

**Under no circumstances should this be used for a cryptographic application!**

This Project is written for a homework to extend NTRU into the Eisenstein Ring.

Guided by paper [ETRU: NTRU over the Eisenstein integers (Monica Nevins)](https://www.researchgate.net/publication/257555334_ETRU_NTRU_over_the_Eisenstein_integers) and [ETRU: NTRU over the Eisenstein integers(Katherine Jarvis · Monica Nevins)](https://link.springer.com/article/10.1007/s10623-013-9850-3)

# What's in this project

```Eisenstein.py```: Definition of Eisenstein Integer and Eisenstein Integer Ring

`EisensteinPloynomial.py`: Definition of Eisenstein Polynomial. Polynomials which coefficients are all Eisenstein Integers.

`classETRU.py`: Definition of ETRU, with method to (1) generate public key & private keys (2) encrypt (3) decrypt

# How to use

At the first time you use this package, delete the file `helper.so` and run the following command in Terminal to compile pybind C++ file `helpers.cpp` and generate a new `helper.so` in your directory.

```bash
(base)$ g++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) helpers.cpp -o helpers.so
```

Or you can skip the step above by modifying the `is_prime()` method in `Eisenstein.py` to avoid use helpers.so

```python
@property
    def is_prime(self):
        '''
        Proposition 4.2.4: If φ ∈ Z[ω] and d (φ) = p where p is a rational prime, then φ is a prime in Z[ω].
        :return: bool: True or False
        '''
        if is_prime(self.norm):
        #if helpers.is_prime(self.norm):
            return True
        else:
            return False
```

Now this project has a problem of unequal encryption and decryption, my classmate and I are fixing it.
