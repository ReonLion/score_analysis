# coding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from read_xls import Student

class Data_analyzer():
    def __init__(self, student_list):
        score_list = []
        for student in student_list:
            score_list.append(student.score)
        #print([score for score in score_list])
        self.bar(score_list)
        
    # 画直方图
    def bar(self, score_list):
        count_0_60 = len([score for score in score_list if score < 60])
        count_60_70 = len([score for score in score_list if 60 <= score < 70])
        count_70_80 = len([score for score in score_list if 70 <= score < 80])
        count_80_90 = len([score for score in score_list if 80 <= score < 90])
        count_90_100 = len([score for score in score_list if 90 <= score <= 100])
        x = np.arange(5)
        y = [count_0_60, count_60_70, count_70_80, count_80_90, count_90_100]
        plt.bar(x, y)
        plt.show()