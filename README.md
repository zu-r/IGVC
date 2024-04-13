instructions for ROS installation:

MacOS (M1): 
https://medium.com/robostack/cross-platform-conda-packages-for-ros-fa1974fd1de3
https://www.youtube.com/watch?app=desktop&v=zF7Pbq4Puvg


Windows: https://wiki.ros.org/noetic/Installation/Windows

Ubuntu (ideally use Ubuntu): https://wiki.ros.org/noetic/Installation/Ubuntu

to setup your workspace, run these commands in your terminal:

    mkdir -p ~/catkin_ws/src  
    cd ~/catkin_ws/src
    catkin_create_pkg igvc
    cd ~/catkin_ws
    catkin build

this creates a folder named catkin_ws, and creates a package named igvc

now copy the config, launch, rviz, scripts, and urdf folders from the github into igvc folder (will be in catkin_ws/src/igvc/)

go inside your catkin_ws/src/igvc/CMakeLists.txt, and look for catkin_install_python(PROGRAMS      this line should be commented out

replace it with 

    catkin_install_python(PROGRAMS
      scripts/lane_detection2
      scripts/lane_detection
      scripts/object_detection
      DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
    )

now run

    cd ~/catkin_ws
    catkin build


your environment should now be all setup

to run a gazebo simulation, run these commands:
   
    cd ~/catkin_ws
    source devel/setup.bash OR source devel/setup.zsh  (depending on if you are using bash or zsh terminal)
    roslaunch igvc diffdrive.launch
