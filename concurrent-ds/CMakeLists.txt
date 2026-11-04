cmake_minimum_required(VERSION 4.4)
project(CONCURRENT_DS)
set(CMAKE_CXX_STANDARD 26)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_SCAN_FOR_MODULES OFF)

add_executable(
                main
                main.cpp 
                linked_list/cpp/LinkedListNode.cpp
                linked_list/cpp/UnSyncLinkedList.cpp
                linked_list/cpp/CoarseGrainedLinkedList.cpp
              )
target_include_directories(main PRIVATE linked_list/include)
target_link_options(main PRIVATE -static)
