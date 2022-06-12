
import Vue from 'vue';
import Router from 'vue-router';
import { LedFirmwareFrontendConfiguration } from '@/types/config';
import Home from '@/views/Home.vue';

export default function routerFactory(config: LedFirmwareFrontendConfiguration) {
  Vue.use(Router);
  const router = new Router({
    base: `${config.baseURL}`,
    mode: 'history',
    routes: [
      {
        path: '/',
        alias: '/home',
        name: 'Home',
        component: Home,
      },
      // {
      //   path: '/cidrs',
      //   name: 'CIDR',
      //   component: () => import(/* webpackChunkName: "cidrs" */ './views/CIDRs.vue'),
      // },
      // {
      //   path: '/pools',
      //   name: 'Pool',
      //   component: () => import(/* webpackChunkName: "pools" */ './views/Pools.vue'),
      // },
      // {
      //   path: '/tokens',
      //   name: 'Token',
      //   component: () => import(/* webpackChunkName: "tokens" */ './views/Token.vue'),
      // },
      // {
      //   path: '/profile',
      //   name: 'Profile',
      //   component: () => import(/* webpackChunkName: "cidrs" */ './views/Profile.vue'),
      // },
      {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '@/views/About.vue'),
      },
    ],
  });
  return router;
}
