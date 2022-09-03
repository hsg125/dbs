from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox
from db import *
import hashlib
import mainUI
from login import *
import sys


class loginForm(QtWidgets.QWidget, Ui_login):
    def __init__(self, parent=None):
        super(loginForm, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.setFocus()
        self.label_2.setVisible(False)
        # 修改按钮文字
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('登录')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText('退出')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).setText('清空')
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.login)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.quit)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)
        self.lineEdit.editingFinished.connect(self.lineEdit2.setFocus)
        self.lineEdit2.editingFinished.connect(self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFocus)

        # 设置用户名限制
        reg = QRegExp('[0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        self.lineEdit.setValidator(validator)

    def closeEvent(self, event):
        if QMessageBox.information(self, '退出程序', '确定退出吗？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No) == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def login(self):
        username = self.lineEdit.text().strip()
        if len(username) < 5:
            self.label_2.setText(r'请输入正确的用户名!')
            self.label_2.setVisible(True)
        else:
            pwd = self.lineEdit2.text().strip()
            hash_pwd = hashlib.sha1()
            hash_pwd.update(pwd.encode('UTF-8'))
            try:
                sqlite = Mysqlite('db.db')
            except Exception as e:
                self.label_2.setText(r'打开数据库错误，请联系管理员!' + str(e))
                self.label_2.setVisible(True)
                return
            sql = 'select password, grand from admin where ID = {}'.format(username)
            try:
                pwd_db = sqlite.execute_sqlite3(sql)
            except Exception as e:
                self.label_2.setText(r'访问数据库错误，请联系管理员!' + str(e))
                self.label_2.setVisible(True)
                return
            if pwd_db[0][0] != hash_pwd.hexdigest():
                self.label_2.setText(r'请输入正确的密码!')
                self.label_2.setVisible(True)
                self.reset()
            else:
                self.m = mainUI.mainUI()
                self.m.show()
                self.m.grand = pwd_db[0][1]
                myWin.hide()

    def reset(self):
        self.lineEdit.setText('')
        self.lineEdit2.setText('')
        self.label_2.setVisible(False)
        self.lineEdit.setFocus()

    def quit(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = loginForm()
    myWin.show()
    sys.exit(app.exec_())
