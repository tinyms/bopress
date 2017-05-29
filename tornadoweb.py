

import os
import sys

import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from BoPress.log import Logger

__author__ = 'i@tinyms.com'

# if settings.DEBUG:
#     ABS_PATH = "c:/tinyms/dev.projects/meizi"

# ABS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ABS_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ABS_PATH)


def startup(port=8080):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BoPress.settings")

    if django.VERSION[1] > 5:
        django.setup()

    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        handlers=[
            # ('/hello-tornado', HelloHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        ],
        debug=False,
        static_path=os.path.join(ABS_PATH, "static"),
        template_path=os.path.join(ABS_PATH, "templates"),
        compress_response=True,
    )
    try:
        print("Tornado Web Server %s "% tornado.version)
        print("Django %s" % django.__version__)
        print("Document Root: "+ABS_PATH)
        print("Run At: http://127.0.0.1:%i/" % port)
        server = tornado.httpserver.HTTPServer(tornado_app)
        server.listen(port)
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        Logger.exception(e)

if __name__ == '__main__':
        startup()
