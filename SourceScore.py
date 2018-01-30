# -*- encoding:utf8 -*-
'''
Purpose:对资源数据进行打分
author:liupu
Time:2018-01-29
Description:First Version
'''
import numpy as np 

Index = int(input("请输入你需要进行得分评估的资源数据类型，其中：0代表幼儿园"))

def score(x):
	Score = []
	qt98 = np.pencentile(x,98)
	qt05 = np.pencentile(x,5)
	for num in x:
		if num > qt98:
			anum = 10
		elif num < qt05:
			anum = 2
		elif num == 0:
			anum = 1
		else:
			anum = (num-qt05)/(qt98-qt05)*8+2
		Score.append(anum)

