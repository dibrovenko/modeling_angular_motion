cmake_minimum_required(VERSION 3.26)
project(Gravity)

set(CMAKE_CXX_STANDARD 17)

find_package(GeographicLib REQUIRED)
include_directories (${GeographicLib_INCLUDE_DIRS})


add_executable(Gravity main.cpp)
target_link_libraries (Gravity ${GeographicLib_LIBRARIES})


# Укажите исходные файлы
set(SOURCES gravity_ITRF.cpp)

# Создайте библиотеку с флагами -fPIC и -shared
add_library(gravity_ITRF SHARED ${SOURCES})

# Если нужно подключить внешние библиотеки
target_link_libraries(gravity_ITRF PRIVATE ${GeographicLib_LIBRARIES})

# Укажите флаги компиляции
set_target_properties(gravity_ITRF PROPERTIES
        POSITION_INDEPENDENT_CODE ON
)

# Последовательность команд для cmake файла
#   mkdir build
#   cd build
#   cmake ..
#   make
