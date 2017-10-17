
broadcasterSingleton = None

def getBroadcaster():
  global broadcasterSingleton
  if broadcasterSingleton is None:
    broadcasterSingleton = Broadcaster()
  return broadcasterSingleton

class Broadcaster():
  def __init__(self):
    self.event = {}

    ''' Define events'''
    
    self.event["log_data"]                     = Event()
    self.event["get_log_data"]                 = ResponseEvent()
    #self.event["end"]                     = Event()
    #self.event["change_water_time"]           = ResponseEvent()
    
    
class Event(object):
  def __init__(self):
    self.__handlers = []

  def __iadd__(self, handler):
    ''' Register observer/subscriber '''
    if not handler in self.__handlers: 
        self.__handlers.append(handler)
    return self

  def __isub__(self, handler):
    ''' Unregister observer/subscriber '''
    if handler in self.__handlers:
        self.__handlers.remove(handler)
    return self

  def call(self, *args, **keywargs):
    for handler in self.__handlers:
      handler(*args, **keywargs)

  def clearObjectHandlers(self, inObject):
    ''' Remove all observers '''
    for theHandler in self.__handlers:
      if theHandler.im_self == inObject:
        self -= theHandler

class ResponseEvent(object):

  def __init__(self):
    self.__handlers = None

  def __iadd__(self, handler):
    self.__handlers = handler
    return self

  def __isub__(self, handler):
    self.__handlers = None
    return self

  def call(self, *args, **keywargs):
    return self.__handlers(*args, **keywargs)