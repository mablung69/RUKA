import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
from controller import Controller
from logger import Logger
import bluetooth_variables as b_v
import logger_variables as l_v

from twisted.python         import log
from twisted.internet       import reactor
from twisted.web.server     import Site
from twisted.web.resource   import Resource

from eventModule import getBroadcaster
broadcasterSingleton = getBroadcaster()

from slaveDataControl import getSlaveDataControl
slaveDataControl = getSlaveDataControl()

class Views(Resource):

  isLeaf = True

  def __init__(self):
    Resource.__init__(self)

  def render_GET(self, request):

    logging.debug("[V].render_GET")
    logData = broadcasterSingleton.event["get_log_data"].call()
    data = {"status":"ok", "logData":logData}
    data = str(data).replace("'",'"')


    request.setHeader('Access-Control-Allow-Origin', '*')
    request.setHeader('Access-Control-Allow-Methods', 'GET')
    request.setHeader('Access-Control-Allow-Headers', 'x-prototype-version,x-requested-with')
    request.setHeader('Access-Control-Max-Age', 2520) # 42 hours
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")

    logging.debug("[V].render_GET before return")

    #return "<html><body>Prueba</body></html>"
    #return u'{"status":"ok"}'.encode('utf-8')
    return data.encode('utf-8')

    #request.setHeader("Content-Type", "text/plain; charset=utf-8")
    #return u"<html><body>Prueba</body></html>".encode('utf-8')


if __name__ == '__main__':

  log.startLogging(sys.stdout)

  logging.debug(sys.argv)
  logging.debug('----- PiTooth -----\n')
  sstate = "develop"
  if len(sys.argv)>1:
    sstate = sys.argv[1] if sys.argv[1] in ["develop","production"] else "develop"
  logging.debug(sstate)
  logger = Logger(logging_delay=l_v.logging_delay,
                  file_name=l_v.file_name,
                  sensor_pin=l_v.sensor_pin,
                  state=sstate)
  controller = Controller(intensity_threshold=b_v.intensity_threshold,
                          connection_attempts=b_v.connection_attempts,
                          checker_delay=b_v.checker_delay)

  logging.debug('Slave Node RUKA')
  logging.debug("Using Twisted reactor {0}".format(reactor.__class__))
  web       = 8000
  root = Views()
  reactor.listenTCP(web, Site(root))      
  reactor.run()
