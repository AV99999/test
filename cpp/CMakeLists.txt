cmake_minimum_required(VERSION 3.10)
project(tcl_interpreter)

set(CMAKE_CXX_STANDARD 14)

find_package(TCL REQUIRED)

include_directories(
  ${TCL_INCLUDE_PATH}
  ../lib/OpenDB/include
  ../lib/OpenDB/include/opendb
  ../lib/OpenDB/src
  ../lib/OpenDB/src/db
  ../lib/OpenDB/src/def
  ../lib/OpenDB/src/zlib
  ../lib/OpenDB/src/zutil
  ../lib/OpenDB/src/lef
  ../lib/OpenDB/src/defin
  ../lib/OpenDB/src/defout
  ../lib/OpenDB/src/lefin
  ../lib/OpenDB/src/lefout
  ../lib/OpenDB/src/tm
)

link_directories(
  ../lib/OpenDB/build/src/db
  ../lib/OpenDB/build/src/zlib
  ../lib/OpenDB/build/src/zutil
  ../lib/OpenDB/build/src/defin
  ../lib/OpenDB/build/src/defout
  ../lib/OpenDB/build/src/lefin
  ../lib/OpenDB/build/src/lefout
  ../lib/OpenDB/build/src/tm
  ../lib/OpenDB/src/def/lib
  ../lib/OpenDB/src/lef/lib        # ✅ here’s the fix
  ../lib/OpenDB/build/src/swig/tcl
)

add_library(tcl_interpreter SHARED tcl_interpreter.cpp)

target_link_libraries(tcl_interpreter
  ${TCL_LIBRARY}
  -Wl,--whole-archive
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/db/libopendb.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/zlib/libzlib.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/zutil/libzutil.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/defin/libdefin.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/defout/libdefout.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/lefin/liblefin.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/lefout/liblefout.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/tm/libtm.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/src/def/lib/libdef.a
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/src/lef/lib/liblef.a      # ✅ <== the fix
    ${CMAKE_CURRENT_SOURCE_DIR}/../lib/OpenDB/build/src/swig/tcl/libopendbtcl.a
  -Wl,--no-whole-archive
)

