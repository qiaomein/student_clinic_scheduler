cmake_minimum_required(VERSION 3.29.2) # cmake --version to find curr version

project(SCS) # project name


#add_library(leetcode STATIC leetcode.cpp)
#add_library(ezmath STATIC adder.cpp) # this is how to add a library; these are .a files (static libraries); mainly used for adding custom libraries (built from source (cpp files))
# ^ always add source files; you also name the library here (in context of CMake)


set(pybind11_DIR ${CMAKE_SOURCE_DIR}/venv/lib/python3.13/site-packages/pybind11/share/cmake/pybind11)
find_package(pybind11 REQUIRED)
pybind11_add_module(${PROJECT_NAME} main.cpp)

set(CMAKE_CXX_STANDARD 17) # use C++ 17
#add_executable(${PROJECT_NAME} main.cpp) # this specifies which files to compile! usually only the main.cpp as libraries are in other lines


target_include_directories(${PROJECT_NAME} PRIVATE /opt/homebrew/opt/python@3.13/Frameworks/Python.framework/Versions/3.13/include/python3.13) # this tells CMake where all the libraries should be so no need to specify all directories; not used too often if using open source libraries
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/venv/lib/python3.13/site-packages/pybind11/include/) # this tells CMake where all the libraries should be so no need to specify all directories; not used too often if using open source libraries

#target_link_libraries(${PROJECT_NAME} PRIVATE ezmath) # private means that only this project can use ezmath
#target_link_libraries(${PROJECT_NAME} PRIVATE leetcode) # private means that only this project can use ezmath


############ INSTALL BELOW


# install(TARGETS ${PROJECT_NAME} DESTINATION lib) # this is for the universal libraries that linux/mac will reference! 
# no need to do target_link_directories anymore once library is installed

install(TARGETS ${PROJECT_NAME} DESTINATION bin) # install the project into the bin (binary); usually great for linux 
# if you do 
# $sudo make install
# you can rune $./SCS or $SCS from anywhere and it'll run; SCS ready to run at drop of a dime! the bin is located in /usr/local/bin/SCS; simply delete it

