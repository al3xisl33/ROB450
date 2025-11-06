cmake_minimum_required(VERSION 3.10)
project(set_pid_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

# --- Fetch moteus from GitHub ---
FetchContent_Declare(
  moteus
  GIT_REPOSITORY https://github.com/mjbots/moteus.git
  GIT_TAG main
)

FetchContent_MakeAvailable(moteus)

# --- Build your executable ---
add_executable(wait_complete wait_complete.cc)
target_link_libraries(wait_complete moteus::cpp)

add_executable(wait_complete_orig wait_complete_orig.cc)
target_link_libraries(wait_complete_orig moteus::cpp)

add_executable(multiple_cycle multiple_cycle.cc)
target_link_libraries(multiple_cycle moteus::cpp)

add_executable(1_cycle 1_cycle.cc)
target_link_libraries(1_cycle moteus::cpp)

