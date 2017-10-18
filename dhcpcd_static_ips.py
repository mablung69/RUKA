import sys

if __name__ == '__main__':

  ipWlan=sys.argv[1]
  ipElan=sys.argv[2]

  file_dhcp="/etc/dhcpcd.conf"
  with open(file_dhcp,'r') as f:
    lines=f.readlines()

  nLines=[]
  for line in lines:  
    if "# interfaces static ip RUKA" in line:
      break
    else:
      nLines.append(line)

  nLines.append("# interfaces static ip RUKA")
  nLines.append("interface wlan0")
  nLines.append("static ip_address={}/24".format(ipWlan))
  nLines.append("static routers=192.168.0.1")
  nLines.append("static domain_name_servers=192.168.0.1 8.8.8.8")
  nLines.append("interface eth0")
  nLines.append("static ip_address={}/24".format(ipWlan))
  nLines.append("static routers=192.168.0.1")
  nLines.append("static domain_name_servers=192.168.0.1 8.8.8.8")

  with open(file_dhcp,'w') as f:
    for line in nLines:
      f.write(line)
