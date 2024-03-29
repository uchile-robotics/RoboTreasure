import tornado.ioloop
import tornado.web
import tornado.websocket

import socket
import os.path


from std_msgs.msg import String
import rospy

from tornado.options import define, options, parse_command_line

define("port", default=8888, type=int)
# Carpetas para archivos statics e html's
settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
)

team_name_def = ""
stage = ""

################################################

                    #STAGE1#

################################################

class B1Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "blue"
        print team_name_def
        self.redirect("/")

class G1Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "green"
        print team_name_def
        self.redirect("/")

class R1Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "red"
        print team_name_def
        self.redirect("/")

class Y1Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "yellow"
        print team_name_def
        self.redirect("/")

class P1Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "purple"
        print team_name_def
        self.redirect("/")


################################################

                    #STAGE2#

################################################

class B2Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "blue"
        print team_name_def
        self.redirect("/stage2")

class G2Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "green"
        print team_name_def
        self.redirect("/stage2")

class R2Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "red"
        print team_name_def
        self.redirect("/stage2")

class Y2Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "yellow"
        print team_name_def
        self.redirect("/stage2")

class P2Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "purple"
        print team_name_def
        self.redirect("/stage2")

################################################

                    #STAGE3#

################################################

class B3Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "blue"
        print team_name_def
        self.redirect("/stage3")

class G3Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "green"
        print team_name_def
        self.redirect("/stage3")

class R3Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "red"
        print team_name_def
        self.redirect("/stage3")

class Y3Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "yellow"
        print team_name_def
        self.redirect("/stage3")

class P3Handler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = ("CONNECT", "GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, HEAD')

    def head(self):
        print "head"
        self.get()
        print "head finish"

    def get(self):
        print "loading html"
        global team_name_def
        team_name_def = "purple"
        print team_name_def
        self.redirect("/stage3")

################################################

                    #HANDLERS#

################################################


# Clase que renderiza el index 
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
        print "################################################"
        print team_name_def
        print "################################################"
        if team_name_def == "yellow":
            self.render("index.html", team_name="Equipo Amarillo")
        elif team_name_def == "red":
            self.render("index.html", team_name="Equipo Rojo")
        elif team_name_def == "blue":
            self.render("index.html", team_name="Equipo Azul")
        elif team_name_def == "purple":
            self.render("index.html", team_name="Equipo Morado")
        elif team_name_def == "green":
            self.render("index.html", team_name="Equipo Verde")


# Clase que renderiza el index Stage2
class Stage2Handler(tornado.web.RequestHandler):
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
        print "################################################"
        print team_name_def
        print "################################################"
        if team_name_def == "yellow":
            self.render("index_s2.html", team_name="Equipo Amarillo")
        elif team_name_def == "red":
            self.render("index_s2.html", team_name="Equipo Rojo")
        elif team_name_def == "blue":
            self.render("index_s2.html", team_name="Equipo Azul")
        elif team_name_def == "purple":
            self.render("index_s2.html", team_name="Equipo Morado")
        elif team_name_def == "green":
            self.render("index_s2.html", team_name="Equipo Verde")


# Clase que renderiza el index Stage3
class Stage3Handler(tornado.web.RequestHandler):
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
        print "loading html Stage 3"
        print "################################################"
        print team_name_def
        print "################################################"
        if team_name_def == "yellow":
            self.render("index_s3_t4.html", team_name="Equipo Amarillo")
        elif team_name_def == "red":
            self.render("index_s3_t2.html", team_name="Equipo Rojo")
        elif team_name_def == "blue":
            self.render("index_s3_t1.html", team_name="Equipo Azul")
        elif team_name_def == "purple":
            self.render("index_s3_t5.html", team_name="Equipo Morado")
        elif team_name_def == "green":
            self.render("index_s3_t3.html", team_name="Equipo Verde")

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

class WrongHandler(tornado.web.RequestHandler):
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
        self.get()
        print "head finish"

    def get(self):
        print "loading wrong html"
        self.render("wrong.html")

class TutorialHandler(tornado.web.RequestHandler):
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
        self.get()
        print "head finish"

    def get(self):
        print "loading tutorial html"
        self.render("tutorial.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
      
    def on_message(self, message):
        message = message.encode('ascii', 'ignore').decode('ascii')
        print 'message received:  %s' % message
        if message == "ready":
            print "Publishing to AWR"
            ready_pub = rospy.Publisher('/answer_web_ready', String, queue_size=10)
            ready_pub.publish("ready")
        else:
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

# Url's
app = tornado.web.Application([
    (r'/', MainHandler),
    (r'/', MainHandler),
    (r'/stage3', Stage3Handler),
    (r'/stage2', Stage2Handler),


    (r'/stage3/1', B3Handler),
    (r'/stage3/2', R3Handler),
    (r'/stage3/3', G3Handler),
    (r'/stage3/4', Y3Handler),
    (r'/stage3/5', P3Handler),

    (r'/stage2/1', B2Handler),
    (r'/stage2/2', R2Handler),
    (r'/stage2/3', G2Handler),
    (r'/stage2/4', Y2Handler),
    (r'/stage2/5', P2Handler),

    (r'/stage1/1', B1Handler),
    (r'/stage1/2', R1Handler),
    (r'/stage1/3', G1Handler),
    (r'/stage1/4', Y1Handler),
    (r'/stage1/5', P1Handler),

    (r'/b', WhiteHandler),
    (r'/wrong', WrongHandler),
    (r'/tutorial', TutorialHandler),
    (r'/(launch_details\.json)', tornado.web.StaticFileHandler, {'path': ''}),
    (r'/ws', WSHandler),
], **settings)

# Corre el servidor
if __name__ == '__main__':
    print 'running'
    app.listen(options.port)
    # myIP = socket.gethostbyname(socket.gethostname())
    myIP = "192.168.1.126"
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()
