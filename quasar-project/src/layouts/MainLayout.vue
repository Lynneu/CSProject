<template>
  <div class="q-pa-auto">
    <q-layout view="hHh Lpr lfr">
      <q-header elevated class="bg-primary text-white q-electron-drag">
        <q-toolbar>
          <q-btn
            flat
            dense
            round
            icon="menu"
            aria-label="Menu"
            @click="lefDrawerOpen = !lefDrawerOpen"
          />
          <q-toolbar-title> Mapu </q-toolbar-title>

          <q-space />

          <div class="q-gutter-sm row items-center no-wrap">
            <q-btn round flat>
              <q-avatar size="26px">
                <img src="/src/assets/headphoto.png" />
              </q-avatar>
              <q-tooltip>Account</q-tooltip>
            </q-btn>
            <q-btn round dense flat color="text-white" icon="apps">
              <q-tooltip>Google Apps</q-tooltip>
            </q-btn>
            <q-btn round dense flat color="white" icon="notifications">
              <q-badge color="red" text-color="white" floating> 2 </q-badge>
              <q-tooltip>Notifications</q-tooltip>
            </q-btn>
            <q-bar class="q-electron-drag bg-primary">
              <q-btn dense flat icon="minimize" @click="minimize" />
              <q-btn dense flat icon="crop_square" @click="toggleMaximize" />
              <q-btn dense flat icon="close" @click="closeApp" />
            </q-bar>
          </div>
        </q-toolbar>
      </q-header>

      <q-drawer
        v-model="lefDrawerOpen"
        show-if-above
        :mini="miniState"
        @mouseover="miniState = false"
        @mouseout="miniState = true"
        mini-to-overlay
        :width="200"
        :breakpoint="500"
        bordered
        class="bg-white"
      >
        <q-list padding>
          <q-item to="/indexpage" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>

            <q-item-section> 首页 </q-item-section>
          </q-item>

          <q-item to="/todolist" exact clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="list" />
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
      </q-drawer>

      <q-page-container>
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </q-page-container>
    </q-layout>
  </div>
</template>

<script lang="ts">
import { date } from 'quasar';
import { ref } from 'vue';

export default {
  name: 'MyLayout',

  setup() {
    // we rely upon
    function minimize() {
      if (process.env.MODE === 'electron') {
        window.myWindowAPI.minimize();
      }
    }

    function toggleMaximize() {
      if (process.env.MODE === 'electron') {
        window.myWindowAPI.toggleMaximize();
      }
    }

    function closeApp() {
      if (process.env.MODE === 'electron') {
        window.myWindowAPI.close();
      }
    }

    return {
      minimize,
      toggleMaximize,
      closeApp,
      drawer: ref(false),
      miniState: ref(true),
    };
  },

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
