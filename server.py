#!/usr/bin/env python
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from gogame import *
import signal, json

signal.signal(signal.SIGINT, signal.SIG_DFL)

class Handler(WebSocketHandler):

    clients = set()
    black = False
    white = False
    game = GoGame(9)

    def open(self):
        if not Handler.black:
            Handler.clients.add(self)
            Handler.black = True
            self.color = {"name": "black", "value": BLACK}
            self.write_message(json.dumps({"action": "turn"}))
        else:
            Handler.clients.add(self)
            Handler.white = True
            self.color = {"name": "white", "value": WHITE}

    def on_message(self, message):
        print message
        x, y = [int(z) for z in message.split("_")]
        result = Handler.game.move_stone(x, y)
        print result.prisoners

        if (result.status == VALID):
            for client in Handler.clients:
                client.write_message(json.dumps({"action": "put", "x": x, "y": y, "color": self.color["name"]}))

                for prisoner in result.prisoners:
                    client.write_message(json.dumps({"action": "remove", "x": prisoner[0], "y": prisoner[1]}))

                if client.color["value"] == Handler.game.to_play:
                    client.write_message(json.dumps({"action": "turn"}))
        else:
            self.write_message(json.dumps({"action": "nope"}))

    def on_close(self):
        Handler.clients.remove(self)
        if self.color["value"] == BLACK:
            Handler.black = False
        else:
            Handler.white = False
        print "Connection closed. Id: " + str(self)

print "Server started."

HTTPServer(Application([("/", Handler)])).listen(8888)
IOLoop.instance().start()
