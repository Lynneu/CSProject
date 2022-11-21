
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import itertools
import random
import sys
import pandas as pd
import held_karp
import DataInit
import simulated_annealing

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
@app.route('/PostMap', methods=['POST'])
def get_route():
    distance = 0
    routeLocation = []
    routeName = []
    response_object = {'status': 'success'}
    arr = request.get_json()['arr']
    print(arr)
    dists = DataInit.read_csv_distance(arr)
    print(dists)
    if(len(arr) < 15):
      distance, routeLocation, routeName = held_karp.finalRoute(arr, pd.DataFrame(dists))
    else:
      distance, routeLocation, routeName = simulated_annealing.finalRoute(arr,pd.DataFrame(dists))
    response_object['Distance'] = json.dumps(int(distance))
    response_object['RouteLocation'] = routeLocation
    response_object['RouteName'] = routeName
    print(distance)
    print(routeLocation)
    print(routeName)
    return jsonify(response_object)

@app.route('/GetMap', methods=['GET'])
def get_map_position():
  return jsonify({
    'status': 'success',
    'Position': DataInit.read_csv_all_lnglat()
  })

if __name__ == "__main__":
    app.run()

