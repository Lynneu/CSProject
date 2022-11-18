
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import itertools
import random
import sys
import pandas as pd
import held_karp
import DataInit

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
    distance = 0
    routeLocation = []
    response_object = {'status': 'success'}
    if request.method == 'POST':
      arr = request.get_json()['arr']
      print(arr)
      dists = DataInit.read_csv_distance(arr)
      print(dists)
      distance, routeLocation = held_karp.finalRoute(arr,dists)
      response_object['Distance'] = json.dumps(int(distance))
      response_object['RouteLocation'] = routeLocation
      print(distance)
      print(routeLocation)
    return jsonify(response_object)

if __name__ == "__main__":
    app.run(host='10.27.112.2',port=5000,debug=True)

