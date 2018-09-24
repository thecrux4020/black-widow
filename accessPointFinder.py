from scapy.all import *
import threading
from interface import Interface
import time

class AccessPointFinder:

	def __init__(self, interface):
		print interface
		self.interface = Interface(interface, True)
		self._should_continue = True
		self.aps_desc = list()
		self.aps = list()

	def _sniff_packet(self):
		self.interface.enable_sniff()
		sniff(prn=self._process_packet, iface=self.interface.get_monitor_interface_id(), stop_filter = lambda x: not self._should_continue)

	def _should_stop_sniff(self, packet):
		return self._should_continue

	def _process_packet(self, packet):
		if packet.haslayer(Dot11):
			#Detect beacon frame
			if packet.type == 0 and packet.subtype == 8:
				print 'packet'
				print "SSID--> {ssid}  -- BSSID --> {bssid}  -- CHANNEL --> {channel}".format(ssid=packet.info, bssid=packet.addr2, channel=ord(packet[Dot11Elt:3].info))
				if not packet.addr2 in self.aps:
					self.aps.append(packet.addr2)
					self.aps_desc.append({
							'essid': packet.info,
							'bssid': packet.addr2,
							'channel': ord(packet[Dot11Elt:3].info)
						})
				print packet.summary()
				print ''
				print packet[Dot11]

			#Detect probe request frame
#			if packet.type == 0 and packet.subtype == 4:


		#if packet.haslayer(Dot11ProbeReq):
		#	self.send_probe_resp()
		#if packet.haslayer(Dot11Auth):
		#	self.send_auth_resp()
		#if packet.haslayer(Dot11AssoReq):
		#	self.send_assoc_resp()

	def channel_hopping(self):
		while self._should_continue:
			for i in range(1,12):
				self.interface.channel_hopping(i)
			time.sleep(1)

	#Start 2 threads, one for sniff with scapy, and one for channel hopping
	def start_finding_AP(self):
		self.sniff_thread = threading.Thread(target=self._sniff_packet)
		self.sniff_thread.daemon = True
		self.sniff_thread.start()

		self.channel_hop_thread = threading.Thread(target=self.channel_hopping)
		self.channel_hop_thread.daemon = True
		self.channel_hop_thread.start()

	def get_all_AP(self):
		return self.aps

	def stop_finding(self):
		self._should_continue = False
		self.channel_hop_thread.join()
		self.sniff_thread.join()
		self.interface.disable_sniff()

#	def deauth_all_clients(self):
