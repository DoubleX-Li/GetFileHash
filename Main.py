# -*- coding: utf-8 -*-

import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget, QGridLayout, QFileDialog, \
    QLabel, QLineEdit
import hashlib
from tkinter import Tk


class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(QLineEdit, self).__init__(parent)
        # 初始化打开接受拖拽使能
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        # 获取拖放过来的文件的路径
        st = str(event.mimeData().urls())
        # 处理QUrl
        st = st.replace("[PyQt5.QtCore.QUrl('file:///", "")
        st = st.replace("')]", "")
        self.setText(st)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 标签
        name = QLabel("文件名:")
        md5 = QLabel("MD5:")
        sha1 = QLabel("SHA1:")
        sha256 = QLabel("SHA256:")

        # 文件信息
        self.filenameText = MyLineEdit()
        self.filenameText.setText("将文件拖入此框或者点击下方浏览")
        self.filenameText.textChanged.connect(self.changeFileName)
        self.md5Text = QLineEdit()
        self.sha1Text = QLineEdit()
        self.sha256Text = QLineEdit()

        # 功能按钮
        compareWithClipboard = QPushButton("剪贴板比较")
        compareWithClipboard.clicked.connect(self.compare)
        browse = QPushButton("浏览")
        browse.clicked.connect(self.browse)

        # 网格布局
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(name, 1, 0)
        grid.addWidget(self.filenameText, 1, 1, 1, 5)
        grid.addWidget(md5, 2, 0)
        grid.addWidget(self.md5Text, 2, 1, 1, 5)
        grid.addWidget(sha1, 3, 0)
        grid.addWidget(self.sha1Text, 3, 1, 1, 5)
        grid.addWidget(sha256, 4, 0)
        grid.addWidget(self.sha256Text, 4, 1, 1, 5)

        grid.addWidget(compareWithClipboard, 5, 0)
        grid.addWidget(browse, 5, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 300)
        self.center()
        self.setWindowTitle('文件Hash校验')
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '警告', "是否要退出?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def changeFileName(self):
        self.filename = self.filenameText.text()
        self.calculate()

    def browse(self):
        filename = QFileDialog.getOpenFileName(self, "选择文件", "C:/")[0]
        self.filename = filename
        self.calculate()

    def addHashType(self):

        sender = self.sender()
        text = sender.text()
        if text == "MD5":
            self.hashtype[0] = sender.isChecked()
        elif text == "SHA1":
            self.hashtype[1] = sender.isChecked()
        elif text == "SHA256":
            self.hashtype[2] = sender.isChecked()

    def md5_sum(self):  # 校验值方法
        fd = open(self.filename, "rb")  # 打开文件
        fd.seek(0)  # 将文件打操作标记移到offset的位置
        line = fd.readline()  # 读取文件第一行进入line

        # md5校验值计算
        md5 = hashlib.md5()
        md5.update(line)
        # SHA1校验值计算
        sha1 = hashlib.sha1()
        sha1.update(line)
        # SHA256校验值计算
        sha256 = hashlib.sha256()
        sha256.update(line)

        while line:  # 循环读取文件
            line = fd.readline()
            md5.update(line)
            sha1.update(line)
            sha256.update(line)

        fmd5 = md5.hexdigest()  # 生成文件MD5校验值
        fsha1 = sha1.hexdigest()  # 生成文件SHA1校验值
        fsha256 = sha256.hexdigest()  # 生成文件SHA256校验值
        fsum = {"MD5": fmd5.upper(), "SHA1": fsha1.upper(), "SHA256": fsha256.upper()}

        fd.close()
        return fsum

    def calculate(self):
        if os.path.isfile(self.filename):
            self.fmd5 = self.md5_sum()
            self.filenameText.setText(self.filename)
            self.md5Text.setText(self.fmd5["MD5"])
            self.sha1Text.setText(self.fmd5["SHA1"])
            self.sha256Text.setText(self.fmd5["SHA256"])
        else:
            QMessageBox.question(self, "警告", "不是文件！", QMessageBox.Yes, QMessageBox.Yes)

    def compare(self):
        text = Tk().clipboard_get()
        reply = ""
        for key in self.fmd5:
            if self.fmd5[key] == text:
                reply = "最后一次校验的文件" + key + "与剪贴板中的数据完全相同"

        if "" == reply:
            QMessageBox.question(self, "结果", "剪贴板中的数据与最后一次校验的文件的MD5、SHA1、SHA256都不相同", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.question(self, "结果", reply, QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())