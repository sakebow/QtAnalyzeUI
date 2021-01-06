import pandas as pd
import matplotlib.pyplot as pyplot

def get_data(path, x, y):
  datas = pd.read_csv(path)
  # print(type(datas))
  data = datas[[x, y]]
  return data

if __name__ == '__main__':
  # 获取数据
  datas = pd.read_csv('/home/sakebow/python/data/germany_energy.csv')
  # 确认索引，并且替换掉原先的索引
  datas.set_index('Date', inplace=True)
  # 内置函数绘图
  datas.plot()
  # 横坐标备注
  pyplot.xlabel('date')
  # 显示图表
  pyplot.show()
  pass


  # data = get_data('/home/sakebow/python/data/germany_energy.csv', 'Date', 'Consumption')

  # data.set_index('Date', inplace=True)

  # print(data)

  # data.plot()

  # pyplot.xlabel('date')
  
  # pyplot.ylabel('consumption')
  
  # pyplot.show()

  # consumption = np.array(data.Consumption)
  # x_date = np.array(data.Date)
  # mean = np.array(roll.Consumption)

  # pyplot.figure(figsize=(20, 5))

  # pyplot.plot(x_date, consumption, 'r-')
  # pyplot.plot(x_date, roll, 'b')

  # pyplot.show()

  pass