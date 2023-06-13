#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <gmp.h>

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

std::string convertToBase7(const mpz_t& number) {
    if (mpz_cmp_si(number, 0) == 0) {
        return "0";
    }

    std::string result = "";
    bool isNegative = false;

    mpz_t temp;
    mpz_init(temp);
    mpz_set(temp, number);

    if (mpz_cmp_si(temp, 0) < 0) {
        isNegative = true;
        mpz_abs(temp, temp);
    }

    while (mpz_cmp_si(temp, 0) > 0) {
        mpz_t remainder;
        mpz_init(remainder);
        mpz_mod_ui(remainder, temp, 7);
        result = mpz_get_str(nullptr, 10, remainder) + result;
        mpz_fdiv_q_ui(temp, temp, 7);
        mpz_clear(remainder);
    }

    if (isNegative) {
        result = "-" + result;
    }

    mpz_clear(temp);

    return result;
    }

std::string convertFromBase7(const std::string& base7Number) {
    mpz_t number;
    mpz_init(number);
    mpz_set_str(number, base7Number.c_str(), 7);

    std::string result = mpz_get_str(nullptr, 10, number);

    mpz_clear(number);

    return result;
}

namespace py = pybind11;

PYBIND11_MODULE(helpers, m) {
    m.def("extended_gcd", &extended_gcd, "Extended euclid algorithm, output [g,a,b] satisfy ax+by=gcd(a,b)=g");
    m.def("is_prime", &is_prime, "Check if a number is prime.");
    m.def("convertToBase7", [](const std::string& number) {
        mpz_t num;
        mpz_init(num);
        mpz_set_str(num, number.c_str(), 10);

        std::string result = convertToBase7(num);

        mpz_clear(num);

        return result;
    });
    m.def("convertFromBase7", [](const std::string& base7Number) {
        return convertFromBase7(base7Number);
    });
}