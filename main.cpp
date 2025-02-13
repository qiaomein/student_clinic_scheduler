#include <Python.h> //include this first just ot be safe
#include "pybind11/pybind11.h" // link cpp to python modules

#include<stdlib.h>
#include<stdio.h>
#include<iostream>



namespace py = pybind11;

using std::cout;
using std::endl;



// int add(int a, int b){
//     return a + b;
// }

PYBIND11_MODULE(SCS,m){
    //m.def("add", &add, "Adds two numbers for this pybind11 example working code.");
    
}

int main(){

    return 0;
}

