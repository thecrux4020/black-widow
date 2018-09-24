import nmap

class NetworkScanner:
	def __init__(self, targets):
		self.scanner = nmap.PortScanner()
		self.targets = targets

	def detect_OS(self):
		for target in self.targets:
			self.scanner.scan(target, arguments='-O')
		
		self.targets = self.scanner['scan']
		self.scanner = nmap.PortScanner()

	def get_OS(self, host):
		list_aux = []

		for os in self.targets[host]['osmatch']:
			list_aux.append({
					'name': os['name'],
					'accuracy': os['accuracy']
				})
		return list_aux

	def get_hostnames(self, host):
		return self.targets[host]['hostnames']

	def get_uptime(self, host):
		return self.targets[host]['uptime']

	def get_status(self, host):
		return self.targets[host]['status']

	def get_open_ports(self, host):
		return self.targets[host]['tcp'].keys()

	def get_detail_for_port(self, host, port):
		return self.targets[host]['tcp'][port]
