FROM osrf/ros:humble-desktop
ENV DEBIAN_FRONTEND=noninteractive

# 安裝 RealSense 套件
RUN apt-get update && apt-get install -y \
    ros-humble-realsense2-camera \
    ros-humble-realsense2-description \
    ros-humble-rviz2 \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
CMD ["bash"]