!/bin/bash

g++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) helpers.cpp -lgmp -o helpers.so