#!/usr/bin/env python
import rospy
import smach
import smach_ros
from smach_ros import IntrospectionServer
from std_msgs.msg import String

#Robot building
from maqui_skills import robot_factory
from maqui_skills.capabilities.tablet import TabletControllerSkill

#States
from uchile_states.navigation.states import GoState
from uchile_states.interaction.states import Speak
from uchile_states.interaction.tablet_states import ShowWebpage
#########from uchile_states.interaction.tablet_states import OperationMessage



class Setup(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self, outcomes=["succeeded"])
        self.robot = robot
        self.tts = self.robot.get("tts")
        self.head = self.robot.get("neck")
        self.track = self.robot.get("track_person")
        self.audition = self.robot.get("audition")
        self.knowledge = self.robot.get("knowledge")
        self.facial_features   = self.robot.get("facial_features")
        self.face   = self.robot.get("face")
        # self.track = self.robot.get("track_person")
    def execute(self,userdata):
        # self.track.set_search(False)
        self.tts.set_language("Spanish")
        # self.tts.set_speed(110)
        self.audition.set_audio_expression(False)
        self.knowledge.pose.delete_all()
        self.knowledge.pose.load_from_map("receptionist.sem_map")
        self.head.home()  
        self.face.turn_on()
        self.facial_features.clear_face_database()
        self.facial_features._set_resolution(4)
        return 'succeeded'

class Subs(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded"])
        self.robot = robot

    def callback(self, data):
        print data.data
        return "succeeded"

    def execute(self, userdata):
        rospy.Subscriber("qr", String, self.callback)

class SingleSub(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded"])
        self.robot = robot

    def execute(self, userdata):
        qr = rospy.wait_for_message("qr", String)
        print qr
        return "succeeded"

class Questions(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded"])
        self.robot = robot
        self.tts = self.robot.get("tts")

    def execute(self, userdata):
        question = rospy.wait_for_message("question", String)
        print question
        print type(question)
        self.tts.say_with_gestures(str(question))
        return "succeeded"

class Image(smach.State):
    skill_req = []
    def __init__(self, robot, url=None, timeout=5):
        
        self.tablet = robot.get("tablet")
        self.url = url
        input_keys = ['url'] if self.url is None else []
        smach.State.__init__(self, 
                                outcomes=["succeeded","preempted"], 
                                input_keys=input_keys)
    
    def execute(self, userdata):

        url = userdata.url if self.url is None else self.url
        self.tablet.wakeUp()
        if self.tablet.show_image(url):
            return "succeeded"
    
        return "preempted"



def getInstance(robot):
    """
    parameters of the test:
        *Places of interaction:
            -START
            -RECEPTION
            -LIVING

    """
    start_place = 'start'
    RECEPTION_PLACE = 'start'
    JOHN_PLACE = 'near_couch'

    sm = smach.StateMachine(outcomes=['succeeded', 'aborted', 'preempted'])
    sm.userdata.qr = ""
    sm.userdata.page = "http://198.18.0.1:8888/"

    with sm:

        smach.StateMachine.add('SETUP', Setup(robot),
            transitions={
                'succeeded':'WEB_SHOW'
            }
        )

        smach.StateMachine.add('QR', SingleSub(robot),
            transitions={
                'succeeded':'WEB_SHOW'
            }
        )

        # smach.StateMachine.add('WEB_SHOW', Image(robot, url="http://198.18.0.1:8888/home/nao/uchile_last_ws/src/uchile_robocup/src/uchile_robocup/yay.jpg"),
        #     transitions={
        #         'succeeded':'succeeded'
        #     }
        # )

        smach.StateMachine.add('WEB_SHOW', ShowWebpage(robot, page = "http://198.18.0.1:8888/"),
            transitions={
                'succeeded':'HEAR_QUESTIONS'
            }
        )

        smach.StateMachine.add('HEAR_QUESTIONS', Questions(robot),
            transitions={
                'succeeded':'HEAR_QUESTIONS'
            }
        )




        return sm

if __name__ == '__main__':

    rospy.init_node('TREASURE')
    base_skills = [ 
        "audition",
        "marker",
        "tablet",
        "tabletapp",
        'knowledge',
        "navigation",
        "person_detector",
        "facial_features",
        "l_arm",
        "r_arm"]#,
        #"sitting_person_detector"] not sure if we need this

    extra_skills = []

    robot = robot_factory.build( base_skills + extra_skills, core = True)

    sm = getInstance(robot)
    sis = IntrospectionServer('treasure', sm, '/TREASURE_SM') #Smach Viewer
    sis.start()
    outcome = sm.execute() # here is where the test begin
    sis.stop()
