# 打开我的文件

import sublime, sublime_plugin, os
from utils import runtime
from exsublime import load_settings

class Tree:
	__slots__ = ('parent', 'children')

class Menu(Tree):
	__slots__ = ('name', 'path')

	def __getattr__(self, name):
		return None

	@classmethod
	def parse(cls, datas, parent = None):
		"""递归解析json数据"""
		if not parent:
			parent = cls()
		parent.children = []
		for item in datas:
			child = cls()
			child.name = item['name']
			child.path = item['path']
			if parent.path:
				child.path = parent.path + child.path
			if 'children' in item:
				cls.parse(item['children'], child)
			child.parent = parent
			parent.children.append(child)
		return parent

	def to_array(self):
		menu = [[(child.name + ' >>') if child.children else child.name, child.path] for child in self.children]
		if self.parent:
			menu.insert(0, ["..", self.name])
		return menu

class MyFileCommand(sublime_plugin.WindowCommand):
	def run(self):
		# 根结点
		datas = load_settings(self, "all")
		platform_settings = load_settings(self, sublime.platform())
		if platform_settings:
			datas.extend(platform_settings)
		self.node = Menu.parse(datas)
		self.show_menu()

	def on_select(self, i):
		if i == -1:
			pass
		elif i == 0 and self.node.parent:
			self.node = self.node.parent
			self.show_menu()
		else:
			if self.node.parent:
				i -= 1
			node = self.node.children[i]
			if node.children:
				self.node = node
				self.show_menu()
			else:
				from An import an
				an.open_file(node.path, self.window)

	def show_menu(self):
		self.window.show_quick_panel(self.node.to_array(), self.on_select)