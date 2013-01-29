#!/usr/bin/env python
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from gogame import GoGame
import signal, json

signal.signal(signal.SIGINT, signal.SIG_DFL)

class Handler(WebSocketHandler):

    clients = set()

    def open(self):
        Handler.clients.add(self)

    def on_message(self, message):
        for client in Handler.clients:
            client.write_message('Gil '+str(client))

    def on_close(self):
        Handler.clients.remove(self)
        print "Connection closed."

print "Server started."

HTTPServer(Application([("/", Handler)])).listen(8888)
IOLoop.instance().start()
