
import math
import random
import pandas as pd
import DataInit

# 计算最短路径距离，即评价函数
def calFitness(line, dis_matrix):
  dis_sum = 0
  dis = 0
  for i in range(len(line)):
    if i < len(line) - 1:
      dis = dis_matrix.loc[line[i], line[i + 1]]  # 计算距离
      dis_sum = dis_sum + dis
    else:
      dis = dis_matrix.loc[line[i], line[0]]
      dis_sum = dis_sum + dis
  # print(dis_sum)
  return round(dis_sum, 1)


def traversal_search(line, dis_matrix):
  # 随机交换生成100个个体，选择其中表现最好的返回
  i = 0  # 生成个体计数
  line_value, line_list = [], []
  while i <= 100:
    new_line = line.copy()  # 复制当前路径
    exchange_max = random.randint(1, 5)  # 随机生成交换次数,城市数量较多时增加随机数上限效果较好
    exchange_time = 0  # 当前交换次数
    while exchange_time <= exchange_max:
      pos1, pos2 = random.randint(0, len(line) - 1), random.randint(0, len(line) - 1)  # 交换点
      new_line[pos1], new_line[pos2] = new_line[pos2], new_line[pos1]  # 交换生成新路径
      exchange_time += 1  # 更新交换次数

    new_value = calFitness(new_line, dis_matrix)  # 当前路径距离
    line_list.append(new_line)
    line_value.append(new_value)
    i += 1

  return min(line_value), line_list[line_value.index(min(line_value))]  # 返回表现最好的个体


def greedy(arr, dis_matrix):
  '''贪婪策略构造初始解'''
  # 转换格式—dis_matrix
  dis_matrix = dis_matrix.astype('float64')
  for i in range(len(arr)): dis_matrix.loc[i, i] = math.pow(10, 10)
  line = []  # 初始化
  now_city = random.randint(0, len(arr) - 1)  # 随机生成出发城市
  line.append(now_city)  # 添加当前城市到路径
  dis_matrix[dis_matrix.columns[now_city]] = math.pow(10, 10)  # 更新距离矩阵，已经过城市不再被取出
  for i in range(len(arr) - 1):
    next_city = dis_matrix.loc[now_city, :].idxmin()  # 距离最近的城市
    line.append(next_city)  # 添加进路径
    dis_matrix[dis_matrix.columns[next_city]] = math.pow(10, 10)  # 更新距离矩阵

    now_city = next_city  # 更新当前城市
  return line


def finalRoute(arr, dists):

  # SA参数
  Tend = 0.1  # 终止温度
  T = 100  # 初温
  beta = 0.99  # 退火步长

  best_value = math.pow(10, 10)  # 较大的初始值，存储最优解
  best_line = []  # 存储最优路径

  # 城市之间的距离矩阵
  dis_matrix = dists
  # 贪婪构造初始解
  line = greedy(arr, dis_matrix)
  value = calFitness(line, dis_matrix)  # 初始最短路径距离
  # 存储当前最优
  best_value, best_line = value, line

  while T >= Tend:
    new_value, new_line = traversal_search(line, dis_matrix)

    if new_value <= best_value:  # 优于最优解
      best_value, best_line = new_value, new_line  # 更新最优解
      line, value = new_line, new_value  # 更新当前解
    elif random.random() < math.exp(-(new_value - value) / T):
      line, value = new_line, new_value  # 更新当前解
    # print('当前最优值 %.1f' % (best_value))
    T *= beta

  # 路径顺序
  best_line.append(best_line[0])
  print(best_line)
  print(best_value)

  routeLocation, routename = DataInit.read_csv_route_lnglat(arr, best_line)
  return best_value, routeLocation, routename

