from controller import Controller
from logger import Logger
import bluetooth_variables as b_v
import logger_variables as l_v

from twisted.internet       import reactor
from twisted.web.server     import Site
from twisted.web.resource   import Resource

from eventModule import getBroadcaster
broadcasterSingleton = getBroadcaster()

class Views(Resource):

  isLeaf = True

  def __init__(self):
    Resource.__init__(self)

  def render_GET(self, request):

    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'POST')
    request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', 2520) # 42 hours
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")

    logData = broadcasterSingleton.event["get_log_data"].call()
    data = {"status":"ok", "logData":logData}
    data = str(data).replace("'",'"')

    return data

if __name__ == '__main__':
  print('----- PiTooth -----\n')
  state="develop"
  logger = Logger(logging_delay=l_v.logging_delay,
                  file_name=l_v.file_name,
                  sensor_pin=l_v.sensor_pin,
                  state=state)
  controller = Controller(intensity_threshold=b_v.intensity_threshold,
                          connection_attempts=b_v.connection_attempts,
                          checker_delay=b_v.checker_delay)

  print "Using Twisted reactor {0}".format(reactor.__class__)
  web       = 8000
  root = Views()
  reactor.listenTCP(web, Site(root))      
  reactor.run()