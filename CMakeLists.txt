cmake_minimum_required(VERSION 3.10)

project(ci-project VERSION 1.0
                   DESCRIPTION "GROUP-D"
                   LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_compile_options(-Wall -Wextra -Wpedantic)
include_directories(${CMAKE_SOURCE_DIR}/lib/buffer ${CMAKE_SOURCE_DIR}/lib/signals)

include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/lib/signals/signals.cpp)
    add_library(signals lib/buffer/buffer.o lib/signals/signals.cpp)
endif()

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/test/test.cpp)
    add_executable(test test/test.cpp)
    target_link_libraries(test PRIVATE gtest_main signals)
endif()

add_custom_target(generate COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/script/generate.py)