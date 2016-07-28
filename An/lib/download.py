import os, threading
from urllib.request import urlopen
from An import an

class Downloader(threading.Thread):
	def __init__(self, datas, filedir = None):
		super(Downloader, self).__init__()
		self.datas = datas
		self.filedir = filedir

	def run(self):
		now = 0
		length = len(self.datas)
		for data in self.datas:
			if isinstance(data, dict):
				# datas是字典列表 [{'url': '', 'name': ''}]
				url = data['url']
				filename = data['name']
			else:
				# datas是url列表
				url = data
				filename = os.path.basename(data)
			request = urlopen(url)
			filepath = filename if not self.filedir else os.path.join(self.filedir, filename)
			file = open(filepath, 'wb')
			file.write(request.read())
			file.close()
			request.close()
			now += 1
			an.echo("{0:2d}/{1:2d} {2}".format(now, length, filepath))

def download(datas, filedir = None):
	downloader = Downloader(datas, filedir)
	downloader.start()