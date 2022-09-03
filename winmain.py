
import datetime
import sys

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import os

from mainForm import *
from word import *
from call_data import *

# 备份数据库
def backup():
    date = str(datetime.date.today())
    path = '.\\backup\\'
    filename = date + '.db'
    if os.path.exists(path + filename):
        return
    else:
        os.system('copy /v /y db2.db ' + path + filename)
    db = []
    ls = os.listdir(path)
    for x in ls:
        if ('.db' in x) and (x[0] == '2'):
            db.append(x)
    db.reverse()
    while len(db) > 30:
        os.remove(path + db.pop())

# 主窗口类
class MyMain(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyMain, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(832, 540)
        self.tabWidget.setCurrentIndex(0)

        # 限制lineEdit编辑框只能输入字符和数/字
        reg = QRegExp('[0-9]+$')
        validator = QRegExpValidator(self)
        validator.setRegExp(reg)
        reg_pos = QRegExp('[1-8-]+$')
        validator_pos = QRegExpValidator(self)
        validator_pos.setRegExp(reg_pos)
        self.lineEdit_01.setValidator(validator_pos)
        self.lineEdit_02.setValidator(validator_pos)
        self.lineEdit_03.setValidator(validator_pos)
        self.lineEdit_04.setValidator(validator_pos)
        self.lineEdit_21.setValidator(validator_pos)
        self.lineEdit_22.setValidator(validator_pos)
        self.lineEdit_23.setValidator(validator_pos)
        self.lineEdit_24.setValidator(validator_pos)
        self.lineEdit_12.setValidator(validator)
        self.lineEdit_11.setValidator(validator)
        try:
            backup()
        except Exception as e:
            QMessageBox.critical(self, '严重错误', '数据库备份错误，请重启或联系管理员！\n' + str(e), QMessageBox.Ok)
            sys.exit(1)

        # 槽的绑定
        self.pushButton_reset.clicked.connect(self.reset_button_click)
        self.comboBox_01.currentIndexChanged['int'].connect(self.type_select)
        self.comboBox_7.currentIndexChanged['int'].connect(self.jg_type)
        self.pushButton_save.clicked.connect(self.save_clicked)
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_exit.clicked.connect(self.close)

    # 打开查询界面
    def search(self):
        dataWin = CallData()
        dataWin.exec()
        result = dataWin.info
        print(result)
        # 设置传回数据
        if len(result) > 1:
            if result[-1] == 0:
                self.tabWidget.setCurrentIndex(0)
                self.comboBox_01.setCurrentIndex(int(result[0])-1)
                self.lineEdit_10.setText(result[2])
                self.comboBox.setEditText(result[3])
                self.lineEdit_12.setText(result[4])
                self.lineEdit_11.setText(result[1])
                self.comboBox_2.setEditText(result[-2])
                self.comboBox_3.setEditText(result[-4])
                a = eval(result[-3])
                self.lineEdit_01.setText(a[0])
                self.lineEdit_02.setText(a[1])
                self.lineEdit_03.setText(a[3])
                self.lineEdit_04.setText(a[4])

            else:
                self.tabWidget.setCurrentIndex(1)
                self.lineEdit_2.setText(result[1])
                self.comboBox_7.setEditText(result[2])
                if result[3] == '':
                    self.comboBox_9.setEnabled(0)
                else:
                    self.comboBox_9.setEditText(result[3])
                self.textEdit.setText(result[-3])
                a = eval(result[-4])
                self.lineEdit_21.setText(a[0])
                self.lineEdit_22.setText(a[1])
                self.lineEdit_23.setText(a[2])
                self.lineEdit_24.setText(a[3])


    # 关闭提示
    def closeEvent(self, event):
        if QMessageBox.information(self, '退出程序', '确定退出吗？', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No) == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 复位键的实现
    def reset_button_click(self):
        self.comboBox_01.setCurrentIndex(0)
        self.lineEdit_10.setText("")
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_12.setText("")
        self.lineEdit_11.setText("")
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_2.setText("")
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_9.setCurrentIndex(0)
        self.lineEdit_01.setText("")
        self.lineEdit_02.setText("")
        self.lineEdit_03.setText("")
        self.lineEdit_04.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.lineEdit_23.setText("")
        self.lineEdit_24.setText("")
        self.textEdit.setText("")

    # 类型选择时的判断
    def type_select(self):
        by = ['阻生牙', '牙周病', '残冠', '残根', '多生牙', '乳牙滞留', '牙列不齐']
        rct = ['急性牙髓炎', '慢性牙髓炎', '急性根尖周炎', '慢性根尖周炎', '牙隐裂']
        ss = ['残冠', '慢性牙周炎']
        xf = ['牙体缺损', '牙列缺损', '牙列缺失']
        current = self.comboBox_01.currentIndex()
        self.comboBox_2.setEnabled(1)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.clear()
        if current == 0:
            for a in by:
                self.comboBox_3.addItem(a)
        elif current == 1:
            for a in rct:
                self.comboBox_3.addItem(a)
        elif current == 2:
            for a in ss:
                self.comboBox_3.addItem(a)
        else:
            for a in xf:
                self.comboBox_3.addItem(a)
            self.comboBox_2.setCurrentIndex(3)
            self.comboBox_2.setEnabled(0)

    # 判断是否需要颜色下拉框
    def jg_type(self):
        num = [2, 4, 8, 9, 10, 11]
        current = self.comboBox_7.currentIndex()
        self.comboBox_9.setEnabled(1)
        if current in num:
            self.comboBox_9.setCurrentIndex(0)
            self.comboBox_9.setEnabled(0)

    # 检测关键数据
    def check(self, current):
        if current:
            if self.lineEdit_2.text().strip() == '' or self.comboBox_7.currentText().strip() == '':
                return 1

        else:
            if self.lineEdit_10.text().strip() == '' or self.lineEdit_11.text().strip() == '' or self.lineEdit_12.text().strip() == '' or self.comboBox_3.currentText() == '':
                return 1

        return 1

    # 获取输入信息
    def get_info(self):
        info = []
        current = self.tabWidget.currentIndex()
        info.append(str(datetime.date.today()))
        check = self.check(current)
        if check:
            QMessageBox.warning(self, '注意', '关键数据不完整，请检查后重新保存!', QMessageBox.Ok)
            return
        if current:
            # 获取加工单所需信息
            info.append(self.comboBox_6.currentText())
            info.append(self.lineEdit_2.text().strip())
            info.append(self.comboBox_7.currentText())
            info.append(self.comboBox_9.currentText())
            info.append(self.comboBox_8.currentText())
            pos = [self.lineEdit_21.text().strip(), self.lineEdit_22.text().strip(), self.lineEdit_23.text().strip(),
                   self.lineEdit_24.text().strip()]
            info.append(str(pos))
            info.append(self.textEdit.toPlainText())
            info.append(1)
        else:
            # 获取知情同意书信息
            info.append(self.comboBox_01.currentIndex())  # 类型
            info.append(self.lineEdit_10.text().strip())  # 姓名
            info.append(self.comboBox.currentIndex())  # 性别
            info.append(int(self.lineEdit_12.text()))  # 年龄
            info.append(int(self.lineEdit_11.text()))  # 病例号
            info.append(self.comboBox_2.currentText())  # 麻醉
            info.append(self.comboBox_3.currentText())  # 诊断
            pos = [self.lineEdit_01.text().strip(), self.lineEdit_02.text().strip(), self.lineEdit_04.text().strip(),
                   self.lineEdit_03.text().strip()]
            info.append(str(pos))  # 位置
            info.append(0)
        return info

    # 保存至数据库
    def saveToDB(self, info):
        # 连接数据库
        sqlite = Mysqlite('db2.db')

        # 处理加工单F
        if info[-1]:
            value = str(info[0:-1])[1:-1]
            sql = "SELECT * FROM jgd WHERE date = '{}' and patient = '{}'".format(info[0], info[2])
            exist = len(sqlite.select(sql))
            if exist:
                msg = self.cf_msg()
                if msg == -1:
                    return
                elif msg:
                    # 打印
                    pass
                else:
                    value = value + ',NULL'
                    sqlite.insert_value('jgd', value)

            filename = get_word('jgd', info)

        # 处理知情同意书
        else:
        # 查找患者是否已登记过
            data = sqlite.select_data2('patient', 'id = {}'.format(int(info[5])))
            exist = len(data)
            if not exist:
                value_patient = str(info[2:6])[1:-1]
                sqlite.insert_value('patient', value_patient)
            elif data[0][0] != info[2]:
                msg = QMessageBox.warning(self, '登记号重复', '输入的登记号已存在，但是患者姓名不一致！\n是否修改原数据？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msg == QMessageBox.No:
                    return
                else:
                    sqlite.update_data('patient', 'name', info[2], int(info[5]))

            # 检查就诊内容是否重复
            sql = "SELECT * FROM visit WHERE date = '{}' and id = {} and type = {}".format(info[0], int(info[5]),
                                                                                           int(info[1]))
            exist = len(sqlite.select(sql))
            if exist:
                msg = self.cf_msg()
                if msg == -1:
                    return
                elif msg:
                    # 打印
                    pass
                else:
                    value_visit = []
                    value_visit += info
                    del value_visit[2:5]
                    new_num = self.get_num(int(info[1]))
                    value_visit.append(new_num + 1)
                    value_visit = str(value_visit)[1:-1]
                    info.append(new_num + 1)
                    try:
                        sqlite.insert_value('visit', value_visit)
                    except Exception as e:
                        QMessageBox.critical(self, '致命错误', '写入数据库错误，请重试！')
                        return e
                    type1 = ['by', 'rct', 'ss', 'gdxf', 'hdxf']
            filename = get_word(type1[int(info[1])], info)
    def printBtn(self):


        str0 = '保存成功，即将打印。\n请放入{}后，点击OK按钮。'.format(
            (lambda x, y: x if table_name == 'jgd' else y)('加工单', '2张A4纸'))
        QMessageBox.information(self, '保存成功', str0)
        if not table_name == 'jgd':
            print_word(filename)
        print_word(filename)
        del_file(filename)
        self.pushButton_reset.click()

    # 保存并打印按钮
    def save_clicked(self):


        # 连接数据库
        sqlite = Mysqlite('db2.db')

        # 处理加工单
        if table_name == 'jgd':
            value = str(info)[1:-1]
            sql = "SELECT * FROM jgd WHERE date = '{}' and patient = '{}'".format(info[0], info[2])
            exist = len(sqlite.select(sql))
            if exist:
                msg = self.cf_msg()
                if not msg:
                    return

            value = value + ',NULL'
            sqlite.insert_value(table_name, value)
            filename = get_word('jgd', info)

        # 处理知情同意书
        else:
            # 查找患者是否已登记过
            data = sqlite.select_data2('patient', 'id = {}'.format(int(info[5])))
            exist = len(data)
            if not exist:
                value_patient = str(info[2:6])[1:-1]
                sqlite.insert_value('patient', value_patient)
            elif data[0][0] != info[2]:
                # 待替换语句
                # QMessageBox.warning(self, '登记号重复', '输入的登记号已存在，但是患者姓名不一致，请检查！', QMessageBox.Ok)
                # return
                msg = QMessageBox.warning(self, '登记号重复', '输入的登记号已存在，但是患者姓名不一致！\n是否修改原数据？',
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if msg == QMessageBox.No:
                    return
                else:
                    sqlite.update_data('patient', 'name', info[2], int(info[5]))

            # 检查就诊内容是否重复
            sql = "SELECT * FROM visit WHERE date = '{}' and id = {} and type = {}".format(info[0], int(info[5]),
                                                                                           int(info[1]))
            exist = len(sqlite.select(sql))
            if exist:
                msg = self.cf_msg()
                if not msg:
                    return

            value_visit = []
            value_visit += info
            del value_visit[2:5]
            new_num = self.get_num(int(info[1]))
            value_visit.append(new_num + 1)
            value_visit = str(value_visit)[1:-1]
            info.append(new_num + 1)
            try:
                sqlite.insert_value('visit', value_visit)
            except Exception as e:
                QMessageBox.critical(self, '致命错误', '写入数据库错误，请重试！')
                return e
            type1 = ['by', 'rct', 'ss', 'gdxf', 'hdxf']
            filename = get_word(type1[int(info[1])], info)
        str0 = '保存成功，即将打印。\n请放入{}后，点击OK按钮。'.format((lambda x, y: x if table_name == 'jgd' else y)('加工单', '2张A4纸'))
        QMessageBox.information(self, '保存成功', str0)
        if not table_name == 'jgd':
            print_word(filename)
        print_word(filename)
        del_file(filename)
        self.pushButton_reset.click()

    # 获取自动编号
    def get_num(self, type1):
        sqlite = Mysqlite('db2.db')
        sql = "select max(num) from visit where type = {}".format(type1)
        data = eval(sqlite.select(sql))[0]
        if data is None:
            return 0
        else:
            return data

    # 重复内容信息提示
    def cf_msg(self):

        msg = QMessageBox().information(self, '重复提醒', '保存的信息可能已存在，是否仅打印文档而不保存?/nYes', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                        QMessageBox.Cancel)
        if msg == QMessageBox.Cancel:
            return -1
        elif msg == QMessageBox.No:
            return 0
        else:
            return 1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = MyMain()
    myWin.show()
    sys.exit(app.exec_())