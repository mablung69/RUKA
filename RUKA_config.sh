#!/bin/bash
#modificar en masterDataControl.py la url por la que corresponda al server
#agregar las ips de los nodos slave mas un nombre en el archivo slaves.data
#sudo ./RUKA_config.sh master 00 develop 192.168.0.100 192.168.0.110
#sudo ./RUKA_config.sh slave 01 develop 192.168.0.101 192.168.0.111
#sudo ./RUKA_config.sh slave 02 develop 192.168.0.102 192.168.0.112

#modificar en masterDataControl.py la url por la que corresponda al server
#agregar las ips de los nodos slave mas un nombre en el archivo slaves.data
#sudo ./RUKA_config.sh master 00 production 192.168.0.100 192.168.0.110
#sudo ./RUKA_config.sh slave 01 production 192.168.0.101 192.168.0.111
#sudo ./RUKA_config.sh slave 02 production 192.168.0.102 192.168.0.112

#$1 master, slave
#$2 00->99
#$3 develop, production
#$4 ip fija wifi (192.168.x.y)
#$5 ip fija ethernet (192.168.x.y)

if [ $1 == "master" ]; then
echo '#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo ifconfig eth0 down
sudo ifconfig eth0 hw ether 00:e0:4c:53:44:'$2'
sudo ifconfig eth0 up

cd /home/pi/RUKA/
python3.5 master.py 2>&1 /home/pi/RUKA/master.log &'>/etc/rc.local
else
echo '#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

sudo ifconfig eth0 down
sudo ifconfig eth0 hw ether 00:e0:4c:53:44:'$2'
sudo ifconfig eth0 up

cd /home/pi/RUKA/
python3.5 slave.py '$3' 2>&1 /home/pi/RUKA/slave.log &'>/etc/rc.local
fi

echo '# A sample configuration for dhcpcd.
# See dhcpcd.conf(5) for details.

# Allow users of this group to interact with dhcpcd via the control socket.
#controlgroup wheel

# Inform the DHCP server of our hostname for DDNS.
hostname

# Use the hardware address of the interface for the Client ID.
clientid
# or
# Use the same DUID + IAID as set in DHCPv6 for DHCPv4 ClientID as per RFC4361.
# Some non-RFC compliant DHCP servers do not reply with this set.
# In this case, comment out duid and enable clientid above.
#duid

# Persist interface configuration when dhcpcd exits.
persistent

# Rapid commit support.
# Safe to enable by default because it requires the equivalent option set
# on the server to actually work.
option rapid_commit

# A list of options to request from the DHCP server.
option domain_name_servers, domain_name, domain_search, host_name
option classless_static_routes
# Most distributions have NTP support.
option ntp_servers
# Respect the network MTU. This is applied to DHCP routes.
option interface_mtu

# A ServerID is required by RFC2131.
require dhcp_server_identifier

# Generate Stable Private IPv6 Addresses instead of hardware based ones
slaac private

# Example static IP configuration:
#interface eth0
#static ip_address=192.168.0.10/24
#static routers=192.168.0.1
#static domain_name_servers=192.168.0.1 8.8.8.8

# It is possible to fall back to a static IP if DHCP fails:
# define static profile
#profile static_eth0
#static ip_address=192.168.1.23/24
#static routers=192.168.1.1
#static domain_name_servers=192.168.1.1

# fallback to static profile on eth0
#interface eth0
#fallback static_eth0

# interfaces static ip RUKA
interface wlan0
static ip_address='$4'/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1 8.8.8.8

interface eth0
static ip_address='$5'/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1 8.8.8.8'>/etc/dhcpcd.conf

echo '# Use MAC based names for network interfaces which are directly or indirectly
# on USB and have an universally administered (stable) MAC address (second bit
# is 0). Do not do this when ifnames is disabled via kernel command line or
# customizing/disabling 99-default.link (or previously 80-net-setup-link.rules).

IMPORT{cmdline}="net.ifnames"
ENV{net.ifnames}=="0", GOTO="usb_net_by_mac_end"

ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb", NAME=="", \
    ATTR{address}=="?[014589cd]:*", \
    TEST!="/etc/udev/rules.d/80-net-setup-link.rules", \
    TEST!="/etc/systemd/network/99-default.link", \
    IMPORT{builtin}="net_id", NAME="eth0"

LABEL="usb_net_by_mac_end"'>/lib/udev/rules.d/73-usb-net-by-mac.rules
sudo cp /lib/udev/rules.d/73-usb-net-by-mac.rules /etc/udev/rules.d/

