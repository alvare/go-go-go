#!/usr/bin/env python
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from gogame import GoGame
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL) 

gg = GoGame()

class Handler(WebSocketHandler):
   def open(self):
       print "New connection opened."

   def on_message(self, message):
           print message

   def on_close(self):
           print "Connection closed."

print "Server started."
HTTPServer(Application([("/", Handler)])).listen(8888)
IOLoop.instance().start()
