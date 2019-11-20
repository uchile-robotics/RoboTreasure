import tornado.ioloop
import tornado.web
import tornado.websocket

import socket
import os.path

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
        self.render("index.html")
        print "head finish"

    def get(self):
        print "loading html"
        self.render("index.html")

class HMainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("horizontal/horizontal_base.html")

class VMainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("vertical/vertical_base.html")

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("normal/link1.html")

class HTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("horizontal/link1_horizontal.html")

class VTestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("vertical/link1_vertical.html")

class SPRHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("normal/SPR.html")

class HSPRHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("horizontal/SPR_horizontal.html")

class VSPRHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("vertical/SPR_vertical.html")

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
    (r'/vertical', VMainHandler),
    (r'/horizontal', HMainHandler),
    (r'/link1.html', TestHandler),
    (r'/link1_vertical.html', VTestHandler),
    (r'/link1_horizontal.html', HTestHandler),
    (r'/SPR.html', SPRHandler),
    (r'/SPR_vertical.html', VSPRHandler),
    (r'/SPR_horizontal.html', HSPRHandler),
    (r'/(com.*)', CommandHandler ),
    (r'/(launch_details\.json)', tornado.web.StaticFileHandler, {'path': ''}),
], **settings)

# Corre el servidor
if __name__ == '__main__':
    print 'running'
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
