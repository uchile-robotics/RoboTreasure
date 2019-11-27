import tornado.ioloop
import tornado.web
import tornado.websocket

import socket
import os.path

#from std_msgs.msg import String
#import rospy

from tornado.options import define, options, parse_command_line

define("port", default=8888, type=int)
# Carpetas para archivos statics e html's
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)
# Clase que renderiza el index (html con el websocket)
class MainHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        print "setting headers for main page!!!"
        #self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://198.18.0.2:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://198.18.0.1:8888/")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        self.render("index.html")

class WhiteHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        print "setting headers for main page!!!"
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://198.18.0.2:8888/")
        self.set_header("Access-Control-Allow-Origin", "http://198.18.0.1:8888/")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.render("blank.html")
        print "head finish"

    def get(self):
        print "loading blank html"
        self.render("blank.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
      
    def on_message(self, message):
        message = message.encode('ascii', 'ignore').decode('ascii')
        print 'message received:  %s' % message
        pub = rospy.Publisher('/question', String, queue_size=10)
        rospy.init_node("hola")
        pub.publish(message)
        # Reverse Message and send it back
        # print 'sending back message: %s' % message[::-1]
        # self.write_message(message[::-1])

    def on_close(self):
        print 'connection closed'

    def check_origin(self, origin):
        return True


class CommandHandler(tornado.web.RequestHandler):
    #both GET and POST requests have the same responses
    def set_default_headers(self):
        print "setting headers!!!"
        #self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Origin", "http://127.0.0.1:8888/com?op=kill_roscore")
        self.set_header("Access-Control-Allow-Origin", "http://127.0.0.1:8888/com?op=run_roscore")
        self.set_header("Access-Control-Allow-Origin", "http://127.0.0.1:8888/com?op=spr_launcher")
        self.set_header("Access-Control-Allow-Origin", "http://127.0.0.1:8888/com?op=spr_test")
        self.set_header("Access-Control-Allow-Origin", "http://127.0.0.1:8888/com?op=spr_kill")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        #self.set_header("Access-Control-Allow-Headers", "access-control-allow-origin,authorization,content-type")


    def get(self, url = '/'):
        print "get"
        self.handleRequest()

    def post(self, url = '/'):
        print 'post'
        self.handleRequest()

    # handle both GET and POST requests with the same function
    def handleRequest( self ):
        # is op to decide what kind of command is being sent
        op = self.get_argument('op',None)
        print op

        #received a "checkup" operation command from the browser:
        if op == "dummy":
            print "dummy"

#$%&Signal DO NOT ERASE

        elif op == "spr_launcher":
            spr_launcher()
            print 'yay: spr_launcher'
                        
        elif op == "spr_test":
            spr_test()
            print 'yay: spr_test'
                        
        elif op == "spr_test_kill":
            spr_test_kill()
            print 'yay: spr_test_kill'
                        
        elif op == "spr_launcher_kill":
            spr_launcher_kill()
            print 'yay: spr_launcher_kill'
                        
        elif op == "run_roscore":
            run_roscore()
            print 'yay: run_roscore'
                        
        elif op == "kill_roscore":
            kill_roscore()
            print 'yay: kill_roscore'
                        
#ENDSIGNAL

        #operation was not one of the ones that we know how to handle
        else:
            print op
            print self.request
            raise tornado.web.HTTPError(404, "Missing argument 'op' or not recognized")

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

# Url's
app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/b', WhiteHandler),
    (r'/(com.*)', CommandHandler),
    (r'/(launch_details\.json)', tornado.web.StaticFileHandler, {'path': ''}),
    (r'/ws', WSHandler),
], **settings)

# Corre el servidor
if __name__ == '__main__':
    print 'running'
    app.listen(options.port)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()
