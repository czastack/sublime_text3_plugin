import threading

def newthread(fn):
	"""
	@newthread
	def fn(x):
		print(x)
		time.sleep(2)

	fn(1)
	print(2)
	"""
	def _deco(*args, **kwargs):
		runner = threading.Thread(target=lambda: fn(*args, **kwargs))
		runner.start()
	return _deco