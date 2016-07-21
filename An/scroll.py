import sublime_plugin

# 光标不移动的滚动
# di: 1  下一行
# di: -1 上一行
# di: 2  下一屏
# di: -2 上一屏
# di: -4  开头
# di: 4  结尾
class ViewportScroolCommand(sublime_plugin.TextCommand):
	def run(self, edit, di):
		curTop = self.view.viewport_position()[1]
		# 行高(layout单位)
		lineHeight = self.view.line_height()
		maxTop = self.view.layout_extent()[1] - lineHeight
		mul = 1 if di > 0 else -1
		num = 0
		if di & 1:
			# 行滚动
			# 行高(layout单位)
			num = mul * lineHeight
		elif di & 2:
			# 屏滚动
			# 可视区高(layout单位)
			num = mul * self.view.viewport_extent()[1]
		else:
			# 开头或结尾
			if di < 0:
				curTop = 0
			else:
				curTop = maxTop
		curTop += num
		if curTop < 0:
			curTop = 0
		elif curTop > maxTop:
			curTop = maxTop
		self.view.set_viewport_position((0, curTop))
