cmake_minimum_required(VERSION 3.16)

project(MessengerClient VERSION 0.1 LANGUAGES CXX)

# Set default build type to Debug if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the build type (Debug, Release, RelWithDebInfo, MinSizeRel)" FORCE)
endif()

# Enable Qt auto features
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# Set RPATH for installation
set(CMAKE_INSTALL_RPATH "/lib")

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required Qt components
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets Network)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets Network)

# Enable debug output for qDebug()
add_definitions(-DQT_MESSAGELOGCONTEXT)

# Headers and UI files
set(HEADERS
    mainwindow.h
)

set(UIS
    mainwindow.ui
)

# Source files
set(PROJECT_SOURCES
    main.cpp
    mainwindow.cpp
    apiclient.cpp
    mainwindow.h
    apiclient.h
    mainwindow.ui
)

# Add executable
if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(MessengerClient
        MANUAL_FINALIZATION
        ${PROJECT_SOURCES}
    )
else()
    add_executable(MessengerClient
        ${PROJECT_SOURCES}
    )
endif()

# Link libraries
target_link_libraries(MessengerClient PRIVATE Qt${QT_VERSION_MAJOR}::Widgets Qt${QT_VERSION_MAJOR}::Network)

# Set target properties
set_target_properties(MessengerClient PROPERTIES
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

# Install rules
include(GNUInstallDirs)
install(TARGETS MessengerClient
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Finalize executable for Qt6
if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(MessengerClient)
endif()