import pyric
import pyric.pyw as pyw
import os

class Interface:

	def __init__(self, interface_id, monitor_mode):
		self.interface = pyw.getcard(interface_id)
		self.monitor_mode = monitor_mode

	def _enable_phisical_interface(self):	
		pyw.devadd(self._interface_mon, self.interface.dev, 'managed')

	def _disable_phisical_interface(self):
		for card,_ in pyw.ifaces(self.interface):   
			if not card.dev == self._interface_mon.dev:
				pyw.devdel(card)

	def _disable_monitor_mode(self, interface):
		pyw.devdel(interface)

	def _enable_interface(self, interface):
		if not self.is_enable(interface): pyw.up(interface)

	def _disable_interface(self, interface):
		pyw.down(interface)

	def enable_monitor_mode(self):
		self._interface_mon = pyw.devadd(self.interface, 'mon0', 'monitor')

	def set_inet_config(self, ip, netmask):
		command = 'ifconfig {interface} up {ip} netmask {netmask}'.format(interface=self.get_physical_interface_id(), ip=ip, netmask=netmask)
		os.system(command)
		#pyw.inetset(self.interface, ip, netmask)

	def connect_to_AP(self, essid):
		command = 'iwconfig {interface} essid {essid}'.format(interface=self.interface, essid=essid)
		os.system(command)
		
	def change_mac_addr(self, new_mac):
		self._disable_interface(self.interface)
		pyw.macset(self.interface, new_mac)
		self._enable_interface(self.interface)

	def get_monitor_interface_id(self):
		return self._interface_mon.dev

	def get_physical_interface_id(self):
		return self.interface.dev

	def channel_hopping(self, channel):
		if hasattr(self, '_interface_mon'):
			pyw.chset(self._interface_mon, channel, None)
			return True
		else: return False

	def is_enable(self, interface):
		return pyw.isup(interface)

	def enable_sniff(self):
		self.enable_monitor_mode()
		self._disable_phisical_interface()
		self._enable_interface(self._interface_mon)

	def disable_sniff(self):
		self._enable_phisical_interface()
		self._disable_interface(self._interface_mon)
		self._disable_monitor_mode(self._interface_mon)
		