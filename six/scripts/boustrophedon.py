#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
import numpy as np

class Boustrophedon:
    def __init__(self):
        rospy.init_node('boustrophedon', anonymous=True)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.map_sub = rospy.Subscriber('/map', OccupancyGrid, self.map_callback)
        self.twist = Twist()
        self.rate = rospy.Rate(10)
        self.direction = 0  # 0: thẳng, 1: quay
        self.map_data = None
        self.step_size = 1.0  # Khoảng cách giữa các đường zigzag

    def scan_callback(self, data):
        # Kiểm tra chướng ngại phía trước
        front_dist = min([r for r in data.ranges[:30] + data.ranges[-30:] if r > 0], default=float('inf'))
        if front_dist < 1.0:
            self.direction = 1  # Chuyển sang quay
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.5
        else:
            self.direction = 0  # Tiếp tục thẳng
            self.twist.linear.x = 0.2
            self.twist.angular.z = 0.0

    def map_callback(self, data):
        self.map_data = data

    def run(self):
        while not rospy.is_shutdown():
            if self.direction == 1 and self.twist.angular.z == 0.0:
                # Hoàn thành quay, chuyển sang đường mới
                self.twist.linear.x = 0.2
                self.twist.angular.z = 0.0
                self.direction = 0
            self.cmd_vel_pub.publish(self.twist)
            self.rate.sleep()

if __name__ == '__main__':
    try:
        planner = Boustrophedon()
        planner.run()
    except rospy.ROSInterruptException:
        pass
