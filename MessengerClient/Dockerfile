# Use an older Ubuntu version with compatible glibc
FROM ubuntu:18.04

# Install required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    qt5-default \
    qttools5-dev \
    qttools5-dev-tools \
    libgl1-mesa-dev \
    libxkbcommon-x11-0 \
    && apt-get clean


# Install a newer version of CMake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-linux-x86_64.sh -O /tmp/cmake.sh \
    && chmod +x /tmp/cmake.sh \
    && /tmp/cmake.sh --skip-license --prefix=/usr/local \
    && rm /tmp/cmake.sh


# Download linuxdeployqt
RUN wget https://github.com/probonopd/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage -O /usr/local/bin/linuxdeployqt \
    && chmod +x /usr/local/bin/linuxdeployqt

# Download appimagetool
RUN wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage -O /usr/local/bin/appimagetool \
    && chmod +x /usr/local/bin/appimagetool

# Set the working directory
WORKDIR /app