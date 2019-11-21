#!/usr/bin/env python

import rospy

from cv_bridge import CvBridge, CvBridgeError
import cv2

from std_msgs.msg import String
from sensor_msgs.msg import Image
from uchile_srvs.srv import PersonDetection, PersonDetectionRequest

class QrDetectorClient:

	def __init__(self):
		self.img_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.img_callback)
		self.rgb_image = None
		self.img_pub = rospy.Publisher("/qr_detector", String, queue_size=1)
		self.bridge = CvBridge()
		self.output = String()

	def img_callback(self, img_data):
		self.rgb_image = img_data


	def call_service(self):
		rospy.loginfo("Waiting...")
		self.output = String()
		if self.rgb_image is None:
			return
		rospy.wait_for_service('/qr_detector')
		try:
			server_client = rospy.ServiceProxy('/qr_detector', PersonDetection)
			request = PersonDetectionRequest()
			request.image = self.rgb_image
			detection = server_client(request)		
		except CvBridgeError as e:
			print(e)
		if detection.labels != []:
			self.output = detection.labels[0]
			rospy.loginfo(self.output)
		self.img_pub.publish(self.output)
		return 


if __name__ == "__main__":

	rospy.init_node('qr_detector_client')
	server_client = QrDetectorClient()

   
	while not rospy.is_shutdown():
		server_client.call_service()
		rospy.sleep(2.0)
