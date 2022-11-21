<template>
  <div id="container" class="absolute-full"></div>
  <q-page-sticky position="top-right" :offset="[18, 18]">

      <q-input
        v-model="model"
        bg-color="white"
        id="tipinput"
        color="primary"
        filled
        input-debounce="0"
        style="max-width: 280px"
        dense
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
      </q-input>
  </q-page-sticky>
</template>

<script>
import AMapLoader from '@amap/amap-jsapi-loader';
import { shallowRef } from 'vue';
import { ref } from 'vue';
import qs from 'qs'
import jsondata from '../../server/LocationData.json';

const stringOptions = [


];
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'gaode',
  setup() {
    const map = shallowRef(null);
    const filterOptions = ref(stringOptions);
    const distance = 0;
    const routelocation = [];
    const LocationArr = {};

    return {
      map,
      model: ref(null),
      filterOptions,
      distance,
      routelocation,
      LocationArr,
      togglemodel: ref('one'),
      selectvisible: ref(true),
      createValue(val, done) {
        if (val.length > 2) {
          if (!stringOptions.includes(val)) {
            done(val, 'add-unique');
          }
        }
      },

    };
  },
  methods: {
    initMap() {
      AMapLoader.load({
        key: '678ba1081f72cf4ac0b93ffacdd2e14f',
        version: '2.0', //指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
        plugins: ['AMap.moveAnimation','AMap.ToolBar','AMap.Marker', 'AMap.OverView','AMap.Geolocation'], //需要使用的的插件列表，如比例尺'AMap.Scale'等
        AMapUI:{
                    version:'1.1',
                    'plugins':['overlay/SimpleMarker'],
                },
      })
        .then((AMap) => {
          this.map = new AMap.Map('container', {
            //设置地图容器id
            //viewMode: '3D', //是否为3D地图模式
            zoom: 12, //初始化地图级别
            center: [116.397, 39.918], //初始化地图中心点位置
            isHotspot: true
          });
        //  this.map.addControl(new AMap.Geolocation());
        this.map.addControl(new AMap.ToolBar())
        let marker = new AMap.Marker({
              position: [116.397, 39.918],
              clickable: true,
             // anchor: 'bottom-right'
            });
            this.map.add(marker);
            this.searchPlace();
        })
        .catch((e) => {
          console.log(e);
        });
    },
    searchPlace() {
      AMap.plugin(['AMap.Autocomplete', 'AMap.PlaceSearch'], function() {
        const autoOptions = {
          // 使用联想输入的input的div的id
          input: 'tipinput'
        }
        const autocomplete = new AMap.Autocomplete(autoOptions)
        const placeSearch = new AMap.PlaceSearch({
          city: '长沙',
          map: this.map
        })
        AMap.event.addListener(autocomplete, 'select', function(e) {
          console.log(e.poi.location) // 获取选中的的地址的经纬度
          placeSearch.search(e.poi.name)
        })
      })
    }

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
 /* height: 546px;*/
 height: 100%;
 padding: 0px;
        margin: 0px;
  /* border: 1px solid rgb(12, 88, 107);*/
}
</style>
