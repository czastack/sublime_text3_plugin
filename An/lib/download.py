import os, threading
from urllib.request import urlopen

class Downloader(threading.Thread):
	# keepdir datas为url列表且urlprefix不为空时，文件名是否保留路径
	def __init__(self, datas, urlprefix = None, filedir = None, keepdir = False):
		super(Downloader, self).__init__()
		self.datas = datas
		self.urlprefix = urlprefix
		self.filedir = filedir
		self.keepdir = keepdir

	def run(self):
		now = 0
		length = len(self.datas)
		for data in self.datas:
			if isinstance(data, dict):
				# datas是字典列表 [{'url': '', 'name': ''}]
				url = data['url']
				if self.urlprefix:
					url = self.urlprefix + url
				filename = data['name']
			else:
				# datas是url列表
				url = data
				if self.urlprefix:
					url = self.urlprefix + url
					filename = data if self.keepdir else os.path.basename(data)
				else:
					filename = os.path.basename(data)
			request = urlopen(url)
			filepath = filename if not self.filedir else os.path.join(self.filedir, filename)
			
			# 创建父目录
			file_parent_dir = os.path.dirname(filepath)
			if file_parent_dir and not os.path.isdir(file_parent_dir):
				print('创建目录:' + file_parent_dir)
				os.makedirs(file_parent_dir)

			file = open(filepath, 'wb')
			file.write(request.read())
			file.close()
			request.close()
			now += 1
			print("{0:2d}/{1:2d} {2}".format(now, length, filepath))
		print('finish')

def download(*args, **kwargs):
	downloader = Downloader(*args, **kwargs)
	downloader.start()