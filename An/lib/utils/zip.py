# zip文件操作函数
# time: 2016年6月10日

from zipfile import ZipFile

def is_zipfile(z):
	return isinstance(z, ZipFile)

# zip模块cp437编码解析为GBK编码
def as_gbk(s):
	return bytes(s, 'cp437').decode('GBK')

# 转为zip模块cp437
def to_cp(s):
	return bytes(s, 'GBK').decode('cp437')

# 预处理目录
def prepare_dir(dirstr):
	if isinstance(dirstr, str):
		if not dirstr.endswith('/'):
			dirstr += '/'
		return to_cp(dirstr)

# 列出zip文件列表（GBK编码）
# parentdir 父目录
def zip_gbk_namelist(z, parentdir = None):
	if is_zipfile(z):
		parentdir = prepare_dir(parentdir)
		result = [as_gbk(data.filename) for data in z.filelist if not parentdir or (data.filename != parentdir and data.filename.startswith(parentdir))]
		result.sort()
		return result

# 列出zip目录列表（GBK编码）
def zip_gbk_dirlist(z, parentdir = None):
	if is_zipfile(z):
		parentdir = prepare_dir(parentdir)
		result = [as_gbk(data.filename) for data in z.filelist if data.filename.endswith('/') and (not parentdir or (data.filename != parentdir and data.filename.startswith(parentdir)))]
		result.sort()
		return result

# 读取zip中的文件
def zip_read(z, index):
	if is_zipfile(z):
		return z.read(z.filelist[index].filename)