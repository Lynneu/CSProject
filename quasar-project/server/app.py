"""
测试Flask
"""
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import itertools
import random
import sys
import pandas as pd

# 配置参数,开启debug模式,json转换中文不使用unicode
DEBUG = True
JSON_AS_ASCII = False

# 实例化Flask
app = Flask(__name__)
app.config.from_object(__name__)

# 开启CORS,解决跨域调用问题
CORS(app, resources={r'/*': {'origins': '*'}})
# 也可以简单直接写CORS(app)

# 配置路由
@app.route('/PostMap', methods=['GET', 'POST'])
def all_map():
    response_object = {'status': 'success'}
    if request.method == 'POST':
      InitMap(request.data)
    else:
      response_object['route'] = routeForPrinting


def held_karp(dists):
  n = len(dists)
  C = {}
  for k in range(1, n):
    C[(1 << k, k)] = (dists[0][k], 0)

  for subset_size in range(2, n):
    for subset in itertools.combinations(range(1, n), subset_size):
      # Set bits for all nodes in this subset
      bits = 0
      for bit in subset:
        bits |= 1 << bit

      # Find the lowest cost to get to this subset
      for k in subset:
        prev = bits & ~(1 << k)

        res = []
        for m in subset:
          if m == 0 or m == k:
            continue
          res.append((C[(prev, m)][0] + dists[m][k], m))
        C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
  bits = (2 ** n - 1) - 1

  # Calculate optimal cost
  res = []
  for k in range(1, n):
    res.append((C[(bits, k)][0] + dists[k][0], k))
  opt, parent = min(res)

  # Backtrack to find full path
  path = []
  for i in range(n - 1):
    path.append(parent)
    new_bits = bits & ~(1 << parent)
    _, parent = C[(bits, parent)]
    bits = new_bits

  # Add implicit start state
  path.append(0)

  return opt, list(reversed(path))


def generate_distances(n):
  dists = [[0] * n for i in range(n)]
  for i in range(n):
    for j in range(i + 1, n):
      dists[i][j] = dists[j][i] = random.randint(1, 99)

  return dists


def InitMap(arr):
  mapArr = arr
  SortMapArr = sorted(mapArr)


def read_csv(path="test-data.csv"):
  dists = []
  with open(path, 'rb') as f:
    for line in f:
      # Skip comments
      if line[0] == '#':
        continue
      dists.append(map(int, map(str.strip, line.split(','))))
  # for num in SortMapArr:
  #  dist = dist
  return dists


def finalRoute(dists):
  distance, route = held_karp(dists)
  routeForPrinting = [x + 1 for x in route]
  return routeForPrinting


if __name__ == "__main__":
    app.run()

