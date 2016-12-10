# 打开我的文件

from An import an
from subl import tree_command

class Menu(tree_command.Tree):
	__slots__ = ('name', 'path')

	@classmethod
	def parse_node(cls, parent, data, child):
		for key in cls.__slots__:
			setattr(child, key, data[key])
		if parent.path:
			child.path = parent.path + child.path

	def to_array(self):
		menu = [[(child.name + ' >>') if child.children else child.name, child.path] for child in self.children]
		if self.parent:
			menu.insert(0, ["..", self.name])
		return menu

	def __str__(self):
		return self.path or 'root'


class MyFileCommand(tree_command.TreeCommandBase):
	NODE = Menu

	def done(self, node):
		an.open(node.path, self.window)