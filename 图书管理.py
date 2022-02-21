from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QTableWidgetItem, QCheckBox, QAbstractItemView, QHeaderView, QLabel, QFrame  # 使用的界面库为PYQT5
from GUI import Ui_Dialog  # 导入ui件中的类#ss是ui转换后的py文件，Ui_Form是文件中的类名
import sys  # 创建和关闭进程
import sqlite3  # python内置数据库


class win(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        # self.resize(300,300)
        self.setupUi(self)  # 执行类中的setupUi函数
        self.exe = "     执行: "
        self.output = "     输出: "
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()
        self.tableName = "一些图书信息"
        print("数据库打开成功")

        self.pushButton.clicked.connect(self.add_book)
        self.pushButton_2.clicked.connect(self.Query)
        self.pushButton_3.clicked.connect(self.del_book)
        self.pushButton_4.clicked.connect(self.change_book)
        self.pushButton_5.clicked.connect(self.ReFalsh)
        self.pushButton_6.clicked.connect(self.ReFalsh)
        self.tableWidget_3.clicked.connect(self.chang_line_edit)

    def __del__(self):
        print("释放数据库实例")
        self.cursor.close()
        self.conn.close()

    # 增删改查等功能

    def __Insert(self, fieldNames, fieldValues):
        """
        插入数据
        :param fieldNames: 字段list
        :param fieldValues: 值list
        """
        # 通过fieldNames解析出字段名
        try:
            names = ""  # 字段名，用于插入数据
            nameTypes = ""  # 字段名及字段类型，用于创建表
            for index in range(fieldNames.__len__()):
                if index != fieldNames.__len__() - 1:
                    names += fieldNames[index] + ","
                    nameTypes += fieldNames[index] + " text,"
                else:
                    names += fieldNames[index]
                    nameTypes += fieldNames[index] + " text"
            # 通过fieldValues解析出字段对应的值
            values = ""
            for index in range(fieldValues.__len__()):
                cell_value = str((fieldValues[index]))
                if isinstance(fieldValues[index], float):
                    cell_value = str((int)(fieldValues[index]))
                if index != fieldValues.__len__() - 1:
                    values += "\'" + cell_value + "\',"
                else:
                    values += "\'" + cell_value + "\'"
            print(values)
            # 将fieldValues解析出的值插入数据库
            sql = 'insert into %s(%s) values(%s)' % (self.tableName, names, values)
            print(self.exe + sql)
            try:
                self.cursor.execute(sql)
            except:
                print("插入失败，检查sql执行情况")
            self.conn.commit()
        except:
            print("插入失败，检查__Insert函数")

    def add_book(self):
        try:
            fieldNames = ['图书编号', '图书名称', '作者', '出版社', '定价', '借出状态', '借出时间']
            borrowed = "借出" if self.checkBox.isChecked() else "未借出"
            time = self.lineEdit_7.text() if self.checkBox.isChecked() else "-"

            fieldValues = [self.lineEdit.text(),  # 编号
                           self.lineEdit_2.text(),  # 名称
                           self.lineEdit_3.text(),  # 作者
                           self.lineEdit_4.text(),  # 出版社
                           self.lineEdit_6.text(),  # 定价
                           borrowed,  # 借出状态
                           time  # 借出时间
                           ]
            # print(fieldValues)
            self.__Insert(fieldNames, fieldValues)  # 数据插入到数据库中

        except:
            print("插入失败，add_book函数")

    def del_book(self):
        tableName = "一些图书信息"

        row = self.tableWidget.currentRow()  # 获取选中文本所在的行

        #print(self.tableWidget.item(row,0).text())

        try:
            sql = 'DELETE FROM %s WHERE 图书编号 = \'%s\'' % (tableName,self.tableWidget.item(row,0).text())
            self.cursor.execute(sql)
            print(self.exe + sql)  # 删除目标信息
        except:
            print("检查删除sql语句执行情况")
        self.conn.commit()


    def chang_line_edit(self):
        tableName = "一些图书信息"
        try:
            row = self.tableWidget_3.currentRow()  # 获取选中文本所在的行
            self.lineEdit_8.setText(self.tableWidget_3.item(row, 0).text())
            self.lineEdit_9.setText(self.tableWidget_3.item(row, 1).text())
            self.lineEdit_10.setText(self.tableWidget_3.item(row, 2).text())
            self.lineEdit_11.setText(self.tableWidget_3.item(row, 3).text())
            self.lineEdit_12.setText(self.tableWidget_3.item(row, 4).text())
            self.checkBox_2.setChecked(False) if self.tableWidget_3.item(row,5).text() == "未借出" else self.checkBox_2.setChecked(True)
            self.lineEdit_13.setText(self.tableWidget_3.item(row, 6).text())
            #print(self.tableWidget_3.item(row, 0).text())
        except:
            print("检查tableWidgetd_3的选择功能")

    def change_book(self):
        tableName = "一些图书信息"
        try:
            row = self.tableWidget_3.currentRow()  # 获取选中文本所在的行

            print(self.tableWidget_3.item(row,0).text())
        except:
            print("检查tableWidgetd的选择功能")
        try:
            sql = 'DELETE FROM %s WHERE 图书编号 = %s ' % (tableName,self.tableWidget_3.item(row,0).text())
            self.cursor.execute(sql)
            #print(self.exe + sql)  # 删除目标信息
        except:
            print("检查修改sql语句执行情况")
        self.conn.commit()
        try:
            fieldNames = ['图书编号', '图书名称', '作者', '出版社', '定价', '借出状态', '借出时间']
            borrowed = "借出" if self.checkBox_2.isChecked() else "未借出"
            time = self.lineEdit_13.text() if self.checkBox_2.isChecked() else "-"

            fieldValues = [self.lineEdit_8.text(),  # 编号
                           self.lineEdit_9.text(),  # 名称
                           self.lineEdit_10.text(),  # 作者
                           self.lineEdit_11.text(),  # 出版社
                           self.lineEdit_12.text(),  # 定价
                           borrowed,  # 借出状态
                           time  # 借出时间
                           ]
            # print(fieldValues)
            self.__Insert(fieldNames, fieldValues)  # 数据插入到数据库中

        except:
            print("修改失败，change_book函数")


    def Query(self):  #
        """
        查找数据表中的数据
        :param tableName:表名
        """
        tableName = "一些图书信息"
        x = str(self.lineEdit_5.text())
        try:
            print("查询表 " + tableName)
            sql = 'select * from %s' % tableName
            self.cursor.execute(sql)
            if x != "":
                sql = 'select * from %s' % tableName
            else:
                sql = 'select * from %s WHERE %s in 图书名称' % (tableName, x)
            print(self.exe + sql)
        except:
            print("检查查询函数的sql语句执行情况")

        results = self.cursor.fetchall()  # 获取所有记录列表

        cheat = []

        if x != "":
            for i in results:
                for j in i:
                    if x in j or j in x:
                        cheat.append(i)
                        break
                        # print(cheat)
            results = cheat

        index = 0
        self.tableWidget_2.clearContents()
        for i in range(0, self.tableWidget_2.rowCount())[::-1]:
            self.tableWidget_2.removeRow(i)
            # print(i)
        for row in results:
            try:
                row_tw = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_tw)
                for r in range(len(row)):
                    self.tableWidget_2.setItem(row_tw, r, QTableWidgetItem(row[r]))
            except:
                print("检查qt5 数据插入")
            print(self.output + "index=" + index.__str__() + " detail=" + str(row))  # 打印结果
            index += 1
        print(self.output + "共计" + results.__len__().__str__() + "条数据")

    def ReFalsh(self):
        tableName = "一些图书信息"
        sql = 'select * from %s' % tableName
        self.cursor.execute(sql)
        results = self.cursor.fetchall()  # 获取所有记录列表
        print(self.exe + sql)
        index = 0
        self.tableWidget.clearContents()
        self.tableWidget_3.clearContents()
        for i in range(0, self.tableWidget.rowCount())[::-1]:
            self.tableWidget.removeRow(i)
            self.tableWidget_3.removeRow(i)
            # print(i)
        for row in results:
            try:
                row_tw = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_tw)
                self.tableWidget_3.insertRow(row_tw)
                for r in range(len(row)):
                    self.tableWidget.setItem(row_tw, r, QTableWidgetItem(row[r]))
                    self.tableWidget_3.setItem(row_tw, r, QTableWidgetItem(row[r]))
            except:
                print("检查qt5 数据插入")
            print(self.output + "index=" + index.__str__() + " detail=" + str(row))  # 打印结果
            index += 1
        print(self.output + "共计" + results.__len__().__str__() + "条数据")
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(app.exec_())
