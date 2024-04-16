#!/usr/bin/env python

import pygame
from geometry_msgs.msg import Twist
import rospy

pygame.init()
BLACK = (0,0,0)
WIDTH = 1280
HEIGHT = 1024
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
windowSurface.fill(BLACK)

pub = rospy.Publisher('mobile_base_controller/cmd_vel', Twist, queue_size=10)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
    
    t = Twist()
    t.linear.x = 0
    t.angular.z = 0
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP]:
        t.linear.x += 1
    if keys[pygame.K_DOWN]:
        t.linear.x -= 1
    if keys[pygame.K_LEFT]:
        t.angular.z +=1
    if keys[pygame.K_RIGHT]:
        t.angular.z -=1

    pub.publish(t)
    rate.sleep()
    pygame.event.pump()


# #!/usr/bin/env python

# import rospy
# from std_msgs.msg import String
# from geometry_msgs.msg import Twist

# def commands_callback(msg):
#     global t

#     command = msg.data

#     if command == "GO":
#         t.linear.x = 1.0
#         t.angular.z = 0.0
#     elif command == "GO_REALLY_FAST":
#         t.linear.x = 10.0  # Adjust as needed
#         t.angular.z = 0.0
#     elif command == "BACK":
#         t.linear.x = -0.5
#         t.angular.z = 0.0
#     elif command == "LEFT":
#         t.linear.x = 0.0
#         t.angular.z = 1.0
#     elif command == "RIGHT":
#         t.linear.x = 0.0
#         t.angular.z = -1.0
#     else:
#         t.linear.x = 0.0
#         t.angular.z = 0.0

#     pub.publish(t)

# if __name__ == '__main__':
#     rospy.init_node('motor_controller', anonymous=True)
#     pub = rospy.Publisher('mobile_base_controller/cmd_vel', Twist, queue_size=10)
#     rospy.Subscriber('motor_commands', String, commands_callback)

#     t = Twist()
#     t.linear.x = 0.0
#     t.angular.z = 0.0

#     rate = rospy.Rate(10)  # 10hz

#     while not rospy.is_shutdown():
#         rate.sleep()