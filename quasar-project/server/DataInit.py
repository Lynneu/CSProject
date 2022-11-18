
import pandas as pd

def read_csv_distance(arr, path="test-data.csv"):
  # mapArr = arr
  # SortMapArr = sorted(mapArr)
  # print(arr)

  # 构造距离矩阵dist,初始化对角线均为0
  n = len(arr)
  dists = [[0] * n for i in range(n)]

  # 用pandas读取csv文件，返回的是一个DataFrame数组
  pd_reader = pd.read_csv(path)

  # 读取SortMapArr中选中地点的距离矩阵
  for i in range(n):
    for j in range(i + 1, n):
      dists[i][j] = dists[j][i] = pd_reader.iloc[arr[i], arr[j]]

  return dists


def read_csv_lng_lat(arr, route, path="LocationData.csv"):
  n = len(arr)
  location = []
  pd_reader = pd.read_csv(path)
# 按最短路径读取经纬度
  for i in range(n):
    location.append([pd_reader.iloc[arr[route[i]],1],pd_reader.iloc[arr[route[i]],2]])

  return location


# if __name__ == '__main__':
#    pd_reader = pd.read_csv("LocationData.csv")
#    arr = [1,16,5,15,6,0]
#    route = [0,5,1,2,3,4]
#    read_csv_lng_lat(arr, route)
