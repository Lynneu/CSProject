import itertools
import pandas as pd
import DataInit
import simulated_annealing

def held_karp(dists):
  n = len(dists)
  C = {}
  for k in range(1, n):
    C[(1 << k, k)] = (dists[0][k], 0)

  for subset_size in range(2, n):
    for subset in itertools.combinations(range(1, n), subset_size):
      bits = 0
      for bit in subset:
        bits |= 1 << bit

      for k in subset:
        prev = bits & ~(1 << k)

        res = []
        for m in subset:
          if m == 0 or m == k:
            continue
          res.append((C[(prev, m)][0] + dists[m][k], m))
        C[(bits, k)] = min(res)

  bits = (2 ** n - 1) - 1

  res = []
  for k in range(1, n):
    res.append((C[(bits, k)][0] + dists[k][0], k))
  opt, parent = min(res)

  path = []
  for i in range(n - 1):
    path.append(parent)
    new_bits = bits & ~(1 << parent)
    _, parent = C[(bits, parent)]
    bits = new_bits

  # 加入起始点
  path.append(0)
  route = list(reversed(path))
  route.append(0)

  return opt, route


def finalRoute(arr,dists):
  distance, route = held_karp(dists)
  routeLocation, routename= DataInit.read_csv_route_lnglat(arr,route)
  print(route)
  return distance, routeLocation, routename

# 测试用例
# if __name__ == '__main__':
#   arr = [1,18,5,15,6,0]
#   dists = DataInit.read_csv_distance(arr)
#   for row in dists:
#     print(''.join([str(n).rjust(4, ' ') for n in row]))
#   distance, route = held_karp(dists)
#   print(distance)
#   print(route)
#   simulated_annealing.finalRoute(arr,pd.DataFrame(dists))
