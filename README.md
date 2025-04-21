Gói ROS six
Gói six là một gói ROS Noetic để mô phỏng robot trong Gazebo, lập bản đồ bằng Gmapping, điều hướng bằng Move Base, và tự động khám phá bằng Explore Lite. Tài liệu này hướng dẫn cách cài đặt, cấu hình, và khắc phục lỗi hệ thống.
Mục lục

Yêu cầu
Cấu trúc thư mục
Các thành phần chính
Cài đặt
Cách sử dụng
Khắc phục lỗi
Tùy chỉnh
Tài liệu tham khảo
Liên hệ

Yêu cầu

Hệ điều hành: Ubuntu 20.04
ROS: Noetic
Gazebo: Phiên bản 11
Gói ROS cần thiết:sudo apt install ros-noetic-gazebo-ros ros-noetic-gmapping ros-noetic-move-base ros-noetic-explore-lite ros-noetic-xacro


Không gian làm việc: ~/catkin_ws với gói six trong ~/catkin_ws/src/six.

Cấu trúc thư mục
six/
├── config/
│   ├── costmap_common_params.yaml
│   ├── local_costmap_params.yaml
│   ├── global_costmap_params.yaml
│   └── base_local_planner_params.yaml
├── launch/
│   ├── robot.launch
│   ├── gmapping.launch
│   ├── move_base.launch
│   ├── explore.launch
│   ├── testmap.launch
│   └── all_in_one.launch (tùy chọn)
├── urdf/
│   └── six.urdf
├── worlds/
│   ├── testmap.world
│   └── stacks.world
├── maps/
│   └── my_map.yaml (tạo sau khi lưu bản đồ)
├── CMakeLists.txt
└── package.xml

Các thành phần chính

robot.launch: Khởi động Gazebo (mặc định: empty_world), sinh robot từ six.urdf, chạy joint_state_publisher và robot_state_publisher.
gmapping.launch: Chạy Gmapping để lập bản đồ từ dữ liệu LIDAR (/scan).
move_base.launch: Chạy Move Base để điều hướng, dùng cấu hình trong six/config/.
explore.launch: Chạy Explore Lite để robot tự động khám phá.
testmap.launch: Khởi động Gazebo với bản đồ tùy chỉnh testmap.world.
Bản đồ Gazebo:
empty_world: Thế giới trống, nhẹ nhất.
shapes.world: Hình khối đơn giản.
simple_office.world: Văn phòng nhỏ.
testmap.world: Tùy chỉnh với tường và bàn.
stacks.world: Tùy chỉnh với khối xếp chồng.



Cài đặt

Tạo không gian làm việc:
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace


Sao chép gói six:

Đặt gói six vào ~/catkin_ws/src/six.
Đảm bảo package.xml có phụ thuộc:<depend>gazebo_ros</depend>
<depend>gmapping</depend>
<depend>move_base</depend>
<depend>explore_lite</depend>
<depend>xacro</depend>




Cài đặt tệp cấu hình:

Tạo thư mục six/config/ và thêm:
costmap_common_params.yaml
local_costmap_params.yaml
global_costmap_params.yaml
base_local_planner_params.yaml


Tham khảo nội dung trong hướng dẫn trước.


Biên dịch:
cd ~/catkin_ws
catkin_make
source devel/setup.bash



Cách sử dụng

Khởi động mô phỏng:
roslaunch six robot.launch

Mở Gazebo với empty_world và sinh robot.

Chạy Gmapping:
roslaunch six gmapping.launch

Lập bản đồ từ dữ liệu LIDAR.

Chạy Move Base:
roslaunch six move_base.launch

Điều hướng robot.

Chạy Explore Lite:
roslaunch six explore.launch

Robot tự động khám phá.

Sử dụng bản đồ tùy chỉnh:

Chạy testmap.world:roslaunch six testmap.launch


Dùng shapes.world hoặc simple_office.world, chỉnh robot.launch:<node name="gazebo" pkg="gazebo_ros" type="gazebo_world" args="$(find gazebo_ros)/worlds/shapes.world" />
<node name="gazebo_gui" pkg="gazebo_ros" type="gazebo_gui" respawn="false" output="screen" />




Hiển thị trong RViz:
rosrun rviz rviz


Thêm hiển thị:
/map (Map)
/scan (LaserScan)
/move_base/global_costmap/costmap (Map)
/move_base/local_costmap/costmap (Map)
/explore/frontiers (Marker)


Đặt khung cố định: map.


Lưu bản đồ:
mkdir -p ~/catkin_ws/src/six/maps
rosrun map_server map_saver -f ~/catkin_ws/src/six/maps/my_map



Khắc phục lỗi
1. Gazebo không tải

Kiểm tra gazebo_ros:rospack find gazebo_ros
sudo apt install ros-noetic-gazebo-ros ros-noetic-gazebo-ros-pkgs


Đảm bảo Gazebo 11:gazebo --version
sudo apt install gazebo11 libgazebo11-dev


Xem nhật ký:cat ~/.ros/log/latest/roslaunch-*.log



2. Explore Lite báo "found 0 frontiers"

Nguyên nhân:
Bản đồ trống (như empty_world).
Gmapping không tạo bản đồ đúng.
Tham số Explore Lite không phù hợp.


Giải pháp:
Dùng bản đồ có chướng ngại vật (như shapes.world):<node name="gazebo" pkg="gazebo_ros" type="gazebo_world" args="$(find gazebo_ros)/worlds/shapes.world" />


Kiểm tra topic /scan và /map:rostopic echo /scan
rostopic echo /map


Tinh chỉnh explore.launch:<param name="min_frontier_distance" value="0.25"/>
<param name="progress_timeout" value="60.0"/>


Kiểm tra TF:rosrun tf view_frames





3. Robot không di chuyển

Kiểm tra /cmd_vel:rostopic echo /cmd_vel


Giảm inflation_radius trong costmap_common_params.yaml:inflation_radius: 0.3


Tăng dung sai trong base_local_planner_params.yaml:xy_goal_tolerance: 0.3
yaw_goal_tolerance: 0.2



4. Bản đồ Gmapping không chính xác

Tăng số hạt trong gmapping.launch:<param name="particles" value="100"/>


Giảm map_update_interval:<param name="map_update_interval" value="1.0"/>



Tùy chỉnh
1. Thay đổi bản đồ

Bản đồ có sẵn trong Gazebo:
empty_world: Trống, nhẹ nhất.
shapes.world: Hình khối đơn giản.
simple_office.world: Văn phòng nhỏ.


Kiểm tra:ls /usr/share/gazebo-11/worlds/



2. Tạo bản đồ tùy chỉnh

Tạo tệp .world trong six/worlds/ (như testmap.world, stacks.world).
Cập nhật CMakeLists.txt:install(FILES
  worlds/testmap.world
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/worlds
)



3. Gộp thành một tệp launch

Tạo all_in_one.launch để chạy Gazebo, Gmapping, Move Base, và Explore Lite cùng lúc. Tham khảo hướng dẫn trước.

Tài liệu tham khảo

ROS Noetic
Gazebo Tutorials
Gmapping
Move Base
Explore Lite
ROS Launch

Liên hệ
Nếu gặp lỗi, cung cấp:

Nhật ký lỗi (~/.ros/log/).
Nội dung six.urdf.
Dữ liệu topic (/scan, /odom, /map).
Yêu cầu cụ thể (bản đồ, cấu trúc, v.v.).

