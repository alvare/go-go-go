#!/usr/bin/env python
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from gogame import GoGame
import signal, json

signal.signal(signal.SIGINT, signal.SIG_DFL)

class Game(GoGame):
    def __init__(self, size, handicap):
        super(Game, size, handicap)
        self.black = False
        self.white = False

class Handler(WebSocketHandler):
    def open(self):
        global game
        print "New connection opened."
        if game.black:
            self.color = "white"
        else
            self.color = "black"
        self.write_message(json.dumps({"color": self.color}))

    def on_message(self, message):
        global gg
        print message
        self.write_message("black" if gg.to_play== 1 else "white")

    def on_close(self):
        print "Connection closed."

print "Server started."
game = Game(9, 0)

HTTPServer(Application([("/", Handler)])).listen(8888)
IOLoop.instance().start()
