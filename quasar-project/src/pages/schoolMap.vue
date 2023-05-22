<template>
  <q-page class="flex">
    <div>
      <div class="q-pa-md">
        <keep-alive>
          <component :is="current"></component>
        </keep-alive>
        <q-page-sticky position="top-left" :offset="[18, 18]">
          <q-btn-toggle
            v-model="current"
            spread
            no-caps
            toggle-color="primary"
            color="white"
            text-color="black"
            :options="[
              { label: '校内', value: 'schoolmap' },
              { label: '校外', value: 'allmap' },
            ]"
          />
        </q-page-sticky>
      </div>
    </div>
  </q-page>
</template>

<script>
import schoolmap from '../components/SchoolMapComponent.vue';
import allmap from '../components/AllMapComponent.vue';

export default {
  components: { schoolmap, allmap },
  data() {
    return {
      current: 'schoolmap',
    };
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
