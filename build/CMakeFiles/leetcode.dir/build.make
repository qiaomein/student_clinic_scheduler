# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.31

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/qiaomein/student_clinic_scheduler

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/qiaomein/student_clinic_scheduler/build

# Include any dependencies generated for this target.
include CMakeFiles/leetcode.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/leetcode.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/leetcode.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/leetcode.dir/flags.make

CMakeFiles/leetcode.dir/codegen:
.PHONY : CMakeFiles/leetcode.dir/codegen

CMakeFiles/leetcode.dir/leetcode.cpp.o: CMakeFiles/leetcode.dir/flags.make
CMakeFiles/leetcode.dir/leetcode.cpp.o: /Users/qiaomein/student_clinic_scheduler/leetcode.cpp
CMakeFiles/leetcode.dir/leetcode.cpp.o: CMakeFiles/leetcode.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/qiaomein/student_clinic_scheduler/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/leetcode.dir/leetcode.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/leetcode.dir/leetcode.cpp.o -MF CMakeFiles/leetcode.dir/leetcode.cpp.o.d -o CMakeFiles/leetcode.dir/leetcode.cpp.o -c /Users/qiaomein/student_clinic_scheduler/leetcode.cpp

CMakeFiles/leetcode.dir/leetcode.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/leetcode.dir/leetcode.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/qiaomein/student_clinic_scheduler/leetcode.cpp > CMakeFiles/leetcode.dir/leetcode.cpp.i

CMakeFiles/leetcode.dir/leetcode.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/leetcode.dir/leetcode.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/qiaomein/student_clinic_scheduler/leetcode.cpp -o CMakeFiles/leetcode.dir/leetcode.cpp.s

# Object files for target leetcode
leetcode_OBJECTS = \
"CMakeFiles/leetcode.dir/leetcode.cpp.o"

# External object files for target leetcode
leetcode_EXTERNAL_OBJECTS =

libleetcode.a: CMakeFiles/leetcode.dir/leetcode.cpp.o
libleetcode.a: CMakeFiles/leetcode.dir/build.make
libleetcode.a: CMakeFiles/leetcode.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/qiaomein/student_clinic_scheduler/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libleetcode.a"
	$(CMAKE_COMMAND) -P CMakeFiles/leetcode.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/leetcode.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/leetcode.dir/build: libleetcode.a
.PHONY : CMakeFiles/leetcode.dir/build

CMakeFiles/leetcode.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/leetcode.dir/cmake_clean.cmake
.PHONY : CMakeFiles/leetcode.dir/clean

CMakeFiles/leetcode.dir/depend:
	cd /Users/qiaomein/student_clinic_scheduler/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/qiaomein/student_clinic_scheduler /Users/qiaomein/student_clinic_scheduler /Users/qiaomein/student_clinic_scheduler/build /Users/qiaomein/student_clinic_scheduler/build /Users/qiaomein/student_clinic_scheduler/build/CMakeFiles/leetcode.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/leetcode.dir/depend

