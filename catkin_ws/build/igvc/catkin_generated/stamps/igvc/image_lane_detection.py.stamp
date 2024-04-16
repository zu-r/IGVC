#!/usr/bin/python3

	
#roslib.load_manifest('./my_package.xml')
import rospy
import message_filters
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
 



def __init__(self):
    # Publish two nodes, each with it's own lane detection graphics
    self.image_left_pub = rospy.Publisher('lane_detection_left', Image)
    self.image_right_pub = rospy.Publisher('lane_detection_right', Image)
    self.bridge = CvBridge()
 
    # Subscribe to two camera ROS nodes
    self.image_left_sub = message_filters.Subscriber("/laser_object/depth/image_raw", Image)
    self.image_right_sub = message_filters.Subscriber("/laser_object/depth/image_raw", Image)
 
    # Syncronize the camera data we get from rosbag 
    ts = message_filters.ApproximateTimeSynchronizer([self.image_left_sub, self.image_right_sub], 10, 0.2)
    ts.registerCallback(self.callback)



def callback(self, left, right):
    try:
      cv_left_image = self.bridge.imgmsg_to_cv2(left, "bgr8")
      cv_right_image = self.bridge.imgmsg_to_cv2(right, "bgr8")
            
    except CvBridgeError as e:
      print(e)








