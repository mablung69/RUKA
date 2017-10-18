import logging
import threading

from eventModule import getBroadcaster
broadcasterSingleton = getBroadcaster()

LOCK = threading.Lock()

slaveDataControl =  None

def getSlaveDataControl():
  global slaveDataControl
  if slaveDataControl is None:
    slaveDataControl = slaveDataControlModule()
  return slaveDataControl

class  slaveDataControlModule:

  def __init__(self):

    logging.debug("[MDCM] slaveDataControlModule construct")
    self.logData = []
    
    broadcasterSingleton.event["log_data"] += self.onLogData
    broadcasterSingleton.event["get_log_data"] += self.onGetLogData

  def onLogData(self,line):

    logging.debug("[MDCM].onLogData")
    LOCK.acquire()
    self.logData.append(line)
    LOCK.release()    

  def onGetLogData(self):

    logging.debug("[MDCM].onGetLogData")
    LOCK.acquire()
    data = list(self.logData)
    self.logData[:] = []
    LOCK.release()

    return data