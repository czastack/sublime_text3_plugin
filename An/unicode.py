import sublime_plugin
from An import An
import re

class UnicodeDecodeCommand(sublime_plugin.TextCommand):
	reg = None

	def run(self, edit):
		if self.reg == None:
			self.reg = re.compile(r'(\\u[0-9a-fA-F]{4})+')
		if len(self.view.selection) == 1 and self.view.selection[0].empty():
			region = An.region(self.view)
			self.unicode_escape_region_tostr(edit, region)
		else:
			# 所选部分
			for region in self.view.selection:
				if not region.empty():
					self.unicode_escape_region_tostr(edit, region)

	def unicode_escape_region_tostr(self, edit, region):
		result = self.unicode_escape_tostr(self.view.substr(region))
		self.view.replace(edit, region, result)

	def unicode_escape_tostr(self, text):
		return self.reg.sub(lambda matcher: eval('"' + matcher.group(0) + '"'), text)