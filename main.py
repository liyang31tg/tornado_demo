from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
import os
from tornado.web import authenticated
from tornado.web import HTTPError

class BaseApplication(Application):
    def log_request(self, handler):
        print(handler.request)

class BaseRequestHandler(RequestHandler):
    def initialize(self,base):
        print("base",base)
        self.base = base


    def get_current_user(self):
        name = self.get_secure_cookie("name")
        print("get_current_user:",name)
        return name == b'liyang'

    def write_error(self, status_code, **kwargs):
        dic={"code":"1",}
        self.write("这里会抛出通用的错误")



class MainHandler(BaseRequestHandler):

    def initialize(self,db,base):
        super().initialize(base)
        print(base)
        print(db)
        self.db = db

    @authenticated
    def get(self, *args, **kwargs):
        self.get_argument("asdfasdf")
        if self.get_secure_cookie("name"):
            name = self.get_secure_cookie("name")
            self.write(name)
        else:
            self.write("hello python")


class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        param = {"name":"liyang"}
        self.set_secure_cookie("name", "liyang")
        self.render("login.html",**param)

static_URL = os.path.join(os.path.dirname(__file__),"staticDir")
template_URI = os.path.join(os.path.dirname(__file__),"template")


applicationSetting = {"autoreload":True,"debug":True,"compress_response":True,"cookie_secret":"asdfkljladkjsflaksd","login_url":"/login","static_path":static_URL,
                      "template_path":template_URI,"static_url_prefix":"/s/"}


def make_app():
    initParam = {"db":"mydb","base":"bbbb"}
    return BaseApplication([(r'/', MainHandler , initParam),(r'/login',LoginHandler)],**applicationSetting)


if __name__ == '__main__':
    app = make_app()
    app.listen(8800)
    IOLoop.current().start()
    print("ccc")
