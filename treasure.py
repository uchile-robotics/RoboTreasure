#!/usr/bin/env python
import rospy
import smach
import smach_ros
from smach_ros import IntrospectionServer
from std_msgs.msg import String
import time

#Robot building
from maqui_skills import robot_factory
from maqui_skills.capabilities.tablet import TabletControllerSkill

#States
from uchile_states.navigation.states import GoState
from uchile_states.interaction.states import Speak
from uchile_states.interaction.tablet_states import ShowWebpage, WaitTouchScreen
from uchile_states.perception.school import QRDetector, AnswerSelection
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

class SingleSub(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded"], io_keys=["qr"])
        self.robot = robot

    def execute(self, userdata):
        qr = rospy.wait_for_message("qr", String)
        userdata.qr = qr
        print qr
        return "succeeded"

class ChangeURL(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded", "stage1", "stage2"], io_keys=["qr", "page", "base_page", "qr_id"])
        self.robot = robot

    def execute(self, userdata):
        qr_split = str(userdata.qr_id)
        qr_split = qr_split.split()
        print qr_split
        equipo = qr_split[1]
        stage = qr_split[3]
        userdata.page = userdata.base_page+"stage"+stage+"/"+equipo
        print "#####################"
        print "Equipo: "+equipo
        print "Stage: "+stage
        print "URL: "+userdata.page
        print "#####################"

        if stage == "1":
            return "stage1"
        elif stage == "2":
            return "stage2"
        elif stage == "3":
            return "stage3"

class LoadURL(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded"], io_keys=["page"])
        self.robot = robot

    def execute(self, userdata):
        global page
        page = userdata.page
        print "Page: "+page
        return "succeeded"

class Iterator(smach.State):
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded", "preempted"], io_keys=["question_count"])
        self.robot = robot

    def execute(self, userdata):
        print "########################"
        print "Question count: "+str(userdata.question_count)
        print "########################"
        if userdata.question_count < 2:
            userdata.question_count += 1
            return "preempted"
        elif userdata.question_count == 2:
            userdata.question_count = 0
            time.sleep(20)
            return "succeeded"

class Questions(smach.State):
    """docstring for subs"""
    def __init__(self, robot):
        smach.State.__init__(self, outcomes=["succeeded", "preempted"])
        self.robot = robot
        self.tts = self.robot.get("tts")

    def execute(self, userdata):
        question = rospy.wait_for_message("question", String)
        print question
        question2 = str(question)
        question2 = question2.replace('data:', '')
        print question2
        if "end" in question2:
            time.sleep(20)
            return "preempted"
        self.tts.say_with_gestures(str(question2))
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
    start_place = 'start'
    RECEPTION_PLACE = 'start'
    JOHN_PLACE = 'near_couch'

    sm = smach.StateMachine(outcomes=['succeeded', 'aborted', 'preempted'])
    sm.userdata.qr = ""
    sm.userdata.page = "http://198.18.0.1:8888/stage1/r1"
    sm.userdata.base_page = "http://198.18.0.1:8888/"
    sm.userdata.qr_id = ""
    sm.userdata.question_count = 0

    with sm:

        smach.StateMachine.add('SETUP', Setup(robot),
            transitions={
                'succeeded':'PRE_WAIT'
            }
        )

        smach.StateMachine.add('PRE_WAIT', ShowWebpage(robot, page = "http://198.18.0.1:8888/b"),
            transitions={
                'succeeded':'WAIT',
                'preempted':'WAIT'
            }
        )

        smach.StateMachine.add('WAIT', WaitTouchScreen(robot),
            transitions={
                'succeeded':'QR'
            }
        )

        smach.StateMachine.add('QR', QRDetector(robot),
            transitions={
                'succeeded':'CHANGE_URL',
                'aborted':'QR'
            }
        )

        smach.StateMachine.add('CHANGE_URL', ChangeURL(robot),
            transitions={
                'stage1':'WEB_SHOW_1',
                'stage2':'SPEAK_2',
                # 'stage3':'WEB_SHOW_3',
            }
        )

################################################

                    #STAGE1#

################################################

        smach.StateMachine.add('WEB_SHOW_1', ShowWebpage(robot),
            transitions={
                'succeeded':'HEAR_QUESTIONS_1'
            }
        )

        smach.StateMachine.add('HEAR_QUESTIONS_1', Questions(robot),
            transitions={
                'succeeded':'HEAR_QUESTIONS_1',
                'preempted':'PRE_WAIT'
            }
        )

################################################

                    #STAGE2#

################################################

        smach.StateMachine.add('SPEAK_2', Speak(robot, "Felicitaciones, estan en la etapa 2. En esta parte para seleccionar la respueta deben presionar el boton y luego escoger con la pose adecuada"),
            transitions={
                'succeeded' : 'WEB_SHOW_2'
            }
        )

        smach.StateMachine.add('WEB_SHOW_2', ShowWebpage(robot),
            transitions={
                'succeeded':'HEAR_QUESTIONS_1'
            }
        )

        smach.StateMachine.add('HEAR_QUESTIONS_2', Questions(robot),
            transitions={
                'succeeded':'HEAR_QUESTIONS_2',
                'preempted':'PRE_WAIT'
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
