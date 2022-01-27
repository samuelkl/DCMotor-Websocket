#! /usr/bin/python

import os.path
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import pigpio.h

#Initialize Raspberry PI GPIO

#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(11, GPIO.OUT)
#GPIO.setup(13, GPIO.OUT)
#GPIO.setup(16, GPIO.OUT)
#GPIO.setup(18, GPIO.OUT)

enA1 = 12
enB1 = 13
enA2 = 1
enB2 = 6

gpioInitialise();
gpioSetMode(enA1, PI_OUTPUT);
gpioSetMode(enB1, PI_OUTPUT);
gpioSetMode(enA2, PI_OUTPUT);
gpioSetMode(enB2, PI_OUTPUT);

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
    speed = message[1:3]
    speedInt = int(speed)

    if motor == "l":
      print ('Left Motor Rotates at '), speed
      if speedInt > 0:
          #gpioWrite(enA1, 0)
          #gpioPWM(enA2, speedInt)
           print ("1")
      else:
          #gpioWrite(enA2,0)
          #gpioPWM(enA1, speedInt*-1)
          print ("2")

    if motor == "r":
      print ('Right Motor Rotates at '), speed
      if speedInt > 0:
          #gpioWrite(enB1, 0)
          #gpioPWM(enB2, speedInt)
          print ("1")
      else:
          #gpioWrite(enB2,0)
          #gpioPWM(enB1, speedInt*-1)
          print ("2")

    if motor == "o":
          #gpioWrite(enA1,0)
          #gpioWrite(enA2,1)
          #gpioWrite(enB1,0)
          #gpioWrite(enB2,0)
          print ("3")


  def on_close(self):
    print ('[WS] Connection was closed.')
    #gpioWrite(enA1,0)
    #gpioWrite(enA2,1)
    #gpioWrite(enB1,0)
    #gpioWrite(enB2,0)


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
        GPIO.cleanup()

#End of Program
