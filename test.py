from accessPointFinder import AccessPointFinder
import time
import gc2
import nmap_mod
from dns_spoof import DNSSpoof

#ap_finder = AccessPointFinder('wlxf4f26d16149b')
#gcat = gc2.Gcat()

def execute_cmd(cmd, args=[]):
	cmd = cmd.lower()

	if cmd == 'get_all_aps':
		print '[*] Get list of Access Points'
		#ap_finder.get_all_AP()
	elif cmd == 'start_find':
		print '[*] Start finding Access Points'
		#ap_finder.start_finding_AP()
	elif cmd == 'stop_find':
		print '[*] Stop finding Access Points'
		#ap_finder.stop_finding()
	elif cmd == 'start_fake_ap':
		print '[*] Start fake AP with SSID: {ssid} and BSSID: {bssid}'.format(ssid=args[0], bssid=args[1])
		#ap_finder.stop_finding()

	#elif cmd == 'evil_twin_ap':

	#elif cmd == 'get_screenshot_ap':

	#elif cmd == 'scan_hosts':

	#elif cmd == 'get_current_macs'

	#elif cmd == 'deauth_all':

	#elif cmd == 'deauth':

	#elif cmd == 'get_commands':

def main():
	while 1:
		gcat.checkCommands()
		if len(gcat.pending_tasks) != 0:
			for task in gcat.pending_tasks:
				if task.has_key('args'): execute_cmd(task['cmd'], taks['args'])
				else: execute_cmd(task['cmd'])

		time.sleep(3)

def main2():
	dns = DNSSpoof('en1', 'domains.txt')
	dns.start()

if __name__ == '__main__':
	main2()
