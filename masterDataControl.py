import logging
from time import sleep
from threading import Thread
import os
import json
import requests
import subprocess
import traceback

masterDataControl =  None

def getMasterDataControl():
  global masterDataControl
  if masterDataControl is None:
    masterDataControl = masterDataControlModule()
  return masterDataControl

class  masterDataControlModule:

  def __init__(self):

    logging.debug("[MDCM] masterDataControlModule construct")
    self.slavesFile = "slaves.data"
    self.slaves = {}
    self.getDelay = 30#60
    self.server = "http://192.168.0.7:8000/data"
    self.loadSlaves()    

  def start(self):

    logging.debug("[MDCM].start")
    self.dataLoop = Thread(name='dataLoop',target=self.dataLoop)
    self.dataLoop.start()

  def loadSlaves(self):

    logging.debug("[MDCM].loadSlaves")
    if os.path.isfile(self.slavesFile):
      with open(self.slavesFile) as file:
        lines=file.readlines()
      for line in lines:
        try:
          name=line.split(" ")[0].strip()
          ip=line.split(" ")[1].strip()
          self.slaves[name]={"name":name,"ip":ip}
        except IndexError as e:
          logging.debug("Error getLogData get slave: {}".format(e))
          logging.debug("       {}".format(type(e)))
          logging.debug("       {}".format(traceback.format_exc()))
    else:
      self.slaves={}

  def dataLoop(self):

    logging.debug("[MDCM].dataLoop")
    while True:      
      self.getLogData()
      sleep(self.getDelay)

  def getLogData(self):

    logging.debug("[MDCM].getLogData")
    slavesData={}
    for slave in self.slaves:
      try:
        resp=requests.get(self.slaves[slave]["ip"]+":8000")
        logging.debug("resp: {}".format(resp.__dict__))
        if resp.status_code == 200:
          jresp=resp.json()
          status=jresp["status"]
          if status=="ok":        
            logData=jresp["logData"]
          else:
            logData=[]
        else:
          logData=[]
      except Exception as e:
        logging.debug("Error getLogData get slave: {}".format(e))
        logging.debug("       {}".format(type(e)))
        logging.debug("       {}".format(traceback.format_exc()))
        logData=[]
      slavesData[self.slaves[slave]["name"]]=logData     

    self.getInternet()

    #usando get
    '''
    payload = slavesData
    resp = requests.get(self.server, params=payload)
    '''
    #usando post
    try:
      payload = slavesData
      resp = requests.post(self.server, data = {"data":json.dumps(payload)})
      if resp.status_code == 200:
        pass
      else:
        pass
    except Exception as e:
      logging.debug("Error getLogData post data: {}".format(e))
      logging.debug("       {}".format(type(e)))
      logging.debug("       {}".format(traceback.format_exc()))
    
    self.getLan()

  def getInternet(self):

    logging.debug("[MDCM].getInternet")
    bashCommand_eth0 = "sudo ip link set eth0 down"
    process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_eth0_show = "sudo ip link show eth0"
    process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
    output = subprocess.getoutput(bashCommand_eth0_show)
    #output, error = process.communicate()

    logging.debug("[MDCM].getInternet output: {}".format(output))
    logging.debug("[MDCM].getInternet output: {}".format(str(output)))
    while not "state DOWN" in output:
      sleep(5)
      process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()

    bashCommand_wlan0 = "sudo ip link set wlan0 up"
    process = subprocess.Popen(bashCommand_wlan0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_wlan0_show = "ip link show wlan0"
    process = subprocess.Popen(bashCommand_wlan0_show.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    while not "state UP" in output:
      sleep(5)
      process = subprocess.Popen(bashCommand_wlan0.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      process = subprocess.Popen(bashCommand_wlan0_show.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()

  def getLan(self):    
    
    logging.debug("[MDCM].getLan")
    bashCommand_wlan0 = "sudo ip link set wlan0 down"
    process = subprocess.Popen(bashCommand_wlan0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_wlan0_show = "ip link show wlan0"
    process = subprocess.Popen(bashCommand_wlan0_show.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    while not "state DOWN" in output:
      sleep(5)
      process = subprocess.Popen(bashCommand_wlan0.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      process = subprocess.Popen(bashCommand_wlan0_show.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()   

    bashCommand_eth0 = "sudo ip link set eth0 up"
    process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_eth0_show = "ip link show eth0"
    process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    while not "state UP" in output:
      sleep(5)
      process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
