# -*- coding: utf-8 -*-
"""
Purpose：对来自于58同城以及来自赶集网的租房数据进行清洗
Author: Liupu
Time: 2018-01-12
Description: First Version

"""

# =================导入数据分析必需数据包===================
import numpy as np
import pandas as pd

# =================建立导出文件名称列表=====================
fileName = ['赶集-广州','58-广州','赶集-佛山','58-佛山']

# =================导入数据分析源数据=======================
# 输入数据源代码
Index = int(input('请输入你的数据源选择,0代表广州赶集网数据，1代表广州58网数据，2代表佛山赶集网数据，3代表佛山市58网数据，请确认你的输入:'))

# 将数据源代码转换为数据文件名
if Index == 0:
    Data = 'GZ_gj'
elif Index == 1:
    Data = 'GZ_58'
elif Index == 2:
    Data = 'FS_gj'
elif Index == 3:
    Data = 'FS_58'

data = pd.read_excel(Data + '.xlsx',header=0) # 读取数据
#  对来源于赶集网的数据表相关字段进行统一命名
if Index == 0 or Index == 2:
   data = data.rename(columns={'sArea':'sDistrict','sAcreage':'sArea','项目名称':'sName'})
else:
    pass


# ====================数据清洗=========================
# ====================添加辅助列=======================
#  增加五列数据，并对其进行初始化
data['Dummy'] = ''
data['Area'] = ''
data['Price'] = ''
data['House'] = ''
data['Unitprice'] = ''

#  定义辅助函数
def fenge(Ref,ind):
    ''' Ref指需要进行分割操作的数据列，Obj指分割后形成的数据列，
    ind是一个判别值，用于指定分割时采用的算法，ind=0时分割户型
    ind=1时分割面积；ind=3时分割租金 '''
    if ind == 0:
        return float(Ref[0])
    elif ind == 1:
        return float(Ref[0:-1])
    elif ind == 3:
        return float(len(Ref))
    elif Index == 0 or Index == 2 and ind == 2:
        return float(Ref[:])
    elif Index == 1 or Index == 3 and ind == 2:
        return float(Ref[0:-3])

# ==========1、数据初步清洗，删除其中无效数据==========
data.drop(data[data.newcode.isnull()].index,inplace=True)  # 删除数据表中newcode为空的记录
data=data.drop_duplicates(subset=['newcode','sType','sArea','sPrice'],keep='last')  # 即删除数据表中sPrice,sArea,sType以及newcode均相同的数据记录
data.drop(data[data.sPrice == '面议'].index,inplace=True)         # 删除数据表中价格为面议的记录

#  对新增加的数据列进行计算赋值
data.Dummy = [fenge(Ref,3) for Ref in data.sName]
data.Area = [fenge(Ref,1) for Ref in data.sArea]
data.Price = [fenge(Ref,2) for Ref in data.sPrice]
data.House = [fenge(Ref,0) for Ref in data.sType]
data.Unitprice = list(np.array(data.Price)/np.array(data.Area))


# ==========2、数据二次清洗，剔除其中不合理的小区名称==========

#  删除sName字符数超过20的记录
data.drop(data[np.array(data.Dummy) >= 15].index,inplace=True)

# =========2、数据清洗，剔除数据表中不合理数据=========
'''
数据不合理的相关标准：
    1、sArea过大或者太小，将sArea超过600或者小于12的予以删除；
    2、sPrice过大或者太小，将sPrice超过20000或者小于400的予以删除；
    3、删除单位租金Unitprice不合理的数据记录，即删除单位租金小于10或者单位租金大于200的数据记录
    4、删除户型与面积不匹配的记录，即sType和sPrice不匹配的记录：
       a、一室的户型面积不能大于60；
       b、二室的面积不能小于40，且不能大于100；
       c、三室的面积不能小于60，且不能大于200；
       d、四室的面积不能小于80；
       e、五室的面积不能小于90；
       f、六室的面积不能小于100；
       g、七室的面积不能小于120；
       h、八室的面积不能小于140；
       i、九室的面积不能小于160
    5、删除面积与租金不匹配的记录，即sArea和sPrice不匹配的记录：
       步骤：计算出没平米的租金价格；剔除单位租金价格小于10或者大于250的记录；
       对于每个小区的单位租金价格进行3西格玛剔除。如果小区数目小于4，则剔除最
       高者与最低值，否则计算单位租金的标准差和均值，剔除其中租金单位价格大于
       均值+-3*标准差的记录
'''

# 删除数据表中单位租金Unitprice出现极值的数据记录
data.drop(data[np.logical_or(data.Unitprice <= 10,data.Unitprice >= 200)].index,inplace=True)
# 删除数据表中sArea和sPrice不合理的数据记录
data.drop(data[np.logical_or(data.Area <= 12,data.Area >= 600)].index,inplace=True)
data.drop(data[np.logical_or(data.Price.astype('float') <= 400,data.Price.astype('float') >= 20000)].index,inplace=True)

# 删除户型与面积不匹配的记录
data.drop(data[np.logical_and(data.House == 1,data.Area >= 60)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 2,np.logical_or(data.Area <= 40, data.Area >= 100))].index,inplace=True)
data.drop(data[np.logical_and(data.House == 3,np.logical_or(data.Area <= 60, data.Area >= 200))].index,inplace=True)
data.drop(data[np.logical_and(data.House == 4,data.Area <= 80)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 5,data.Area <= 90)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 6,data.Area <= 100)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 7,data.Area <= 120)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 8,data.Area <= 140)].index,inplace=True)
data.drop(data[np.logical_and(data.House == 9,data.Area <= 160)].index,inplace=True)

# 删除面积与租金不匹配的记录
ID = list(set(data.newcode))

for Value in ID:
    if data[data.newcode==Value].shape[0] <= 4:
        continue
    elif 4 < data[data.newcode==Value].shape[0] < 8:
        data.drop(data[data.newcode==Value].Unitprice.argmax(),inplace = True)
        data.drop(data[data.newcode==Value].Unitprice.argmin(),inplace = True)
    else:
        data.drop(data[data.newcode==Value][np.array(data[data.newcode==Value].Unitprice) >=
        np.mean(data[data.newcode==Value].Unitprice)+2*np.std(data[data.newcode==Value].Unitprice)].index,inplace=True)
        data.drop(data[data.newcode==Value][np.array(data[data.newcode==Value].Unitprice) <= 
        np.mean(data[data.newcode==Value].Unitprice)-2*np.std(data[data.newcode==Value].Unitprice)].index,inplace=True)


# ======================删除辅助列==========
data.drop(['House','Area','Price','Dummy','Unitprice'],axis=1,inplace=True)

# ======================导出数据========================
data.to_excel(fileName[Index]+'.xlsx')            