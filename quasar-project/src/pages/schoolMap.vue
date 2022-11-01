<template>
  <q-page class="flex">
    <div>
      <div id="container" class="absolute-full"></div>
      <div class="row q-pa-sm">
        <q-page-sticky position="top-right" :offset="[18, 18]">
          <q-select
            ref="select"
            v-model="model"
            bg-color="grey-3"
            color="primary"
            filled
            use-input
            use-chips
            multiple
            input-debounce="0"
            @new-value="createValue"
            :options="filterOptions"
            @filter="filterFn"
            style="width: 250px"
            dense
          >
            <template v-slot:prepend>
              <q-icon name="place" color="primary" />
            </template>
            <template v-slot:after>
              <q-btn @click="Postmap" dense flat icon="search" />
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
      </div>
    </div>
  </q-page>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import { shallowRef } from 'vue';
import { ref } from 'vue';
import axios from 'src/boot/axios';

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
  '天天餐厅(工业大学店)',
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

    return {
      map,
      model: ref(null),
      filterOptions,

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
        plugins: [''], //需要使用的的插件列表，如比例尺'AMap.Scale'等
      })
        .then((AMap) => {
          this.map = new AMap.Map('container', {
            //设置地图容器id
            //viewMode: '3D', //是否为3D地图模式
            zoom: 17, //初始化地图级别
            center: [116.481686, 39.875344], //初始化地图中心点位置
          });
        })
        .catch((e) => {
          console.log(e);
        });
    },
    Postmap() {
      var arr = [];
      // console.log(arr[0]);
      for (let key in this.model) {
        console.log(this.model[key] + '\n');
        arr.push(stringOptions.indexOf(this.model[key]));
      }
      console.log(arr);
      this.$axios
        .post('http://localhost:5000/PostMap', arr)
        .then(() => {
          this.Getmap();
          //this.result = rst.data;
        })
        .catch((error) => {
          console.log(error);
          this.Getmap();
        });
    },
    Getmap() {
      this.$axios
        .get('http://localhost:5000/PostMap')
        .then((rst) => {
          console.log(rst);
          this.result = rst.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    //DOM初始化完成进行地图初始化
    this.initMap();
  },
};
</script>

<style>
#container {
  width: 100%;
  height: 546px;

  /* border: 1px solid rgb(12, 88, 107);*/
}
</style>
