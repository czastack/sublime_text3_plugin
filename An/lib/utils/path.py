import os

# 在指定路径运行
# run_at(function, 'E:/')()
def run_at(fn, new_dir):
	def wrapper(*args, **kwargs):
		# 暂存当前目录
		if new_dir:
			oldir = os.getcwd()
			os.chdir(new_dir)
		# 运行目标
		ret = fn(*args, **kwargs)
		# 切回当前目录
		if new_dir:
			os.chdir(oldir)
		return ret
	return wrapper