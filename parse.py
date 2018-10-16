import numpy
import pandas
import matplotlib.pylab as mpy
import pymysql
connect=pymysql.connect(host="127.0.0.1",user="root",passwd="643120",db="tmall",charset="utf8")
sql="select * from woods;"
data=pandas.read_sql(sql,connect)
data_transfer=data.T
y=data_transfer.values[3]
x=data_transfer.values[2]
mpy.plot(x,y,'o')
mpy.title("good-parse")
mpy.xlabel("price")
mpy.ylabel("sale")
mpy.show()