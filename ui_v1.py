# -*- coding: utf-8 -*-

'''
亮点：
1、使用Dataframe将原有的索引替换为日期并进行分析
2、算法部分，使用一行代码将月份和季节对应起来
3、窗体部分，使用继承来实现复用（将具有相同属性的查ungti抽象出父类，各自复写）
4、将窗体的各子控件分步骤封装并加入窗体控件：设置初始位置--设置子控件--使用管道赋予子控件的事件--将子控件放在窗体控件内
5、预测部分使用线性回归
'''

import sys
from PyQt5.QtGui import QFont
import qtawesome as qta
from matplotlib import pyplot
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from PyQt5.Qt import Qt, QWidget, QGridLayout, QApplication, QPushButton, QLabel

# 算法部分
class AnalyzeAlg(object):
  def __init__(self):
    super().__init__()
    self.all_data = pd.read_csv('/home/sakebow/python/data/germany_energy.csv')
    # 确认索引，并且替换掉原先的索引
    self.all_data.set_index('Date', inplace=True)
    self.date_index = pd.to_datetime(self.all_data.index)
    # 将月份与季度对应起来，并作为新列加入数据集中
    self.all_data['Season'] = self.date_index.month.map(dict(zip(range(1, 13), [1,1,2,2,2,3,3,3,4,4,4,1])))
    pass
  # 直接显示所有数据在同一张表上
  def show_all_data(self):
    self.all_data.plot()
    pyplot.xlabel('date')
    pyplot.show()
    pass
  # 显示2006年的所有数据
  def show_data_in_2006(self):
    self.all_data.loc['2006-01-01' : '2006-12-31']['Consumption'].plot()
    pyplot.title('show data of 2006')
    pyplot.xlabel('date')
    pyplot.show()
    pass
  # 根据季节显示数据
  def show_data_in_season(self, x):
    # 各季节数据
    spring_data = np.array(self.all_data[x].dropna(axis=0, how='all').loc[self.all_data['Season'].isin([2])])
    summer_data = np.array(self.all_data[x].dropna(axis=0, how='all').loc[self.all_data['Season'].isin([3])])
    autumn_data = np.array(self.all_data[x].dropna(axis=0, how='all').loc[self.all_data['Season'].isin([4])])
    winter_data = np.array(self.all_data[x].dropna(axis=0, how='all').loc[self.all_data['Season'].isin([1])])
    # 各季节均值
    spring_mean = np.full(len(spring_data), spring_data.mean())
    summer_mean = np.full(len(summer_data), summer_data.mean())
    autumn_mean = np.full(len(autumn_data), autumn_data.mean())
    winter_mean = np.full(len(winter_data), winter_data.mean())
    # 横坐标范围
    spring_x = np.arange(1, len(spring_data) + 1, 1)
    summer_x = np.arange(1, len(summer_data) + 1, 1)
    autumn_x = np.arange(1, len(autumn_data) + 1, 1)
    winter_x = np.arange(1, len(winter_data) + 1, 1)
    # 分表展示
    spring_figure = pyplot.subplot(221)
    spring_figure.set_title('spring')
    summer_figure = pyplot.subplot(222)
    summer_figure.set_title('summer')
    autumn_figure = pyplot.subplot(223)
    autumn_figure.set_title('autumn')
    winter_figure = pyplot.subplot(224)
    winter_figure.set_title('winter')
    spring_figure.plot(spring_x, spring_data, 'r')
    spring_figure.plot(spring_x, spring_mean, 'g')
    summer_figure.plot(summer_x, summer_data, 'orange')
    summer_figure.plot(summer_x, summer_mean, 'b')
    autumn_figure.plot(autumn_x, autumn_data, 'g')
    autumn_figure.plot(autumn_x, autumn_mean, 'r')
    winter_figure.plot(winter_x, winter_data, 'b')
    winter_figure.plot(winter_x, winter_mean, 'orange')
    # 确认间距
    pyplot.tight_layout()
    pyplot.show()
    pass
  # 显示每周的平均耗电量
  def show_data_in_week(self):
    self.all_data['Weekday'] = self.date_index.weekday
    self.all_data.groupby('Weekday')['Consumption'].mean().plot()
    pyplot.title('show consumption in week')
    pyplot.show()
    pass
  # 根据指定的字段显示数据
  def show_all_data_for_field(self, field):
    self.all_data[field].plot()
    pyplot.title(f'show data for {field}')
    pyplot.show()
    pass
  # 预测模型
  def predict_model(self):
    self.all_wind_data = np.array(self.all_data['Wind+Solar'].dropna(axis=0, how='all')).reshape(-1, 1)
    self.all_consumption_data = self.all_data['Consumption'].loc[self.all_data['Wind+Solar'].dropna(axis=0, how='all').index]
    x_axis = np.arange(1, len(self.all_wind_data) + 1, 1).reshape(-1, 1)
    linear_regression = LinearRegression()
    linear_regression.fit(x_axis, self.all_wind_data)
    return linear_regression.coef_[0][0], linear_regression.intercept_
    pass
  # 预测风力发电
  def predict_wind(self):
    k, b = self.predict_model()
    x_axis = np.arange(1, len(self.all_wind_data) + 1, 1)
    y_axis = list(map(lambda x: k * x + b, x_axis))
    pyplot.scatter(np.arange(1, len(self.all_wind_data) + 1, 1), self.all_wind_data)
    pyplot.plot(x_axis, y_axis, 'r')
    pyplot.plot(x_axis, self.all_consumption_data, 'orange')
    pyplot.plot(x_axis, np.full(len(x_axis), self.all_consumption_data.mean()), 'g')
    pyplot.title('consumption(orange) & wind+solar(blue)')
    pyplot.show()
    pass
  # 闰年检测
  def is_leap_year(self, year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
      return True
    return False
    pass
  # 天数改为日期
  def days2date(self, days):
    init_year = 2018
    init_month = 1
    while (days > 365):
      if self.is_leap_year(init_year):
        days -= 366
      else:
        days -= 365
        pass
      init_year += 1
      pass
    while (days > 31):
      if init_month in [1, 3, 5, 7, 8, 10,12]:
        days -= 31
      elif init_month in [4, 6, 9, 11]:
        days -= 30
      elif self.is_leap_year(init_year) and init_month == 2:
        days -= 29
      else:
        days -= 28
        pass
      init_month += 1
      if init_month == 13:
        init_month = 1
      pass
    init_date = days
    return init_year, init_month, init_date
    pass

  pass

# provide default values
class QWindow(QWidget):
  def __init__(self, parent=None, flags=Qt.WindowFlags()):
    super().__init__(parent=parent, flags=flags)
    # set x, y, width, height for ui
    self.WINDOW_MAX_WIDTH = QApplication.desktop().width()
    self.WINDOW_MAX_HEIGHT = QApplication.desktop().height()
    self.WINDOW_INIT_HEIGHT = int(self.WINDOW_MAX_HEIGHT / 2)
    self.WINDOW_INIT_WIDTH = int(self.WINDOW_MAX_WIDTH / 2)
    self.X = int(self.WINDOW_MAX_WIDTH / 4)
    self.Y = int(self.WINDOW_MAX_HEIGHT / 4)
    # set x, y, width, height for box
    self.BOX_WIDTH = int(self.WINDOW_INIT_WIDTH / 2)
    self.BOX_HEIGHT = int(self.WINDOW_INIT_HEIGHT / 2)
    self.BOX_X = int(self.WINDOW_MAX_WIDTH *3 / 8)
    self.BOX_Y = int(self.WINDOW_MAX_HEIGHT * 3 / 8)
    # set height for buttons
    self.BUTTON_HEIGHT = int(self.WINDOW_INIT_HEIGHT / 6)
    pass
  pass

# main window
class QAnalyzeUI(QWindow):
  def __init__(self, parent = None, flags = Qt.WindowFlags()):
    super().__init__(parent = parent, flags = flags)
    # set grid layout
    self.window_grid_layout = QGridLayout()
    self.window_grid_layout.setContentsMargins(0, 0, 0, 0)
    self.init_layout()
    self.init_widgets()
    self.finish_layout()
    self.events_of_window()
    self.message_box = MessageWindow(text = 'Here goes something you must attention before it\'s too late', title = 'Hey, there!', type = True)
    self.error_box = MessageWindow(text = 'It seems something wrong here...', title = 'Hey, STOP!', type = False)
    # alg settings
    self.alg = AnalyzeAlg()
    pass

  def init_layout(self):
    self.resize(self.WINDOW_INIT_WIDTH, self.WINDOW_INIT_HEIGHT)
    self.move(self.X, self.Y)
    self.setWindowTitle('genrmany energy analysis')
    self.setWindowIcon(qta.icon('fa5s.broadcast-tower', color='white'))
    # basic function
    pass

  def init_widgets(self):
    # basic functions
    self.about_btn = QPushButton(qta.icon('fa5s.lightbulb', color = 'black'), 'About')
    self.window_grid_layout.addWidget(self.about_btn, 0, 0, 1, 5)
    
    self.exit_btn = QPushButton(qta.icon('fa5s.skull', color = 'red'), 'Exit')
    self.window_grid_layout.addWidget(self.exit_btn, 0, 6, 1, 5)

    self.all_data_btn = QPushButton(qta.icon('fa5s.database', color = 'skyblue'), 'View ALL consumption')
    self.window_grid_layout.addWidget(self.all_data_btn, 1, 1, 2, 3)

    self.year_data_btn = QPushButton(qta.icon('fa5s.calendar', color = 'navy'), 'View consumption in 2006')
    self.window_grid_layout.addWidget(self.year_data_btn, 1, 7, 2, 3)

    self.season_data_btn = QPushButton(qta.icon('fa5s.crow', color = 'black'), 'View consumption in SEASON')
    self.window_grid_layout.addWidget(self.season_data_btn, 3, 1, 2, 3)

    self.week_data_btn = QPushButton(qta.icon('fa5s.calendar-alt', color = 'crimson'), 'View consumption in WEEK')
    self.window_grid_layout.addWidget(self.week_data_btn, 3, 7, 2, 3)

    self.all_solar_btn = QPushButton(qta.icon('fa5s.cloud-sun', color = 'orange'), 'View ALL solar')
    self.window_grid_layout.addWidget(self.all_solar_btn, 5, 1, 2, 3)

    self.season_solar_btn = QPushButton(qta.icon('fa5s.cloud', color = 'grey'), 'View solar in SEASON')
    self.window_grid_layout.addWidget(self.season_solar_btn, 5, 7, 2, 3)

    self.all_wind_btn = QPushButton(qta.icon('fa5s.cannabis', color = 'olive'), 'View ALL wind')
    self.window_grid_layout.addWidget(self.all_wind_btn, 7, 1, 2, 3)

    self.appro_wind_btn = QPushButton(qta.icon('fa5s.chart-line', color = 'green'), 'View APPROXIMATE wind')
    self.window_grid_layout.addWidget(self.appro_wind_btn, 7, 7, 2, 3)
    pass

  def finish_layout(self):
    self.setLayout(self.window_grid_layout)
    pass

  def predict_info_function(self):
    self.alg.predict_wind()
    k, b = self.alg.predict_model()
    days = int((self.alg.all_consumption_data.mean() - b) / k)
    self.message_box.icon_label.setText('Prediction')
    self.message_box.message.setText(f'The Wind & Solar will replace coal in {self.alg.days2date(days)[0]}-{self.alg.days2date(days)[1]}-{self.alg.days2date(days)[2]}')
    self.message_box.show()
    pass

  def show_about(self):
    self.message_box.message.setText('Author: sakebow\nApplication: Energy Analysis')
    self.message_box.show()
    pass

  def events_of_window(self):
    self.about_btn.clicked.connect(lambda: self.show_about())
    self.exit_btn.clicked.connect(lambda: self.close())
    self.all_data_btn.clicked.connect(lambda: self.alg.show_all_data())
    self.year_data_btn.clicked.connect(lambda: self.alg.show_data_in_2006())
    self.season_data_btn.clicked.connect(lambda: self.alg.show_data_in_season('Consumption'))
    self.week_data_btn.clicked.connect(lambda: self.alg.show_data_in_week())
    self.all_solar_btn.clicked.connect(lambda: self.alg.show_all_data_for_field('Solar'))
    self.season_solar_btn.clicked.connect(lambda: self.alg.show_data_in_season('Solar'))
    self.all_wind_btn.clicked.connect(lambda: self.alg.show_all_data_for_field('Wind'))
    self.appro_wind_btn.clicked.connect(lambda: self.predict_info_function())
    pass

  pass

# message box
'''
# window
icon
title
# content
type - True: info; False: error;
content
'''
class MessageWindow(QWindow):
  def __init__(self, text, title = 'Hey, there!', type = True, parent = None, flags = Qt.WindowFlags()):
    super().__init__(parent = parent, flags = flags)
    # set grid layout
    self.window_grid_layout = QGridLayout()
    self.window_grid_layout.setContentsMargins(0, 0, 0, 0)
    self.init_layout(title)
    self.init_widgets(type, text)
    self.finish_layout()
    pass

  def init_layout(self, title):
    self.resize(self.BOX_WIDTH, self.BOX_HEIGHT)
    self.move(self.BOX_X, self.BOX_Y)
    self.setWindowTitle(title)
    pass

  def init_widgets(self, type, text):
    self.icon_label = QLabel()
    if type == True:
      self.icon_label.setText('Information')
    else:
      self.icon_label.setText('ERROR')
    self.icon_label.setFont(QFont('Ubuntu', 30, QFont.Bold))
    self.icon_label.setAlignment(Qt.AlignCenter)

    self.message = QLabel()
    self.message.setText(text)
    self.message.setFont(QFont('Ubuntu', 14))
    self.message.setAlignment(Qt.AlignCenter)
    self.message.setWordWrap(True)
    self.window_grid_layout.addWidget(self.icon_label, 0, 0, 1, 3)
    self.window_grid_layout.addWidget(self.message, 1, 0, 1, 3)
    pass

  def finish_layout(self):
    self.setLayout(self.window_grid_layout)
    pass
  
  pass

if __name__ == '__main__':
  app = QApplication(sys.argv)
  ui = QAnalyzeUI()
  ui.show()
  sys.exit(app.exec())
  pass