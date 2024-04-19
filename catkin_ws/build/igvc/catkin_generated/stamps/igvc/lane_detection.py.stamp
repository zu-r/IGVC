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

        # Convert image to HLS
        hls_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HLS)

        # Normalize HLS values
        normalized_hls = cv2.normalize(hls_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Apply Gaussian blurring
        blurred_image = cv2.GaussianBlur(normalized_hls, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred_image, 25, 120)

        # Define a region of interest
        height, width = edges.shape[:2]
        region_of_interest_vertices = [
            (0, height),
            (width * 0.01, height * 0.4),  # Top-left corner
            (width * 0.98, height * 0.4),
            (width, height)
        ]
        mask = np.zeros_like(edges)
        cv2.fillPoly(mask, [np.array(region_of_interest_vertices, dtype=np.int32)], 255)
        cropped_edges = cv2.bitwise_and(edges, mask)

        # Apply Hough transform
        lines = cv2.HoughLinesP(cropped_edges, rho=1, theta=np.pi/180, threshold=130, minLineLength=40, maxLineGap=25)

        # Generate line image
        line_image = np.zeros_like(cv_image)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # Combine input image with lane lines
        output_image = cv2.addWeighted(cv_image, 0.8, line_image, 1, 0)

        # Display or save the output image
        cv2.imshow('Output Image', output_image)
        cv2.waitKey(1)  # Note: use a non-zero value to allow image to show
        

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
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
