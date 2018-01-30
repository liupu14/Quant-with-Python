# -*- encoding:UTF-8 -*-
'''
Purpose:使用python绘制各类常用商用图形
Author:liupu
Date:2018-01-30
Description:本模块中包含了日常办公中常用商用图形的绘制函数，在使用中只需要调用相关函数并输入参数后便可以生成相关的商业图形
Version:First Version
'''

# =================================象限图==========================================
def QuadrantPlot(x,y):
	'''
	函数QuadrantPlot(x,y)被用来绘制四象限图，x为相关的X轴变量，y为Y轴的相关变量，一般为列表
	'''
	import numpy as np
	import matplotlib.pyplot as plt
	x_length = len(x)
	y_length = len(y)
	if x_length <= 1 or y_length <= 1:
		print("请检查你的输入，本函数主要操作于向量数据上")
		print(QuadrantPlot.__doc__)
		break
	else:
		plt.figure()
		ax = plt.gca()
		ax.spines['top'].set_color('none')
		ax_spines['right'].set_color('none')
		ax_spines['left'].set_position(('data',np.mean(x)))
		ax_spines['bottom'].set_position(('data',np_mean(y)))
		plt.show()

