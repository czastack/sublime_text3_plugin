import re

def replace(s, rulers):
	"""字符串批量替换"""
	for patterm, rep in rulers:
		s = re.sub(patterm, rep, s)
	return s
