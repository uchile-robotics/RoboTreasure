#!/usr/bin/env python
import sys
import getch
import rospy
from std_msgs.msg import String #String message 
from std_msgs.msg import Int8


################################
# created by yuvaram
#yuvaramsingh94@gmail.com
################################


def keys():
    pub = rospy.Publisher('key', Int8, queue_size=10) # "key" is the publisher name
    rospy.init_node('keypress', anonymous=True)
    rate = rospy.Rate(10)#try removing this line ans see what happens
    while not rospy.is_shutdown():
        k = ord(getch.getch())# this is used to convert the keypress event in the keyboard or joypad , joystick to a ord value
        if (k >= 65)&(k <= 68)|(k == 115)|(k == 113)|(k == 97):# to filter only the up , dowm ,left , right key /// this line can be removed or more key can be added to this
            rospy.loginfo(str(k))# to print on terminal
            pub.publish(k)#to publish


if __name__ == '__main__':
    try:
        keys()
    except KeyboardInterrupt:
        sys.exit(0)
