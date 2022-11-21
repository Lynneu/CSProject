<template>
  <div id="container" class="absolute-full"></div>
  <q-page-sticky position="top-right" :offset="[18, 18]">
    <q-card class="my-card" v-show="tabvisible">
      <q-btn @click="Restart" color="primary" dense flat icon="close" />
      <q-card-section bg-color="primary">
        <div class="q-pa-xs q-gutter-md">
          <div class="text-primary text-bold">
            <q-label>您选择了{{ routename.length }}个地点</q-label>
          </div>
          <div class="text-primary text-bold">
            <q-label>
              需步行{{ distance }}米,预计耗时{{ parseInt(distance / 100) }}分钟
            </q-label>
          </div>
          <q-btn @click="Repeat" unelevated color="primary" label="再次播放" />
          <q-btn @click="clearRoute" outline color="primary" label="清除路线" />
        </div>
      </q-card-section>

      <q-tabs v-model="tab" class="text-primary">
        <q-tab label="推荐路线" name="推荐路线" />
        <q-tab label="历史规划" name="历史规划" />
      </q-tabs>

      <q-separator />
      <q-scroll-area
        :thumb-style="thumbStyle"
        :content-style="contentStyle"
        :content-active-style="contentActiveStyle"
        style="height: 212px; width: 250px"
      >
        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="推荐路线">
            <q-list separator style="max-width: 350px">
              <q-item
                v-for="(route, index) in routename"
                :key="route.index"
                clickable
                v-ripple
              >
                <q-item-section side>
                  <q-avatar
                    size="23px"
                    font-size="18px"
                    color="primary"
                    text-color="white"
                    icon="directions"
                  />
                </q-item-section>

                <q-item-section>
                  <q-item-label>{{ route }}</q-item-label>
                </q-item-section>

                <q-item-section side>
                  <q-item-label v-if="index">途径点{{ index }}</q-item-label>
                  <q-item-label v-if="!index">起点</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-tab-panel>

          <q-tab-panel name="历史规划">
            With so much content to display at once, and often so little screen
            real-estate, Cards have fast become the design pattern of choice for
            many companies, including the likes of Google and Twitter.
          </q-tab-panel>
        </q-tab-panels>
      </q-scroll-area>
    </q-card>

    <q-select
      ref="select"
      v-model="model"
      bg-color="white"
      color="primary"
      filled
      use-input
      use-chips
      multiple
      input-debounce="0"
      @new-value="createValue"
      :options="filterOptions"
      @filter="filterFn"
      v-show="selectvisible"
      dense
      style="max-width: 600px"
    >
      <template v-slot:prepend>
        <q-icon name="place" color="primary" />
      </template>
      <template v-slot:after>
        <q-btn @click="Postmap" color="primary" dense flat icon="search" />
      </template>
      <template v-if="model" v-slot:append>
        <q-icon
          name="cancel"
          @click.stop.prevent="model = null"
          class="cursor-pointer"
        />
      </template>
    </q-select>
  </q-page-sticky>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import { shallowRef } from 'vue';
import { ref } from 'vue';
import qs from 'qs';
import jsondata from '../../server/LocationData.json';

const stringOptions = [
  '第三教学楼',
  '第二教学楼',
  '材料楼',
  '信息楼',
  '科学楼',
  '第四教学楼',
  '第一教学楼',
  '数理楼',
  '经管楼',
  '实训楼',
  '人文楼',
  '学生宿舍-12号楼',
  '学生宿舍-9号楼',
  '学生宿舍-7号楼',
  '美食园',
  '天天餐厅',
  '奥运餐厅',
  '游泳馆',
  '奥林匹克体育馆',
  '南足球场',
  '篮球场',
  '北足球场',
  '逸夫图书馆',
  '校医院',
  '南门',
  '东门',
  '西门',
  '北门',
  '南区公共浴室',
  '学生公寓-2号楼',
  '学生公寓-1号楼',
  '学综楼',
  '学生公寓-3号楼',
  '北区公共浴室',
  '学生宿舍-10号楼',
  '礼堂',
  '能源楼',
  '知新园',
  '学生宿舍-8号楼',
  '艺术设计学院',
  '学生宿舍-5号楼',
  '软件楼',
];
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'gaode',
  setup() {
    const map = shallowRef(null);
    const filterOptions = ref(stringOptions);
    const distance = 0;
    const routelocation = [];
    const routename = [];
    const LocationArr = {};
    const markerList = [];
    const routemarkerList = [];
    return {
      map,
      model: ref(null),
      filterOptions,
      distance,
      routelocation,
      routename,
      LocationArr,
      togglemodel: ref('one'),
      tabvisible: ref(false),
      selectvisible: ref(true),
      tab: ref('推荐路线'),
      markerList,
      routemarkerList,
      contentStyle: {
        backgroundColor: 'rgba(0,0,0,0.02)',
        color: '#555',
      },

      contentActiveStyle: {
        backgroundColor: '#eee',
        color: 'black',
      },

      thumbStyle: {
        right: '2px',
        borderRadius: '5px',
        backgroundColor: '#027be3',
        width: '5px',
        opacity: '0.75',
      },

      createValue(val, done) {
        if (val.length > 2) {
          if (!stringOptions.includes(val)) {
            done(val, 'add-unique');
          }
        }
      },
      filterFn(val, update) {
        update(() => {
          if (val === '') {
            filterOptions.value = stringOptions;
          } else {
            const needle = val.toLowerCase();
            filterOptions.value = stringOptions.filter(
              (v) => v.toLowerCase().indexOf(needle) > -1
            );
          }
        });
      },
    };
  },
  methods: {
    initMap() {
      AMapLoader.load({
        key: '678ba1081f72cf4ac0b93ffacdd2e14f',
        version: '2.0', //指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
        plugins: [
          'AMap.moveAnimation',
          'AMap.ToolBar',
          'AMap.Marker',
          'AMap.OverView',
          'AMap.Geolocation',
        ], //需要使用的的插件列表，如比例尺'AMap.Scale'等
        AMapUI: {
          version: '1.1',
          plugins: ['overlay/SimpleMarker'],
        },
      })
        .then((AMap) => {
          this.map = new AMap.Map('container', {
            //设置地图容器id
            //viewMode: '3D', //是否为3D地图模式
            zoom: 17, //初始化地图级别
            center: [116.481686, 39.875344], //初始化地图中心点位置
            isHotspot: true,
          });
          //  this.map.addControl(new AMap.Geolocation());
          this.map.addControl(new AMap.ToolBar());
          this.LocationArr = jsondata;
          //  console.log(this.LocationArr)
          //  console.log(this.LocationArr[0])
          for (let item of this.LocationArr) {
            console.log(item['地点']);
            let marker = new AMap.Marker({
              position: [item['经度'], item['纬度']],
              title: item['地点'],
              clickable: true,
              // anchor: 'bottom-right'
            });
            this.markerList.push(marker);
          }
          this.map.add(this.markerList);
        })
        .catch((e) => {
          console.log(e);
        });
    },

    DrawRoute() {
      AMapLoader.load({
        plugins: ['AMap.moveAnimation'],
      }).then((AMap) => {
        var startIcon = new AMap.Icon({
          // 图标尺寸
          size: new AMap.Size(25, 34),
          // 图标的取图地址
          image:
            '//a.amap.com/jsapi_demos/static/demo-center/icons/dir-marker.png',
          // 图标所用图片大小
          imageSize: new AMap.Size(135, 40),
          // 图标取图偏移量
          //  imageOffset: new AMap.Pixel(-9, -3)
        });
        let marker = new AMap.Marker({
          map: this.map,
          position: this.routelocation[0],
          icon: startIcon,
          // anchor: 'center',
          //  icon: 'https://a.amap.com/jsapi_demos/static/demo-center-v2/car.png',
          // offset: new AMap.Pixel(-13, -26)
        });

        // 绘制轨迹
        var polyline = new AMap.Polyline({
          map: this.map,
          path: this.routelocation,
          showDir: true,
          strokeColor: '#28F', //线颜色
          // strokeOpacity: 1,     //线透明度
          strokeWeight: 6, //线宽
          // strokeStyle: "solid"  //线样式
        });

        var passedPolyline = new AMap.Polyline({
          map: this.map,
          // path: lineArr,
          strokeColor: '#AF5', //线颜色
          // strokeOpacity: 1,     //线透明度
          strokeWeight: 6, //线宽
          // strokeStyle: "solid"  //线样式
        });

        marker.on('moving', function (e) {
          polyline.setPath(e.passedPath);
        });
        this.map.setFitView();
        marker.moveAlong(this.routelocation, {
          // 每一段的时长
          duration: 500,
          // JSAPI2.0 是否延道路自动设置角度在 moveAlong 里设置
          autoRotation: true,
        });
      });
    },

    clearMarker() {
      if (marker) {
        marker.setMap(null);
        marker = null;
      }
    },

    routeLine() {
      var startIcon = new AMap.Icon({
        // 图标尺寸
        size: new AMap.Size(25, 34),
        // 图标的取图地址
        image:
          '//a.amap.com/jsapi_demos/static/demo-center/icons/dir-marker.png',
        // 图标所用图片大小
        imageSize: new AMap.Size(135, 40),
        // 图标取图偏移量
        imageOffset: new AMap.Pixel(-9, -3),
      });
      this.map.remove(this.markerList);
      this.routemarkerList = [];
      let marker = new AMap.Marker({
        position: this.routelocation[0],
        title: this.routename[0],
        clickable: true,
        icon: startIcon,
        // 设置了 icon 以后，设置 icon 的偏移量，以 icon 的 [center bottom] 为原点
        offset: new AMap.Pixel(-13, -30),
        // anchor: 'bottom-right'
      });
      this.routemarkerList.push(marker);
      for (let i = 1; i < this.routelocation.length - 1; i++) {
        let marker = new AMap.Marker({
          position: this.routelocation[i],
          title: this.routename[i],
          clickable: true,
        });
        this.routemarkerList.push(marker);
      }
      this.map.add(this.routemarkerList);

      AMapUI.load(['ui/misc/PathSimplifier', 'lib/$'], (PathSimplifier, $) => {
        if (!PathSimplifier.supportCanvas) {
          alert('当前环境不支持 Canvas！');
          return;
        }
        var defaultRenderOptions = {
          pathNavigatorStyle: {
            initRotateDegree: 0,
            width: 16,
            height: 25,
            autoRotate: true,
            lineJoin: 'round',
            content: 'defaultPathNavigator',
            fillStyle: '#087EC4',
            strokeStyle: '#116394', //'#eeeeee',
            lineWidth: 1,
            pathLinePassedStyle: {
              lineWidth: 5,
              strokeStyle: 'rgba(8, 126, 196, 1)',
              borderWidth: 1,
              borderStyle: '#ffffff',
              dirArrowStyle: true,
            },
          },
          renderAllPointsIfNumberBelow: 100,
        };
        var pathSimplifierIns = new PathSimplifier({
          zIndex: 100,
          //autoSetFitView:false,
          map: this.map, //所属的地图实例

          getPath: function (pathData, pathIndex) {
            return pathData.path;
          },
          getHoverTitle: function (pathData, pathIndex, pointIndex) {
            if (pointIndex >= 0) {
              //point
              return (
                pathData.name +
                '，点：' +
                pointIndex +
                '/' +
                pathData.path.length
              );
            }

            return pathData.name + '，途径点数量' + pathData.path.length - 1;
          },
          renderOptions: defaultRenderOptions,
        });

        window.pathSimplifierIns = pathSimplifierIns;
        pathSimplifierIns.setData([
          {
            name: '最短路径',
            path: this.routelocation, // data为后端接口数据
          },
        ]);

        //对第一条线路（即索引 0）创建一个巡航器
        // this.map.on('complete', function() {
        var navg1 = pathSimplifierIns.createPathNavigator(0, {
          // loop: true, //循环播放
          speed: 500, //巡航速度，单位千米/小时
        });
        navg1.start();
        // })
      });
    },
    Repeat() {
      if (window.pathSimplifierIns) {
        //通过该方法清空上次传入的轨迹
        pathSimplifierIns.setData([
          {
            name: '最短路径',
            path: this.routelocation,
          },
        ]);
      }
      pathSimplifierIns
        .createPathNavigator(0, {
          // loop: true, //循环播放
          speed: 500, //巡航速度，单位千米/小时
        })
        .start();
    },
    //清楚已绘制路径
    clearRoute() {
      if (window.pathSimplifierIns) {
        //通过该方法清空上次传入的轨迹
        pathSimplifierIns.setData();
        //销毁巡航器
        pathSimplifierIns.destroy();
      }
    },
    //清除所有绘图及信息窗
    Restart() {
      this.tabvisible = false;
      this.selectvisible = true;
      this.model = null;
      this.clearRoute();
      this.map.remove(this.routemarkerList);
      this.map.add(this.markerList);
    },
    getRouteInfo() {
      this.tabvisible = true;
      this.selectvisible = false;
    },

    Postmap() {
      var arr = [];
      // console.log(arr[0]);
      for (let key in this.model) {
        console.log(this.model[key] + '\n');
        arr.push(stringOptions.indexOf(this.model[key]));
      }
      //console.log(arr[0]);
      console.log(arr.length);
      if (arr.length) {
        this.$axios
          .post('http://127.0.0.1:5000/PostMap', { arr: arr })
          .then((rst) => {
            console.log(rst);
            this.distance = rst.data.Distance;
            this.routelocation = rst.data.RouteLocation;
            this.routename = rst.data.RouteName;
            console.log(this.distance);
            console.log(this.routelocation);
            console.log(this.routename);
            //this.DrawRoute();
            this.routeLine();
            this.getRouteInfo();
          })
          .catch((error) => {
            console.log(error);
            //this.Getmap();
          });
      }
    },
  },
  // Getmap() {
  //   this.$axios
  //     .get('http://127.0.0.1:5000/GetMap')
  //     .then((rst) => {
  //       console.log(rst);
  //       this.distance = rst.data.Distance;
  //       this.routelocation = rst.data.Routelocation;
  //       console.log(this.distance)
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // },
  //},
  mounted() {
    //DOM初始化完成进行地图初始化
    this.initMap();
  },
};
</script>

<style>
#container {
  width: 100%;
  /* height: 546px;*/
  height: 100%;
  padding: 0px;
  margin: 0px;
  /* border: 1px solid rgb(12, 88, 107);*/
}
.my-card {
  width: 100%;
  max-width: 280px;
}
</style>
