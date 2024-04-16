import roslib  # Import the roslib package
roslib.load_manifest('igvc')  # Load the manifest for the 'igvc' package
import sys  # Import the sys module
import rospy  # Import the rospy package (ROS Python client library)
import cv2  # Import the OpenCV library (cv2)
import numpy as np  # Import NumPy library
from std_msgs.msg import String  # Import the String message type from std_msgs
from sensor_msgs.msg import Image as ImageMsg  # Import the Image message type from sensor_msgs and rename it to avoid conflicts
from cv_bridge import CvBridge, CvBridgeError  # Import CvBridge for converting between ROS Image messages and OpenCV images
from PIL import Image  # Import the Image module from PIL library for image processing

class object_detection:
    orange = [0, 165, 255]  # Define the color orange in BGR colorspace

    # Constructor method (__init__) for object_detection class
    def __init__(self):
        rospy.init_node('object_detection', anonymous=True)  # Initialize a ROS node named 'object_detection'
        self.image_pub = rospy.Publisher("laser_object/depth/image_raw_2", ImageMsg, queue_size=10)  # Create a publisher for image messages
        self.bridge = CvBridge()  # Initialize CvBridge for image conversion
        self.image_sub = rospy.Subscriber("laser_object/depth/image_raw", ImageMsg, self.callback)  # Create a subscriber for image messages

    # Callback method to handle incoming image messages
    def callback(self, data):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")  # Convert ROS Image message to OpenCV image format
        except CvBridgeError as e:
            print(e)
            return

        hsvImage = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)  # Convert BGR image to HSV color space

        lowerLimit, upperLimit = self.get_limits(color=self.orange)  # Get lower and upper color limits for orange

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)  # Create a mask using color limits

        mask_ = Image.fromarray(mask)  # Convert mask to PIL Image format

        bbox = mask_.getbbox()  # Get bounding box of the mask

        if bbox is not None:  # Check if bounding box exists
            x1, y1, x2, y2 = bbox  # Extract coordinates of the bounding box

            frame = cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 5)  # Draw a rectangle around the detected object

        cv2.imshow('frame', cv_image)  # Display the image with detected objects
        cv2.waitKey(1)  # Wait for a short time

    # Method to calculate lower and upper color limits based on a given color
    def get_limits(self, color):
        c = np.uint8([[color]])  # Convert color to NumPy array (BGR format)
        hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)  # Convert BGR color to HSV color space

        hue = hsvC[0][0][0]  # Get the hue value from the converted color

        # Handle red hue wrap-around
        if hue >= 165:  # Upper limit for divided red hue
            lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
            upperLimit = np.array([180, 255, 255], dtype=np.uint8)
        elif hue <= 15:  # Lower limit for divided red hue
            lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
            upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        else:  # Regular case
            lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
            upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

        return lowerLimit, upperLimit  # Return the calculated lower and upper color limits

# Main function to initialize the object_detection class and start the ROS node
def main(args):
    ic = object_detection()  # Create an instance of the object_detection class
    try:
        rospy.spin()  # Keep the node running until shutdown
    except KeyboardInterrupt:
        print("Shutting down")  # Handle keyboard interrupt
    cv2.destroyAllWindows()  # Close OpenCV windows when the node shuts down

# Entry point of the script
if __name__ == '__main__':
    main(sys.argv)  # Call the main function with command line arguments
