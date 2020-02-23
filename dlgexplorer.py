# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlg_explorer.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import os
import threading
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgExplorer(QtWidgets.QDialog):
    def setupUi(self, DlgExplorer):
        DlgExplorer.setObjectName("DlgExplorer")
        DlgExplorer.resize(810, 476)
        self.horizontalLayout = QtWidgets.QHBoxLayout(DlgExplorer)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(DlgExplorer)
        self.tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.retranslateUi(DlgExplorer)
        QtCore.QMetaObject.connectSlotsByName(DlgExplorer)

        self.initUi()

    def retranslateUi(self, DlgExplorer):
        _translate = QtCore.QCoreApplication.translate
        DlgExplorer.setWindowTitle(_translate("DlgExplorer", "Dialog"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("DlgExplorer", "文件名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("DlgExplorer", "文件大小"))

    def runCmd(self, cmd):
        os.system(cmd)

    def open(self):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        file_path = item.data(QtCore.Qt.UserRole)

        file_info = QtCore.QFileInfo(file_path)
        if (file_info.isDir()):
            self.setPath(file_path)
        else:
            threading._start_new_thread(self.runCmd, (), { 'cmd' : "\"%s\"" % file_path })
            # threading.Thread(target=self.runCmd, args=("cmd")).start()
        return

    def explorer(self):
        row = self.tableWidget.currentRow()
        item = self.tableWidget.item(row, 0)
        file_path = item.data(QtCore.Qt.UserRole)
        cmd = "explorer /select," + file_path.replace("/", "\\")
        os.system(cmd)
        print(cmd)
        return

    def OnCellDoubleClicked(self, row, colum):
        self.open()

    def initUi(self):
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setHidden(True)
        self.tableWidget.setColumnWidth(0, 650)

        #连接槽
        self.tableWidget.cellDoubleClicked.connect(self.OnCellDoubleClicked)

        #添加右键菜单
        act_open = QtWidgets.QAction("打开", self)
        act_explorer = QtWidgets.QAction("打开到资源管理器", self)
        act_open.triggered.connect(self.open)
        act_explorer.triggered.connect(self.explorer)
        self.tableWidget.addAction(act_open)
        self.tableWidget.addAction(act_explorer)

    def setPath(self, path):
        self.path = path

        dir_tools = QtCore.QDir(path)
        self.setWindowTitle(dir_tools.absolutePath())
        # print(dir_tools.path())
        
        #设置行数
        self.tableWidget.setRowCount(0)

        line_number = 0
        files = []
        #遍历目录
        for i in range(dir_tools.count()):
            if (dir_tools[i] == "."):
                continue

            #获取文件信息
            file_info = QtCore.QFileInfo(path + "/" + dir_tools[i])
            icon_provider = QtWidgets.QFileIconProvider()
            icon = icon_provider.icon(file_info)
            file_size = file_info.size() / 1024

            if (file_info.isDir()):
                self.tableWidget.insertRow(line_number)
                item = QtWidgets.QTableWidgetItem(dir_tools[i])
                item.setIcon(icon)
                item.setData(QtCore.Qt.UserRole, dir_tools.absolutePath() + "\\" + dir_tools[i])
                self.tableWidget.setItem(line_number, 0, item)
                line_number += 1
            else:
                obj_file = {}
                obj_file['name'] = dir_tools[i]
                obj_file['path'] = dir_tools.absolutePath() + "/" + dir_tools[i]
                obj_file['icon'] = icon
                obj_file['file_size'] = file_size
                files.append(obj_file)

        for o in files:
            self.tableWidget.insertRow(line_number)
            item = QtWidgets.QTableWidgetItem(o['name'])
            item.setIcon(o['icon'])
            item.setData(QtCore.Qt.UserRole, o['path'])
            self.tableWidget.setItem(line_number, 0, item)

            item = QtWidgets.QTableWidgetItem("%.2f KB" % o['file_size'])
            self.tableWidget.setItem(line_number, 1, item)

            line_number += 1