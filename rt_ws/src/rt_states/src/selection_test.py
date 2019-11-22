#!/usr/bin/env python
import rospy
import time
import smach
from smach_ros import IntrospectionServer
from uchile_srvs.srv import PersonDetection, PersonDetectionRequest
from sensor_msgs.msg import Image

from maqui_skills import robot_factory
from uchile_states.interaction.states import Speak 

class Setup(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self,outcomes=["succeeded","aborted"]) # Aca se ponen todas las salidas que pueden tener este estado
        self.robot=robot
        self.audition=self.robot.get("audition")
        self.tts=self.robot.get("tts")
        #self.skill=self.robot.get("skill")

    def execute(self,userdata): # Userdata es informacion que se puede mover entre estados
        self.tts.set_language("Spanish")
        self.tts.say("Inicio prueba de deteccion de alternativas")
        self.tts.wait_until_done()
        

        #return "preemted" 
        #OJO esto genera un error debido a que en los outcomes definidos de las clase no se tiene el preemted , recomiendo ejecutar para ver el error
        return "succeeded"


class Example(smach.State):
    def __init__(self,robot):
        smach.State.__init__(self,outcomes=["succeeded","aborted"]) # Aca se ponen todas las salidas que pueden tener este estado
        self.robot=robot
        self.audition=self.robot.get("audition")
        self.tts=self.robot.get("tts")
        #self.skill=self.robot.get("skill")

    def execute(self,userdata): # Userdata es informacion que se puede mover entre estados

        server_client = rospy.ServiceProxy('/selection_detector/detect', PersonDetection)
        request = PersonDetectionRequest()

        self.tts.say("Ahora indique la alternativa seleccionada")
        self.tts.wait_until_done()
        time.sleep(2)

        request.image = rospy.wait_for_message("/maqui/camera/front/image_raw", Image)
        detections = server_client(request)

        print(detections.labels)
        if len(detections.labels)>0:
            self.tts.say("Alternativa seleccionada, {}".format(detections.labels[0]))
        else:
            self.tts.say("Ninguna alternativa seleccionada")
        self.tts.wait_until_done()
        #return "preemted" 
        #OJO esto genera un error debido a que en los outcomes definidos de las clase no se tiene el preemted , recomiendo ejecutar para ver el error
        return "succeeded"


def getInstance(robot):
    sm =smach.StateMachine(outcomes=['succeeded','aborted','preemted'])


    with sm:
        smach.StateMachine.add('SETUP',Setup(robot),
            transitions={
                'succeeded':'INSTRUCTIONS'
            }
        )
        smach.StateMachine.add('INSTRUCTIONS',Speak(robot,"Cuando se le indique seleccione alternativa. Levante brazo izquierdo para letra a. Levante brazo derecho  para letra b. Levante ambos para letra c. "),
            transitions={
                'succeeded':'EXAMPLE1'
            }
        )
        smach.StateMachine.add('EXAMPLE1',Example(robot),
            transitions={
                'succeeded':'EXAMPLE2'
            }
        )
        smach.StateMachine.add('EXAMPLE2',Example(robot),
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