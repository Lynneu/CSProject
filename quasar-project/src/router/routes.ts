import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/indexpage', component: () => import('pages/schoolMap.vue') },
      { path: '/help', component: () => import('pages/HelpPage.vue') },
      { path: '/settings', component: () => import('pages/SettingsPage.vue') },
      { path: '/todolist', component: () => import('pages/TodoList.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
