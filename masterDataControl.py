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

    self.slavesFile="slaves.data"
    self.slaves={}
    self.getDelay = 60
    self.loadSlaves()    

  def start(self):

    self.dataLoop = Thread(name='dataLoop',target=self.dataLoop)
    self.dataLoop.start()

  def loadSlaves(self):

    if os.path.isfile(self.slavesFile):
      with open(self.slavesFile) as file:
        lines=file.readlines()
      for line in lines:
        try:
          name=line.split(" ")[0]
          ip=line.split(" ")[1]
          self.slaves[name]={"name":name,"ip":ip}
        except IndexError as e:
          print("Error getLogData get slave: {}".format(e))
          print("       {}".format(type(e)))
          print("       {}".format(traceback.format_exc()))
    else:
      self.slaves={}

  def dataLoop(self):

    while True:      
      self.getLogData()
      sleep(self.getDelay)

  def getLogData(self):

    slavesData={}
    for slave in self.slaves:

      try:
        resp=requests.get(self.slaves[slave]["ip"])
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
        print("Error getLogData get slave: {}".format(e))
        print("       {}".format(type(e)))
        print("       {}".format(traceback.format_exc()))
        logData=[]
      slavesData[self.slaves[slave]["name"]]=logData     

    #self.getInternet()

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
      print("Error getLogData post data: {}".format(e))
      print("       {}".format(type(e)))
      print("       {}".format(traceback.format_exc()))
    
    #self.getLan()

  def getInternet(self):

    bashCommand_eth0 = "sudo ip link set enx00e04c534458 down"
    process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_eth0_show = "ip link show enx00e04c534458"
    process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

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

    bashCommand_eth0 = "sudo ip link set enx00e04c534458 up"
    process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    bashCommand_eth0_show = "ip link show enx00e04c534458"
    process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    while not "state UP" in output:
      sleep(5)
      process = subprocess.Popen(bashCommand_eth0.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()
      process = subprocess.Popen(bashCommand_eth0_show.split(), stdout=subprocess.PIPE)
      output, error = process.communicate()