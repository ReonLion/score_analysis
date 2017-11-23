# coding=utf-8

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from score_analysis_ui import Ui_MainWindow
import read_xls
import analyzer

class main_form(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(main_form, self).__init__()
        self.setupUi(self)
        
        # 菜单的点击事件，当点击关闭菜单时，连接槽函数close()
        self.actionClose.triggered.connect(self.close)
        # 菜单的点击事件，当点击打开菜单的时候，连接槽函数openMsg()
        self.actionOpen.triggered.connect(self.open_msg)
        # 按钮的点击事件，点击升序按钮时，升序排列
        # 使用lamda表达式传递额外的参数
        self.riseButton.clicked.connect(lambda:self.tableview_show(self.data.student_list_rise))
        # 按钮的点击事件，点击降序按钮时，降序排列
        self.lowButton.clicked.connect(lambda:self.tableview_show(self.data.student_list_low))
        # 按钮的点击事件，点击统计按钮时，画图
        self.DrawButton.clicked.connect(self.draw_bar)
        
    def open_msg(self):
        file, ok = QFileDialog.getOpenFileName(self, "Open", "C:/", "Excel Files (*.xls, *.xlsx);;All Files (*)")
        # 状态栏显示文件地址
        self.statusbar.showMessage(file)
        # 实例化一个Data_xls类，即读入数据
        self.data = read_xls.Data_xls(file)        
        #打开文件后，在tableView里显示表格信息
        self.tableview_show(self.data.student_list)
        
    def tableview_show(self, student_list):
        # 设置tableview里的item
        self.model = QStandardItemModel(len(student_list), 3)
        self.model.setHorizontalHeaderLabels(['学号', '姓名', '成绩'])
        # model可以理解为一种数据集
        for row in range(0, len(student_list)):
            item = QStandardItem(student_list[row].id)
            self.model.setItem(row, 0, item)
            item = QStandardItem(student_list[row].name)
            self.model.setItem(row, 1, item)
            item = QStandardItem(str(student_list[row].score))
            self.model.setItem(row, 2, item)
        self.tableView.setModel(self.model)
        
    def draw_bar(self):
        #对数据进行分析，画图
        data_analyzer = analyzer.Data_analyzer(self.data.student_list)        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main_form()
    win.show()
    sys.exit(app.exec_())