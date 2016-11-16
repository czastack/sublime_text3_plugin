import sublime, sublime_plugin, os
from utils import runtime
from subl import load_settings

class Tree:
	__slots__ = ('parent', 'children', 'last_sel')

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
			cls.parse_node(parent, item, child)
			if 'children' in item:
				cls.parse(item['children'], child)
			child.parent = parent
			parent.children.append(child)
		return parent

class TreeCommandBase(sublime_plugin.WindowCommand):
	__slots__ = ('node', 'first_highlight', 'focus_map')
	"""
	to add:
	NODE: 节点类型
	done: 处理函数
	"""

	def run(self):
		# 根结点
		if not hasattr(self, 'node'):
			self.load_settings()
			self._settings.add_on_change('node_data', self.on_settings_change)
		self.show_menu()

	def load_settings(self):
		datas = load_settings(self, "all")
		platform_settings = load_settings(self, sublime.platform())
		if platform_settings:
			datas.extend(platform_settings)
		self.node = self.NODE.parse(datas)

	def on_settings_change(self):
		self.load_settings()

	def on_select(self, i):
		if i == -1:
			pass
		elif i == 0 and self.node.parent:
			self.node = self.node.parent
			self.show_menu()
		else:
			self.node.last_sel = i
			if self.node.parent:
				i -= 1
			node = self.node.children[i]
			if node.children:
				self.node = node
				self.show_menu()
			else:
				self.done(node)

	def show_menu(self):
		sel = self.node.last_sel if self.node.last_sel is not None else -1
		self.window.show_quick_panel(self.node.to_array(), 
			self.on_select, selected_index = sel)
