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

class image_converter:

    def __init__(self):
        rospy.init_node('image_converter', anonymous=True)
        self.image_pub = rospy.Publisher("laser_object/depth/image_raw_2", Image, queue_size=10)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("laser_object/depth/image_raw", Image, self.callback)

    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
            return

        # Convert image to HSV
        hsv_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # Define orange color range in HSV
        lower_orange1 = np.array([0, 135, 135])
        lower_orange2 = np.array([15, 255, 255])
        upper_orange1 = np.array([159, 135, 80])
        upper_orange2 = np.array([179, 255, 255])

        # Threshold the HSV image to get only bright orange colors
        imgThreshLow = cv2.inRange(hsv_img, lower_orange1, lower_orange2)
        imgThreshHigh = cv2.inRange(hsv_img, upper_orange1, upper_orange2)

        # Bitwise-OR low and high thresholds
        threshed_img = cv2.bitwise_or(imgThreshLow, imgThreshHigh)

        # Smoothing operations
        kernel = np.ones((5,5),np.uint8)
        threshed_img_smooth = cv2.erode(threshed_img, kernel, iterations = 3)
        threshed_img_smooth = cv2.dilate(threshed_img_smooth, kernel, iterations = 2)
        smoothed_img = cv2.dilate(threshed_img_smooth, kernel, iterations = 11)
        smoothed_img = cv2.erode(smoothed_img, kernel, iterations = 7)

        # Detect edges
        edges_img = cv2.Canny(smoothed_img, 100, 200)
        contours, hierarchy = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 2
        fontColor = (0, 0, 255)
        lineType = 2

        for cnt in contours:
            boundingRect = cv2.boundingRect(cnt)
            approx = cv2.approxPolyDP(cnt, 0.06 * cv2.arcLength(cnt, True), True)
            if len(approx) == 3:
                x, y, w, h = cv2.boundingRect(approx)
                rect = (x, y, w, h)
                cv2.rectangle(cv_image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                bottomLeftCornerOfText = (x, y)
                cv2.putText(cv_image, 'traffic_cone', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)

        # Display the annotated image
        cv2.imshow("Annotated Image", cv_image)
        cv2.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        except CvBridgeError as e:
            print(e)

def main(args):
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
