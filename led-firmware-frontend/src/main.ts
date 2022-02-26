/* eslint-disable import/extensions */
import { createApp } from 'vue';
import BootstrapVue3 from 'bootstrap-vue-3';
// Import Bootstrap an BootstrapVue CSS files (order is important)
import './registerServiceWorker';
import router from './router';
import store from './store';
import App from './App.vue';
import './assets/styles/app.scss';

createApp(App).use(BootstrapVue3).use(store)
  .use(router)
  .mount('#app');
