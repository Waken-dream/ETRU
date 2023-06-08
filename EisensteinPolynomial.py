'''
Definition of Eisenstein Polynomial. Polynomial which coefficients are all Eisenstein Integers.

'''
from Eisenstein import EisensteinElement


zero = EisensteinElement(0, 0)
one = EisensteinElement(1, 0)


def _extend_euclid(f, g, module):
    ''' Extended Euclid Algorithm in Eisenstein Quotient Ring Z[ω]/module[x]/<G>
        Input: F,G are EisensteinPolynomial
        Output: H:Great common divisor(gcd) of f and g; A; B satisfy H=AF+BG
        So that if gcd(f,g)=1, 1=AF(mod G) , A=F.invert(mod G)
    '''
    h = f
    l = g
    u = EisensteinPolynomial([EisensteinElement(0, 0)])
    v = EisensteinPolynomial([EisensteinElement(1, 0)])
    a = EisensteinPolynomial([EisensteinElement(1, 0)])
    b = EisensteinPolynomial([EisensteinElement(0, 0)])
    while bool(l):
        q, r = _divmod(h, l,module)  # q=h//q,r=h%l
        h = l
        l = r
        c = a
        d = b
        a = u
        b = v
        u = c - q * u
        v = d - q * v
    return h%module, a, b


class EisensteinPolynomial():
    def __init__(self, coefficients: list, mod=None):
        self.coefficients = coefficients
        #self.mod = mod
        # self.domain = domain

    def __bool__(self):
        return any(self.coefficients)

    def __str__(self):
        degree = len(self.coefficients) - 1
        terms = []

        for i, coeff in enumerate(self.coefficients):
            term = '(' + str(coeff) + ')'

            if coeff != zero:
                if i < degree:
                    term += f"x^{degree - i}"

                terms.append(term)

        return " + ".join(terms)

    def __hash__(self):
        return hash(self.coefficients)

    def __eq__(self, other):
        if isinstance(other,EisensteinPolynomial):
            if other.coefficients==self.coefficients:
                return True
            return False
        return TypeError(f"{self} and {other} are not the same type !")

    def __ne__(self, other):
        if isinstance(other, EisensteinPolynomial):
            if other.coefficients == self.coefficients:
                return False
            return True
        return TypeError(f"{self} and {other} are not the same type !")


    def __add__(self, other):
        if isinstance(other, EisensteinPolynomial):
            degree_self = len(self.coefficients) - 1
            degree_other = len(other.coefficients) - 1
            max_degree = max(degree_self, degree_other)
            min_degree = min(degree_self, degree_other)

            if degree_self > degree_other:
                coefficients = self.coefficients.copy()
                for i in range(min_degree + 1):
                    coefficients[degree_self - i] += other.coefficients[degree_other - i]
            else:
                coefficients = other.coefficients.copy()
                for i in range(min_degree + 1):
                    coefficients[degree_other - i] += self.coefficients[degree_self - i]

            return EisensteinPolynomial(coefficients)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, EisensteinPolynomial):
            neg_other = EisensteinPolynomial([zero-coeff for coeff in other.coefficients])
            return self + neg_other
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, EisensteinElement):
            return EisensteinPolynomial(list(map(lambda x: x * other, self.coefficients)))
        if isinstance(other, EisensteinPolynomial):
            degree_self = len(self.coefficients) - 1
            degree_other = len(other.coefficients) - 1
            degree_result = degree_self + degree_other
            coefficients = [EisensteinElement(0, 0)] * (degree_result + 1)

            for i in range(degree_self + 1):
                for j in range(degree_other + 1):
                    product = self.coefficients[i] * other.coefficients[j]
                    coefficients[i + j] += product

            return EisensteinPolynomial(coefficients)

        return NotImplemented

    def __mod__(self, other, module=None):
        if isinstance(other, EisensteinPolynomial):
            # Perform polynomial division
            quotient, remainder = _divmod(self, other, module)

            # Return the remainder as a new polynomial
            return remainder
        elif isinstance(other, EisensteinElement) or isinstance(other, int):
            return EisensteinPolynomial(list(
                map(lambda x: x % other, self.coefficients)))
        else:
            raise TypeError("Unsupported operand type for %")

    def __floordiv__(self, other):
        if isinstance(other, EisensteinPolynomial):
            # Perform polynomial division
            quotient, remainder = _divmod(self, other)

            # Return the quotient as a new polynomial
            return quotient
        else:
            raise TypeError("Unsupported operand type for //")

    def invert(self, mod, module):
        if isinstance(mod, EisensteinPolynomial):
            h, a, b = _extend_euclid(self, mod, module)
            if len(h.coefficients)==1:
                return (a*h.coefficients[0].invert(mod=module)) % module
            #if h == EisensteinPolynomial([EisensteinElement(1, 0)]):
                #return a
            raise ZeroDivisionError(f"{self.__str__()} has no inverse in mod {mod.__str__()}")
        return NotImplemented


def _divmod(self: EisensteinPolynomial, other: EisensteinPolynomial, module: EisensteinElement = None):
    if not isinstance(other, EisensteinPolynomial): return NotImplemented
    dividend_coeffs = self.coefficients
    divisor_coeffs = other.coefficients
    # Ensure the divisor is not zero
    if len(divisor_coeffs) == 1 and divisor_coeffs[0] == zero:
        raise ZeroDivisionError("Polynomial division by zero")

    # Initialize the quotient and remainder as empty lists
    quotient_coeffs = [zero]*(len(dividend_coeffs)-len(divisor_coeffs)+1)
    remainder_coeffs = dividend_coeffs.copy()

    # Perform long division algorithm
    while len(remainder_coeffs) >= len(divisor_coeffs):
        # Get the leading terms of the dividend and divisor
        dividend_leading = remainder_coeffs[0]
        divisor_leading = divisor_coeffs[0]

        # Compute the quotient of leading terms
        # quotient_leading = dividend_leading / divisor_leading
        quotient_leading = dividend_leading * divisor_leading.invert(mod=module)

        # Add the quotient to the quotient list
        quotient_coeffs[len(divisor_coeffs)-len(remainder_coeffs)-1] = quotient_leading

        # Multiply the divisor by the quotient and subtract from the dividend
        for i in range(len(divisor_coeffs)):
            remainder_coeffs[i] -= quotient_leading * divisor_coeffs[i]
            remainder_coeffs[i] = remainder_coeffs[i]%module

        # Remove leading zeros in the remainder
        while len(remainder_coeffs) > 0 and remainder_coeffs[0] == zero:
            remainder_coeffs = remainder_coeffs[1:]

    return EisensteinPolynomial(quotient_coeffs), EisensteinPolynomial(remainder_coeffs)


if __name__ == "__main__":
    N = 5
    poly = EisensteinPolynomial([one] + [zero for i in range(N - 1)] + [zero - one])  # ploy=x^N-1
    print(poly)
    q = EisensteinElement(1, -1)
    fpoly = EisensteinPolynomial(
        [EisensteinElement(5, 17), EisensteinElement(8, 3)] + [zero for i in range(4 - 1)] + [zero - one])
    gpoly = EisensteinPolynomial(
        [one] + [zero for i in range(4 - 1)] + [zero - one])
    print(f"fpoly = {fpoly}")
    print(f"gpoly = {gpoly}")
    fqpoly = fpoly % q
    print(f"fqpoly = {fqpoly}")
    a, b = _divmod(fpoly, gpoly, q)
    print(f"a = {a}")
    fq_poly=fqpoly.invert(mod=fpoly,module=q)
