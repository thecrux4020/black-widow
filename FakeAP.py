from interface import Interface
import subprocess

class FakeAP:

	def __init__(self, out_interface=False, in_interface, ssid, bssid, bssid_mac):
		if not out_interface: self.out_interface = Interface(out_interface, False)
		else: self.out_interface = out_interface 
		self.in_interface = Interface(in_interface, True)
		self.ssid = ssid
		self.bssid = bssid
		self.bssid_mac = bssid_mac

		############################################################
		######################## CONSTANTS #########################
		############################################################
		self.ap_ip = '10.0.0.1'
		self.ap_netmask = '255.255.255.0'


	def configure_interface(self):
		self.in_interface.change_mac_addr(mac)		
		self.in_interface.set_inet_config(self.ap_ip, self.ap_netmask)

	def enable_ip_forwarding(self):
		file = open('/proc/sys/net/ipv4/ip_forward', 'w')
		file.write('1')
		file.close()

	def enable_routing(self):
		#Clear previous ip tables config
		os.system('iptables --flush')
		os.system('iptables --table nat --flush')
		os.system('iptables --delete-chain')
		os.system('iptables --table nat --delete-chain')

		#Rule of fake_interface
		command = 'iptables --table nat --append POSTROUTING --out-interface {out_interface} -j MASQUERADE'.format(out_interface=self.out_interface.get_physical_interface_id())
		os.system(command)
		
		#Rule of output_interface
		command = 'iptables --append FORWARD --in-interface {in_interface} -j ACCEPT'.format(in_interface=self.in_interface.get_physical_interface_id())
		os.system(command)

	def start_dhcp_server(self):
		os.system('service isc-dhcp-server start')

	def get_config_from_dhcp(self):
		command = 'dhclient {interface}'.format(interface = self.interface.get_physical_interface_id())
		os.system(command)

	def start_ap(self, config_file):
		subprocess.Popen(['hostapd', '-d', config_file], stdout=PIPE, stderr=PIPE)

	