'''
Definition of Eisenstein Integer and Eisenstein Integer Ring
Guided by paper "ETRU: NTRU over the Eisenstein integers"
'''

import helpers
import os


def _extended_eucild(f, g):
    '''Extended Euclid Algorithm
    Input: F,G are EisensteinElement
    Output: H:Great common divisor(gcd) of f and g; A; B satisfy H=AF+BG
    So that if gcd(f,g)=1, 1=AF(mod G) , A=F.invert(mod G)
    '''
    h = f
    l = g
    u = EisensteinElement(0, 0)
    v = EisensteinElement(1, 0)
    a = EisensteinElement(1, 0)
    b = EisensteinElement(0, 0)
    while l != EisensteinElement(0, 0):
        q, r = h.__divmod__(l)  # q=h//q,r=h%l
        h = l
        l = r
        c = a
        d = b
        a = u
        b = v
        u = c - q * u
        v = d - q * v
    return h, a, b


def is_prime(n: int) -> bool:
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# a+bW
class EisensteinElement():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dtype = EisensteinElement

    def __bool__(self):
        if self.x == 0 and self.y == 0:
            return False
        return True

    def __str__(self):
        return f"{self.x} + {self.y}*omega"

    def __add__(self, other):
        if isinstance(other, EisensteinElement):
            return EisensteinElement(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, EisensteinElement):
            x = self.x - other.x
            y = self.y - other.y
            return EisensteinElement(x, y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, EisensteinElement):
            x = self.x * other.x - self.y * other.y
            y = self.x * other.y + self.y * other.x - self.y * other.y
            return EisensteinElement(x, y)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, EisensteinElement):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        raise TypeError('Not the same type of data')

    def __ne__(self, other):
        if isinstance(other, EisensteinElement):
            if self.x == other.x and self.y == other.y:
                return False
            else:
                return True
        raise TypeError('Not the same type of data')

    def __pow__(self, exponent: int):
        '''
        Fast power algorithm
        :return: EisensteinElement: self ** exponent
        '''
        result = EisensteinElement(1, 0)
        base = self

        while exponent > 0:
            if exponent % 2 == 1:
                result *= base
            base *= base
            exponent //= 2

        return result

    @property
    def norm(self):
        return self.x ** 2 - self.x * self.y + self.y ** 2

    @property
    def conjugate(self):
        return EisensteinElement(self.x, -self.y)

    def __truediv__(self, other):
        '''Eisenstein Integer doesn't have float divide'''
        return NotImplemented("Eisenstein Integer doesn't have float divide")

    def __divmod__(self, other):
        '''
        CVP Algorithm
        Input: α = self.x + self.y*ω and q = other.x + other.y*ω
        Output:(r, β) such that α = rq + β and β is reduced modulo q.
        :param other: EisensteinElement
        :return: r2: EisensteinElement, b2: EisensteinElement. Quotient and remainder
        '''
        if isinstance(other, EisensteinElement):
            epsilon1 = 2 * other.x - other.y
            epsilon2 = 2 * other.y - other.x
            Q = other.norm
            d = 2 * Q
            s = self.x * epsilon1 + self.y * epsilon2
            t = self.y * other.x - self.x * other.y
            x0 = (s - s % d + d) // d if s % d > Q else (s - s % d) // d
            x1 = (t - t % d + d) // d if t % d > Q else (t - t % d) // d
            r1 = EisensteinElement(x0 + x1, 2 * x1)
            b1 = self - other * r1
            s += Q
            t -= Q
            y0 = (s - s % d + d) // d if s % d > Q else (s - s % d) // d
            y1 = (t - t % d + d) // d if t % d > Q else (t - t % d) // d
            r2 = EisensteinElement(y0 + y1, 2 * y1 + 1)
            b2 = self - other * r2
            if b1.norm < b2.norm:
                return r1, b1
            elif b1.norm > b2.norm:
                return r2, b2
            elif x0 < y0:
                return r1, b1
            else:
                return r2, b2
        return NotImplemented

    def __mod__(self, other):
        if isinstance(other, int):
            return EisensteinElement(self.x % other, self.y % other)
        if isinstance(other, EisensteinElement):
            return self.__divmod__(other)[1]
        raise TypeError("Unsupported operand type for %")

    def __floordiv__(self, other):
        if isinstance(other, EisensteinElement):
            return self.__divmod__(other)[0]
        raise TypeError("Unsupported operand type for //")

    def invert(self, mod):
        if isinstance(mod, EisensteinElement):
            '''
            Consider 6 units in Eisenstein Integer
            '''
            h, a, b = _extended_eucild(self, mod)
            if h == EisensteinElement(1, 0):
                return a
            elif h == EisensteinElement(-1, 0):
                return EisensteinElement(0, 0) - a
            elif h == EisensteinElement(0, 1):
                return a * EisensteinElement(-1, -1)
            elif h == EisensteinElement(0, -1):
                return a * EisensteinElement(1, 1)
            elif h == EisensteinElement(-1, -1):
                return a * EisensteinElement(0, 1)
            elif h == EisensteinElement(1, 1):
                return a * EisensteinElement(0, -1)
            raise ZeroDivisionError(f"{self} has no inverse in mod {mod.__str__()}")

    @property
    def is_prime(self):
        '''
        Proposition 4.2.4: If φ ∈ Z[ω] and d (φ) = p where p is a rational prime, then φ is a prime in Z[ω].
        :return: bool: True or False
        '''
        # if is_prime(self.norm):
        if helpers.is_prime(self.norm):
            return True
        else:
            return False


# os.system("g++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) helpers.cpp -o helpers.so")

if __name__ == "__main__":
    a = EisensteinElement(5, 17)
    b = EisensteinElement(8, 3)
    print(f"a*b = {a * b}")
    print(f'a//b = {a // b}')
    print(f'a%b = {a % b}')
    zero = EisensteinElement(0, 0)
    print(f"bool(zero)={bool(zero)}")
    try:
        # 计算倒数
        c = b.invert(mod=a)
        print(f"b^-1 = {c}")  # 输出: 0.25 - 0.125ω
    except ZeroDivisionError as e:
        print(f'e = {e}')
