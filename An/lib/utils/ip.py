import socket

def get_eth_ip(ethname):
	import fcntl, struct
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15].encode('utf-8')))[20:24])


def get_linux_local_ip():
	for x in ('wlp2s0', 'enp3s0f2'):
		try:
			return get_eth_ip(x)
		except OSError:
			print('read %s failed' % x)


def get_windows_local_ip():
	import socket
	return socket.gethostbyname(socket.gethostname())


def get_ip():
	from utils import runtime
	if runtime.is_linux:
		return get_linux_local_ip()
	else:
		return get_windows_local_ip()
