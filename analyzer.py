# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from read_xls import Student

class Data_analyzer():
    def __init__(self, student_list, ax, canvas):
        self.score_list = []
        for student in student_list:
            self.score_list.append(student.score)
        
        # 画直方图
        self.draw_bar(ax, canvas, self.score_list)
        # 计算占比
        self.data_report(self.score_list)
        
        
    # 画直方图
    def draw_bar(self, ax, canvas, score_list):
        self.count = []
        self.count.append(len([score for score in score_list if score < 60]))                    # 0-59人数
        self.count.append(len([score for score in score_list if 60 <= score < 70]))
        self.count.append(len([score for score in score_list if 70 <= score < 80]))
        self.count.append(len([score for score in score_list if 80 <= score < 90]))
        self.count.append(len([score for score in score_list if 90 <= score <= 100]))            # 90-100人数
        x = np.arange(5)
        y = self.count
        ax.bar(x, y)
        ax.set_xticklabels(['0-59', '60-69', '70-79', '80-89', '90-100'])
        ax.grid(False)
        canvas.draw()
        
    # 数据报告
    def data_report(self, score_list):
        # 将列表转换为numpy的数组，便于更多的分析    
        score_array = np.array(score_list)
        # 计算平均值
        self.mean = np.mean(score_array)
        # 计算标准差
        self.std = np.std(score_array)        
        
        self.rate = []
        for i in self.count:
            self.rate.append(i / len(self.score_list))