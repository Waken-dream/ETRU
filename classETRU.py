import random

from Eisenstein import EisensteinElement
from EisensteinPolynomial import EisensteinPolynomial

zero = EisensteinElement(0, 0)
one = EisensteinElement(1, 0)



def _generate_random_ploy(d):
    '''
    Generate Random Eisenstein Polynomial of degree 7d
    '''
    list = [EisensteinElement(0, 0), EisensteinElement(1, 0), EisensteinElement(-1, 0),
            EisensteinElement(0, 1), EisensteinElement(0, -1), EisensteinElement(-1, -1), EisensteinElement(1, 1)
            ] * d
    # list.append(one)
    random.shuffle(list)
    # index = random.sample(range(len(list) + 1))
    # list.insert(index,one)
    return list


class ETRU:
    N = None
    p = None
    q = None
    f_poly = None
    g_poly = None
    h_poly = None
    f_p_poly = None
    f_q_poly = None
    R_poly = None

    def __init__(self, N, p, q):
        self.N = N
        self.p = p
        self.q = q
        self.R_poly = EisensteinPolynomial([one] + [zero for i in range(N - 1)] + [zero - one])

    def generate_random_keys(self):
        g_poly = EisensteinPolynomial(_generate_random_ploy(self.N // 7))
        tries = 10
        while tries > 0 and (self.h_poly is None):
            list = _generate_random_ploy(self.N // 7)
            index = random.sample(range(len(list) + 1), 1)[0]
            list.insert(index, one)
            f_poly = EisensteinPolynomial(list)
            try:
                self.generate_public_keys(f_poly, g_poly)
            except ZeroDivisionError:
                print(f_poly)
                tries -= 1
        if self.h_poly is None:
            raise Exception("Couldn't generate invertible f")

    def generate_public_keys(self, f_poly, g_poly):
        self.f_poly = f_poly
        self.g_poly = g_poly
        self.f_p_poly = self.f_poly.invert(mod=self.R_poly, module=self.p)
        self.f_q_poly = self.f_poly.invert(mod=self.R_poly, module=self.q)
        p_f_q_poly = (self.f_q_poly * self.p) % self.q
        h_before_mod = (p_f_q_poly * self.g_poly) % self.q
        self.h_poly = (h_before_mod.__mod__(self.R_poly, self.q)) % self.q
        self.h_poly = (self.f_q_poly*self.g_poly).__mod__(self.R_poly,self.q) % self.q

    def encrypt(self, msg_poly: EisensteinPolynomial, rand_poly: EisensteinPolynomial) -> EisensteinPolynomial:

        return (((rand_poly * self.h_poly * self.p) + msg_poly).__mod__(self.R_poly, self.q)) % self.q

    def decrypt(self, msg_poly: EisensteinPolynomial) -> EisensteinPolynomial:
        a_poly = ((self.f_poly * msg_poly).__mod__(self.R_poly, self.q)) % self.q
        b_poly = a_poly % self.p
        return ((self.f_p_poly * a_poly).__mod__(self.R_poly, self.p)) % self.p

    def verify(self):
        print((self.f_poly*self.f_p_poly).__mod__(self.R_poly,self.p) % self.p)
        print((self.f_q_poly*self.f_poly).__mod__(self.R_poly,self.q) % self.q)



if __name__ == "__main__":
    etru = ETRU(N=251,
                p=EisensteinElement(2, 3),
                q=EisensteinElement(1, -1))
    etru.generate_random_keys()
