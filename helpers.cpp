#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace std;

vector<int> extended_gcd(int a, int b) {
    if (b == 0) {
        return {a, 1, 0};
    } else {
        vector<int> tmp = extended_gcd(b, a % b);
        auto g = tmp[0], x = tmp[1], y = tmp[2];
        return {g, y, x - (a / b) * y};
    }
}

bool is_prime(int n) {
    for (int i = 2; i <= static_cast<int>(sqrt(n)); ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

namespace py = pybind11;

PYBIND11_MODULE(helpers, m) {
    m.def("extended_gcd", &extended_gcd, "Extended euclid algorithm, output [g,a,b] satisfy ax+by=gcd(a,b)=g");
    m.def("is_prime", &is_prime, "Check if a number is prime.");
}