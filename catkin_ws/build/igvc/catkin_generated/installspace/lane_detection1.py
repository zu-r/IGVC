#!/usr/bin/python3
from __future__ import print_function

import roslib
roslib.load_manifest('igvc')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class lane_detection:

    def __init__(self):
        rospy.init_node('lane_detection', anonymous=True)
        self.image_pub = rospy.Publisher("laser_object/depth/image_raw_4", Image, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("laser_object/depth/image_raw", Image, self.callback)
        
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            return
    
        # Apply Gaussian blur filter:
        frame = cv2.GaussianBlur(cv_image, (5, 5), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper yellow color thresholds
        lower_white = np.array([0, 0, 180])  # Adjust the saturation and value to your preference
        upper_white = np.array([180, 50, 255]) 

        # Create a mask using the white color thresholds
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # Apply Canny edge detection to the masked image
        edges = cv2.Canny(mask, 74, 150)

        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)

        # Draw detected lines on the frame
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)  # Drawing lines
            
        # Display the frame with detected lines and edges
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        cv2.imshow("edges", edges)
        cv2.waitKey(1)
        key = cv2.waitKey(25)


        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)



def main(args):
    ld = lane_detection()  # Create instance of lane_detection class
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
