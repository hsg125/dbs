from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from data import *
import sys
from db import *


class CallData(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(CallData, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(688, 462)
        self.lineEdit.setFocus()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # self.cBox1.currentIndexChanged.connect(self.cbox_change)
        # self.cBox2.currentIndexChanged.connect(self.cbox_change)
        self.cBox1.activated.connect(self.cbox_change)
        self.cBox2.activated.connect(self.cbox_change)
        self.btn1.clicked.connect(self.search)
        self.tableWidget.doubleClicked.connect(self.row_dclick)
        self.btn_del.clicked.connect(self.deldata)
        self.btn_modify.clicked.connect(self.row_dclick)
        self.info = []
        self.btn_modify.setEnabled(0)

    def deldata(self):
        info = self.tableWidget.selectedItems()
        if len(info):
            if info[-1].text().isnumeric():
                tab = 'jgd'
                where = 'num = {}'.format(info[-1].text())
            else:
                tab = 'visit'
                ls = ['拔牙', '根管治疗', '手术', '固定修复', '活动修复']

                where = "num = {} and id = {} and type={}".format(info[0].text(), info[1].text(),
                                                                  ls.index(info[6].text()))

            msg = QMessageBox.critical(self, '警告', '正在删除记录,删除后将无法恢复!\n确认删除吗?', QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if msg == QMessageBox.Yes:
                mysql = Mysqlite('db2.db')
                try:
                    mysql.delete_data(tab, where)
                    QMessageBox.information(self, '完成', '删除成功！', QMessageBox.Ok)
                    self.btn1.click()
                except Exception as e:
                    QMessageBox.critical(self, '错误', '删除失败，请重试！\n' + str(e), QMessageBox.Ok)
            else:
                return

    def cbox_change(self):
        if not self.cBox1.currentIndex():
            self.cBox2.setCurrentIndex(0)
            self.cBox2.setEnabled(0)
        else:
            self.cBox2.setEnabled(1)
        self.lineEdit.setFocus()

    # 查找数据库并显示在表格中
    def search(self):
        t1 = self.cBox1.currentIndex()
        t2 = self.cBox2.currentIndex()
        self.tableWidget.clear()
        text = self.lineEdit.text()
        mysql = Mysqlite('db2.db')
        type_str = "Case type when 0 then '拔牙' when 1 then '根管治疗' when 2 then '手术' when 3 then '固定修复' when 4 then " \
                   "'活动修复' End As 'type' "
        sex = "Case sex when 0 then '女' when 1 then '男' End as sex"
        if not t1:
            if text == '':
                sql = "select date,patient,type,color,position,text, num from jgd order by num desc"
            else:
                sql = "select date,patient,type,color,position,text, num from jgd where patient = '{}' order by num " \
                      "desc".format(text)

        elif text == '':
            sql = "select num,patient.id,name,{},age,date,{},disease,position,anesthesia,position from patient," \
                  "visit where patient.id=visit.id order by date desc".format(sex, type_str)
        else:
            if t2:
                condition = 'patient.id'
            else:
                condition = 'name'
                text = "'" + text + "'"
            sql = "select num,patient.id,name,{},age,date,{},disease,position,anesthesia from patient," \
                  "visit where patient.id=visit.id and {}={} order by date desc".format(sex, type_str, condition, text)

        if 'jgd' in sql:
            header = ['日期', '姓名', '类型', '颜色', '牙位', '备注', '编号']
            self.tableWidget.setColumnCount(7)
        else:
            header = ['编号', '登记号', '姓名', '性别', '年龄', '日期', '类型', '诊断', '牙位', '麻醉方式']
            self.tableWidget.setColumnCount(10)

        self.tableWidget.setHorizontalHeaderLabels(header)
        data = mysql.select(sql)
        row = len(data)
        # vol = len(data[0])
        # 遍历二维元组, 将 id 和 name 显示到界面表格上
        self.tableWidget.setRowCount(row)
        # self.tableWidget.setColumnCount(vol)

        for i in range(row):
            for j in range(self.tableWidget.columnCount()):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableWidget.setItem(i, j, data1)

        if self.tableWidget.columnCount():
            self.btn_modify.setEnabled(1)
        else:
            self.btn_modify.setEnabled(0)

    def row_dclick(self):
        for x in self.tableWidget.selectedItems():
            self.info.append(x.text())
        if self.cBox1.currentIndex():
            self.info.append(0)
        else:
            self.info.append(1)
        self.btn2.click()

    def printData(self):
        info = self.tableWidget.selectedItems()
        if len(info):
            if info[-1].text().isnumeric():
                tab = 'jgd'
                where = 'num = {}'.format(info[-1].text())
            else:
                tab = 'visit'
                ls = ['拔牙', '根管治疗', '手术', '固定修复', '活动修复']

                where = "num = {} and id = {} and type={}".format(info[0].text(), info[1].text(),
                                                                  ls.index(info[6].text()))

            msg = QMessageBox.information(self, '打印', '是否重新打印选择的项目?', QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.No)
            if msg == QMessageBox.Yes:
                mysql = Mysqlite('db2.db')
                try:
                    mysql.delete_data(tab, where)
                    QMessageBox.information(self, '完成', '删除成功！', QMessageBox.Ok)
                    self.btn1.click()
                except Exception as e:
                    QMessageBox.critical(self, '错误', '删除失败，请重试！\n' + str(e), QMessageBox.Ok)
            else:
                return

    # @staticmethod
    # def getinfo(parent=None):
    #     pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myWin = CallData()
    myWin.show()
    sys.exit(app.exec_())
