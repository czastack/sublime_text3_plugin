# zip文件操作函数
# time: 2016年6月10日

from zipfile import ZipFile


def is_zipfile(z):
    return isinstance(z, ZipFile)


def as_gbk(s):
    """zip模块cp437编码解析为GBK编码"""
    return bytes(s, 'cp437').decode('GBK')


def to_cp(s):
    """转为zip模块cp437"""
    return bytes(s, 'GBK').decode('cp437')


def prepare_dir(dirstr):
    """预处理目录"""
    if isinstance(dirstr, str):
        if not dirstr.endswith('/'):
            dirstr += '/'
        return to_cp(dirstr)


def zip_gbk_namelist(z, parentdir=None):
    """
    列出zip文件列表（GBK编码）
    parentdir 父目录
    """
    if is_zipfile(z):
        parentdir = prepare_dir(parentdir)
        result = [as_gbk(data.filename) for data in z.filelist
            if not parentdir or (data.filename != parentdir and data.filename.startswith(parentdir))]
        result.sort()
        return result


def zip_gbk_dirlist(z, parentdir=None):
    """列出zip目录列表（GBK编码）"""
    if is_zipfile(z):
        parentdir = prepare_dir(parentdir)
        result = [as_gbk(data.filename) for data in z.filelist if data.filename.endswith('/') and (not parentdir or (data.filename != parentdir and data.filename.startswith(parentdir)))]
        result.sort()
        return result


def zip_read(z, index):
    """读取zip中的文件"""
    if is_zipfile(z):
        return z.read(z.filelist[index].filename)


def zip_read_content(zfpath, filename):
    with ZipFile(zfpath) as zf:
        content = zf.read(filename).decode()
    return content
