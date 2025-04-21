cmake_minimum_required(VERSION 2.8.3)

project(six)

find_package(catkin REQUIRED)

catkin_package()

find_package(roslaunch)
install(FILES
  worlds/testmap.world
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/worlds
)

foreach(dir config launch meshes urdf)
	install(DIRECTORY ${dir}/
		DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)
