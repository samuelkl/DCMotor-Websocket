#! /usr/bin/python

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import pigpio.h

#Initialize Raspberry PI GPIO
enA1 = 12
enB1 = 13
enA2 = 7
enB2 = 6

pi = pigpio.pi() 
pi.set_mode(enA1, pigpio.OUTPUT)
pi.set_mode(enB1, pigpio.OUTPUT)
pi.set_mode(enA2, pigpio.OUTPUT)
pi.set_mode(enB2, pigpio.OUTPUT)

#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)

#Tonado server port
PORT = 80


class MainHandler(tornado.web.RequestHandler):
  def get(self):
     print ("[HTTP](MainHandler) User Connected.")
     self.render("index.html")

	
class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print ('[WS] Connection was opened.')
 
  def on_message(self, message):
    print ('[WS] Incoming message:'), message
    motor = message[0]
    speed = message[1:]
    speedInt = int(speed)

    if motor == "l":
      print ('Left Motor Rotates at '), speed
      if speedInt > 0:
          pi.write(enA1, 0)
          pi.set_PWM_dutycycle(enA2, speedInt)

      else:
          pi.write(enA2,0)
          pi.set_PWM_dutycycle(enA1, speedInt*-1)


    if motor == "r":
      print ('Right Motor Rotates at '), speed
      if speedInt > 0:
          pi.write(enB1, 0)
          pi.set_PWM_dutycycle(enB2, speedInt)

      else:
          pi.write(enB2,0)
          pi.set_PWM_dutycycle(enB1, speedInt*-1)


    if motor == "o":
          pi.write(enA1,0)
          pi.write(enA2,0)
          gpioWrite(enB1,0)
          gpioWrite(enB2,0)



  def on_close(self):
    print ('[WS] Connection was closed.')
    pi.write(enA1,0)
    pi.write(enA2,0)
    pi.write(enB1,0)
    pi.write(enB2,0)


application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ], **settings)


if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()

        print ("Tornado Server started")
        main_loop.start()

    except:
        print ("Exception triggered - Tornado Server stopped.")

#End of Program

