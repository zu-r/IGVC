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

        # Convert image to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blur, 50, 150)

        # Define region of interest
        mask = np.zeros_like(edges)
        height, width = edges.shape
        polygon = np.array([[(0, height), (width, height), (width // 2, height // 2)]], dtype=np.int32)
        cv2.fillPoly(mask, polygon, 255)
        masked_edges = cv2.bitwise_and(edges, mask)

        # Perform Hough Transform
        lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=50)

        if lines is not None:  # Check if lines are detected
            # Draw detected lane lines
            left_line, right_line = self.lane_lines(cv_image, lines)
            lane_lines_image = self.draw_lane_lines(cv_image, [left_line, right_line])

            # Display the annotated image
            cv2.imshow("Annotated Image", lane_lines_image)
            cv2.waitKey(3)

            # Publish the annotated image
            try:
                self.image_pub.publish(self.bridge.cv2_to_imgmsg(lane_lines_image, "bgr8"))
            except CvBridgeError as e:
                print(e)
        else:
            print("No lines detected")  # Handle case when no lines are detected

    def average_slope_intercept(self, lines):
        """
        Find the slope and intercept of the left and right lanes of each image.
        Parameters:
            lines: output from Hough Transform
        """
        left_lines = []  # (slope, intercept)
        left_weights = []  # (length,)
        right_lines = []  # (slope, intercept)
        right_weights = []  # (length,)

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    continue
                # calculating slope of a line
                slope = (y2 - y1) / (x2 - x1)
                # calculating intercept of a line
                intercept = y1 - (slope * x1)
                # calculating length of a line
                length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
                # slope of left lane is negative and for right lane slope is positive
                if slope < 0:
                    left_lines.append((slope, intercept))
                    left_weights.append((length))
                else:
                    right_lines.append((slope, intercept))
                    right_weights.append((length))
        #
        left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
        right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
        return left_lane, right_lane

    def pixel_points(self, y1, y2, line):
        """
        Converts the slope and intercept of each line into pixel points.
        Parameters:
            y1: y-value of the line's starting point.
            y2: y-value of the line's end point.
            line: The slope and intercept of the line.
        """
        if line is None:
            return None
        slope, intercept = line
        if slope == 0:
            return None
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
        y1 = int(y1)
        y2 = int(y2)
        return ((x1, y1), (x2, y2))
    
    
    def lane_lines(self, image, lines):
        """
        Create full length lines from pixel points.
        Parameters:
            image: The input test image.
            lines: The output lines from Hough Transform.
        """
        left_lane, right_lane = self.average_slope_intercept(lines)
        y1 = image.shape[0]
        y2 = y1 * 0.6
        
        # Additional filtering to consider only solid lines
        if left_lane is not None and right_lane is not None:
            left_slope, _ = left_lane
            right_slope, _ = right_lane
            # Define slope thresholds for solid lines
            slope_threshold = 0.3
            if abs(left_slope) > slope_threshold and abs(right_slope) > slope_threshold:
                left_line = self.pixel_points(y1, y2, left_lane)
                right_line = self.pixel_points(y1, y2, right_lane)
                return left_line, right_line
        
        return None, None


    def draw_lane_lines(self, image, lines, color=[255, 0, 0], thickness=12):
        """
        Draw lines onto the input image.
        Parameters:
            image: The input test image (video frame in our case).
            lines: The output lines from Hough Transform.
            color (Default = red): Line color.
            thickness (Default = 12): Line thickness.
        """
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                cv2.line(line_image, *line, color, thickness)
        return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

def main(args):
    ic = image_converter()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
