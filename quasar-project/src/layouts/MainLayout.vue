<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="lefDrawerOpen = !lefDrawerOpen"
        />
        <q-toolbar-title>UMAP</q-toolbar-title>
        <div class="text-subtitle">{{ todaysDate }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="lefDrawerOpen"
      show-if-above
      :width="200"
      :breakpoint="400"
    >
      <q-scroll-area
        style="
          height: calc(100% - 150px);
          margin-top: 150px;
          border-right: 1px solid #ddd;
        "
      >
        <q-list padding>
          <q-item to="/" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="inbox" />
            </q-item-section>

            <q-item-section> 首页 </q-item-section>
          </q-item>

          <q-item to="/todolist" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="Todo" />
            </q-item-section>

            <q-item-section> 待办 </q-item-section>
          </q-item>

          <q-item to="/settings" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>

            <q-item-section> 设置 </q-item-section>
          </q-item>

          <q-item to="/help" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="help" />
            </q-item-section>

            <q-item-section> 帮助 </q-item-section>
          </q-item>
        </q-list>
      </q-scroll-area>

      <q-img
        class="absolute-top"
        src="https://cdn.quasar.dev/img/material.png"
        style="height: 150px"
      >
        <div class="absolute-bottom bg-transparent">
          <q-avatar size="56px" class="q-mb-sm">
            <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
          </q-avatar>
          <div class="text-weight-bold">小U</div>
          <div>@Lynneu</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
      <keep-alive>
        <router-view />
      </keep-alive>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { date } from 'quasar';

export default {
  name: 'MyLayout',

  data() {
    return {
      lefDrawerOpen: false,
    };
  },
  computed: {
    todaysDate() {
      const timeStamp = Date.now();
      return date.formatDate(timeStamp, 'dddd D MMMM');
    },
  },
};
</script>
