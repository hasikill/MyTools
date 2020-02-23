#coding:utf-8

import sys
import testqt
import httpget
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import dlgexplorer

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = testqt.Ui_Form()
		self.ui.setupUi(self)
		self.mapBtns = {}

		#初始化ui
		self.initUi()

	def showTools(self, obj_tools):
		colums1_titles = obj_tools['colums1_titles']
		colums1_urls = obj_tools['colums1_urls']
		authors = obj_tools['authors']
		descriptors = obj_tools['descriptors']

		self.ui.tableWidget.setRowCount(len(colums1_titles))
		for i in range(len(colums1_titles)):
			#程序名
			item = QtWidgets.QTableWidgetItem(colums1_titles[i])
			item.setData(QtCore.Qt.UserRole, colums1_urls[i])
			self.ui.tableWidget.setItem(i, 0, item)

			#作者
			#self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(authors[i]))

			#描述
			if (i < len(descriptors)):
				self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(descriptors[i]))

		self.ui.tableWidget.resizeRowsToContents()

	def eventFilter(self, target, event):
		if (event.type() == QtCore.QEvent.MouseButtonPress):
			u = self.mapBtns[target]
			print("MouseButtonPress", u)
			obj_tools = httpget.GetTools(u)
			print(obj_tools)
			self.showTools(obj_tools)
		return QtWidgets.QWidget.eventFilter(self, target, event)

	def showToolPath(self, path):
		dlg = dlgexplorer.Ui_DlgExplorer()
		dlg.setupUi(dlg)
		dlg.setPath(path)
		dlg.exec()

	def openTool(self):
		row = self.ui.tableWidget.currentRow()
		item = self.ui.tableWidget.item(row, 0)
		file_url = item.data(QtCore.Qt.UserRole)
		print("Open")

		# 获取文件名称
		file_name = file_url[file_url.rfind('/')+1:]
		path_name = file_name[:file_name.rfind(".")]

		#判断app目录
		if (os.path.exists("./app/" + path_name) == False):
			if (os.path.exists("./download/" + file_name) == False):
				# 下载和解压
				if (self.downloadTool() == False):
					return

			#解压
			self.ui.lb_speed.setText("正在解压")
			cmd = "7z x \"./download/%s\" -o\"app/%s\" -aoa" % (file_name, path_name)
			print(cmd)
			os.system(cmd)
			self.ui.lb_speed.setText("解压完成")

		# 已经解压，显示目录
		self.showToolPath("app/" + path_name)

	def downloadTool(self):
		row = self.ui.tableWidget.currentRow()
		item = self.ui.tableWidget.item(row, 0)
		file_url = item.data(QtCore.Qt.UserRole)
		print("Download: %s" % file_url)

		#获取文件名
		file_name = file_url[file_url.rfind('/')+1:]
		if (file_name[len(file_name)-3:] == "htm"):
			print("不支持的下载格式")
			os.system("start " + file_url)
			# print("start " + file_url)
			return False

		if (os.path.exists("./download/") == False):
			os.mkdir("./download/")

		#下载
		res = httpget.downloadFile("./download/" + file_name, file_url, self.showProgress)
		if (res['status'] == False):
			QtWidgets.QMessageBox.warning(self, "err", res['msg'])
			return False
		self.showProgress(100.0, 0)
		return True

	def showProgress(self, progress, speed):
		print(progress, speed)
		self.ui.progressBar.setValue(int(progress))
		if (progress != 100.0):
			self.ui.lb_speed.setText("%.2fM/S" % speed)
		else:
			self.ui.lb_speed.setText("下载完成")

	def OnCellDoubleClicked(self, row, colum):
		self.openTool()

	def initUi(self):
		#设置样式
		self.ui.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
		self.ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.ui.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
		self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

		#连接槽
		self.ui.tableWidget.cellDoubleClicked.connect(self.OnCellDoubleClicked)

		#添加菜单
		act_open = QtWidgets.QAction("打开", self)
		act_download = QtWidgets.QAction("下载", self)
		act_open.triggered.connect(self.openTool)
		act_download.triggered.connect(self.downloadTool)
		self.ui.tableWidget.addAction(act_open)
		self.ui.tableWidget.addAction(act_download)

		#获取数据
		obj_page = httpget.GetMainMenu()

		titles = obj_page['titles']
		contents = obj_page['contents']

		for i in range(len(titles)):
			groupBox = QtWidgets.QGroupBox()
			vboxLayout = QtWidgets.QVBoxLayout(groupBox)

			content = contents[i]
			for j in range(len(content['titles'])):
			    btn = QtWidgets.QPushButton(content['titles'][j])
			    btn.installEventFilter(self)
			    self.mapBtns[btn] = content['urls'][j]
			    vboxLayout.addWidget(btn)
			self.ui.toolBox.addItem(groupBox, titles[i])

		#显示第一个
		self.ui.toolBox.setCurrentIndex(1)


if __name__ == "__main__":
	QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = MainWindow()
	MainWindow.show()
	sys.exit(app.exec_())