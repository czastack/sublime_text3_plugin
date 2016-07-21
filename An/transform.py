import sublime_plugin
import re

class BaseTransverter(sublime_plugin.TextCommand):
	def run(self, edit):
		if hasattr(self, 'init'):
			self.init()
		for region in self.view.selection:
			if not region.empty():
				self.view.replace(edit, region, self.transform(self.view.substr(region)))

class CamelToLowerCommand(BaseTransverter):
	def transform(self, text):
		if '_' in text:
			# 转为驼峰
			text = re.sub(r'_[a-z]', lambda t: t.group(0)[1].upper(), text)
			# 开头大写
			text = text[0].upper() + text[1:]
		elif text.islower():
			# 开头大写
			text = text[0].upper() + text[1:]
		else:
			# 转为下划线
			text = re.sub(r'[A-Z]', lambda t: '_' + t.group(0).lower(), text)
			# 去掉开头的下划线
			if text[0] == '_':
				text = text[1:]
		return text