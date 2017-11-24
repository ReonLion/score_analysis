# coding=utf-8

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from score_analysis_ui import Ui_MainWindow
import read_xls
import analyzer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # matplotlib对PyQt4的支持
from matplotlib.figure import Figure

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
        # 按钮的点击事件，点击调整按钮时，进行调整
        self.adjustButton.clicked.connect(self.adjust_button_clicked)
        # 输入提示
        self.lineEdit.setPlaceholderText('请输入数字')
        # 搜索操作
        self.search_lineEdit.setPlaceholderText('搜索名字')
        self.search_lineEdit.textChanged.connect(self.search)
        
        # 初始化容器frame中的matplotlib区域
        self.create_figures()
        self.create_layouts()
        
    # 创建matplotlib的画布
    def create_figures(self):
        self.fig = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111) # 增加subplot
        self.ax.hold(True)
        self.initializeFigure()
        
    def initializeFigure(self):
        self.ax.set_xticks([0, 1, 2, 3, 4, 5])
        self.ax.grid(True)
        
    # 在frame中引入水平布局，将matplotlib画布加入其中
    def create_layouts(self):
        layout = QHBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        
    def open_msg(self):
        file, ok = QFileDialog.getOpenFileName(self, "Open", "C:/", "Excel Files (*.xls, *.xlsx);;All Files (*)")
        # 状态栏显示文件地址
        self.statusbar.showMessage(file)
        # 实例化一个Data_xls类，即读入数据
        self.data = read_xls.Data_xls(file)        
        # 打开文件后，在tableView里显示表格信息
        self.tableview_show(self.data.student_list)
        # 打开文件后，画直方图
        self.draw_bar()
        # 打开文件后，在tableView2里显示统计信息
        # 必须放在上一句后面，因为用到了self.data_analyzer
        self.tableview2_show(row = 0)
        
    def tableview_show(self, student_list):
        # 设置tableview里的item
        model = QStandardItemModel(len(student_list), 3)
        model.setHorizontalHeaderLabels(['学号', '姓名', '成绩'])
        # model可以理解为一种数据集
        for row in range(0, len(student_list)):
            item = QStandardItem(student_list[row].id)
            model.setItem(row, 0, item)
            item = QStandardItem(student_list[row].name)
            model.setItem(row, 1, item)
            item = QStandardItem(str(student_list[row].score))
            model.setItem(row, 2, item)
        self.tableView.setModel(model)
        
    # 主要是对self.data_analyzer中的各种属性进行显示处理
    # 所以， 按下调整按钮后，先对data_analyzer处理，再调用此项, 传入参数row=1，对第二行进行显示
    def tableview2_show(self, row):
        # 设置tableview里的item
        # 调整前的第一次显示，进行初始化
        if row == 0:
            self.model = QStandardItemModel(2, 8)
            self.model.setHorizontalHeaderLabels(['平均', '不及格', '60-69', '70-79', '80-89', '90-100', '总人数', '标准差'])
            self.model.setVerticalHeaderLabels(['调整前', '调整后'])
        
        # 对'平均'项进行显示
        item = QStandardItem('%.2f' % self.data_analyzer.mean)
        # 设置文字居中进行显示
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(row, 0, item)
        
        #对每个分段的占比进行显示
        for i in range(0, len(self.data_analyzer.rate)):
            item = QStandardItem('%.2f' % (self.data_analyzer.rate[i] * 100) + r'%')
            # 设置文字居中进行显示
            item.setTextAlignment(Qt.AlignCenter)
            self.model.setItem(row, i + 1, item)
        
        # 对总人数进行显示
        item = QStandardItem('%.2f' % len(self.data.student_list))
        # 设置文字居中进行显示
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(row, 6, item)
        
        # 对标准差进行显示
        item = QStandardItem('%.2f' % self.data_analyzer.std)
        # 设置文字居中进行显示
        item.setTextAlignment(Qt.AlignCenter)
        self.model.setItem(row, 7, item)
        
        # 在tableview2中显示
        self.tableView2.setModel(self.model)
        
    def draw_bar(self):
        #对数据进行分析，画图
        self.data_analyzer = analyzer.Data_analyzer(self.data.student_list, self.ax, self.canvas)
        
    def adjust_button_clicked(self):
        if self.num_radioButton.isChecked():
            self.adjust_num()                      # 调用根据分数调整的方法
        elif self.rate_radioButton.isChecked():
            self.adjust_rate()                     # 调用根据比例调整的方法
    
    def adjust_num(self):
        pass
    
    def adjust_rate(self):
        # 调整的及格率
        rate_60 = float(self.lineEdit.text())
        # 调整后的student_list
        student_list = self.data.student_list_low.copy()
        # 调整后及格的人数
        count_60 = int(len(student_list) * rate_60 + 1)
        # 选择最后一个及格的人, 计算其与60分的差距
        delta = 60 - student_list[count_60 - 1].score
        # 将所有人都加上这个分数，大于100的为100，小于0的为0
        for i in range(0, len(student_list)):
            student_list[i].score += delta
            if student_list[i].score > 100:
                student_list[i].score = 100
            elif student_list[i].score < 0:
                student_list[i].score = 0
        
        # 获取调整后的成绩列表
        score_list = []
        for student in student_list:
            score_list.append(student.score)
        print(score_list)
        print(count_60)
        # 对调整后的score_list进行分析
        self.data_analyzer.draw_bar(self.ax, self.canvas, score_list)
        self.data_analyzer.data_report(score_list)
        # 在tableview2中显示调整后这一行
        self.tableview2_show(row = 1)
        # 在tableview中显示调整后的成绩
        self.tableview_show(student_list)
        
    def adjust_num(self):
        # 调整的及格分数
        num_60 = float(self.lineEdit.text())
        
    def search(self):
        keyword = self.search_lineEdit.text()
        if keyword == '':
            self.tableview_show(self.data.student_list)
        else:
            student_list_search = self.data.student_search(keyword)
            self.tableview_show(student_list_search)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = main_form()
    win.show()
    sys.exit(app.exec_())