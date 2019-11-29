#!/usr/bin/env python
import rospy
import time
import smach
from smach_ros import IntrospectionServer
from uchile_srvs.srv import PersonDetection, PersonDetectionRequest
from sensor_msgs.msg import Image

from maqui_skills import robot_factory
from uchile_states.interaction.states import Speak
from uchile_states.perception.school import QRDetectorWeb, AnswerSelectionWeb

class Setup(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self,outcomes=["succeeded","aborted"]) # Aca se ponen todas las salidas que pueden tener este estado
        self.robot=robot
        self.tts=self.robot.get("tts")
        #self.skill=self.robot.get("skill")

    def execute(self,userdata): # Userdata es informacion que se puede mover entre estados
        self.tts.set_language("Spanish")
        self.tts.say("Inicio prueba de juego")
        self.tts.wait_until_done()
        

        #return "preemted" 
        #OJO esto genera un error debido a que en los outcomes definidos de las clase no se tiene el preemted , recomiendo ejecutar para ver el error
        return "succeeded"

class SaySelection(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self,outcomes=["succeeded","aborted"],io_keys=['answer']) # Aca se ponen todas las salidas que pueden tener este estado
        self.robot=robot
        self.tts=self.robot.get("tts")
        #self.skill=self.robot.get("skill")

    def execute(self,userdata): # Userdata es informacion que se puede mover entre estados
        self.tts.set_language("Spanish")
        text = "Alternativa seleccionada, " + userdata.answer 
        self.tts.say(text)
        self.tts.wait_until_done()
        

        #return "preemted" 
        #OJO esto genera un error debido a que en los outcomes definidos de las clase no se tiene el preemted , recomiendo ejecutar para ver el error
        return "succeeded"

class SayQR(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self,outcomes=["succeeded","aborted"],io_keys=['qr_id']) # Aca se ponen todas las salidas que pueden tener este estado
        self.robot=robot
        self.tts=self.robot.get("tts")
        #self.skill=self.robot.get("skill")

    def execute(self,userdata): # Userdata es informacion que se puede mover entre estados
        self.tts.set_language("Spanish")
        text = "Detectada, " + userdata.qr_id 
        self.tts.say(text)
        self.tts.wait_until_done()
        

        #return "preemted" 
        #OJO esto genera un error debido a que en los outcomes definidos de las clase no se tiene el preemted , recomiendo ejecutar para ver el error
        return "succeeded"


def getInstance(robot):
    sm =smach.StateMachine(outcomes=['succeeded','aborted','preemted'])


    with sm:
        smach.StateMachine.add('SETUP',Setup(robot),
            transitions={
                'succeeded':'INSTRUCTIONS_QR'
            }
        )
        smach.StateMachine.add('INSTRUCTIONS_QR',Speak(robot,"Cuando se le indique levante medallon con q r "),
            transitions={
                'succeeded':'QR_EXAMPLE'
            }
        )
        smach.StateMachine.add('QR_EXAMPLE',QRDetectorWeb(robot),
            transitions={
                'succeeded':'SAY_QR'
            }
        )
        smach.StateMachine.add('SAY_QR',SayQR(robot),
            transitions={
                'succeeded':'INSTRUCTIONS_ANSWER'
            },

        )
        smach.StateMachine.add('INSTRUCTIONS_ANSWER',Speak(robot,"Ahora se probara seleccion por brazo. Levante brazos para responder cuando se indique"),
            transitions={
                'succeeded':'SELECTION_EXAMPLE'
            }
        )
        smach.StateMachine.add('SELECTION_EXAMPLE',AnswerSelectionWeb(robot),
            transitions={
                'succeeded':'SAY_ANSWER'
            },

        )
        smach.StateMachine.add('SAY_ANSWER',SaySelection(robot),
            transitions={
                'succeeded':'FINISH'
            },

        )
        smach.StateMachine.add('FINISH',Speak(robot,"Muchas Gracias"),
            transitions={
                'succeeded':'succeeded'
            }
        )
    return sm


if __name__ == '__main__':
    rospy.init_node('rt_detection_state')

    robot= robot_factory.build([
        "audition",
        "tts"],core=True)

    sm = getInstance(robot)


    sis = IntrospectionServer('example_state', sm, '/EA_INIT_STATE') #Smach Viewer
    sis.start()
    outcome = sm.execute()
    sis.stop()