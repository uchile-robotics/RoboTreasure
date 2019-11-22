#!/usr/bin/env python

import rospy
import rospkg

import zbar

import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from uchile_srvs.srv import PersonDetection, PersonDetectionResponse
from PIL import Image as IMAGE

class QrDetectorServer:

	def __init__(self):
		self.bridge = CvBridge()
		rospy.Service('/qr_detector', PersonDetection, self.detect)


	def detect(self, req):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(req.image, "bgr8")
		except CvBridgeError as e:
			print(e)

		resp = PersonDetectionResponse()
		cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		image = IMAGE.fromarray(cv_image)
		width, height = image.size
		zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())
		# Scans the zbar image.
		scanner = zbar.ImageScanner()
		scanner.scan(zbar_image)
		for decoded in zbar_image:
			resp.labels.append(decoded.data)
		return resp


if __name__ == "__main__":
	rospy.init_node('qr_detector_server')
	detector = QrDetectorServer()
	rospy.loginfo("QR detector server up!")
	rospy.spin()
