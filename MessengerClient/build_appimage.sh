#!/bin/bash

# Build the Docker image
docker build -t qt-appimage-builder .

# Run the container and build the AppImage
docker run --rm -v $(pwd):/app qt-appimage-builder bash -c "
    cd /app &&
    rm -rf build &&
    mkdir build &&
    cd build &&
    cmake .. &&
    make &&
    mkdir -p MessengerClient.AppDir/usr/bin &&
    cp ./MessengerClient MessengerClient.AppDir/usr/bin/ &&
    linuxdeployqt MessengerClient.AppDir/usr/bin/MessengerClient -appimage &&
    cp MessengerClient-x86_64.AppImage /app
"