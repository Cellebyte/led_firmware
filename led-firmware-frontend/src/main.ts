
import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';
import I18n from 'vue-i18n';

import '@/assets/styles/custom.scss';

import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faPlusCircle, faMinusCircle, faCog, faEye, faEyeSlash,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import workerFactory from '@/registerServiceWorker';
import routerFactory from '@/router';
import Language from '@/utils/Language';
import App from '@/App.vue';
import fetchConfig from '@/config';
import storeFactory from '@/store';
import apiFactory from '@/ledFirmwareFrontend';


fetchConfig().then((config) => {
  workerFactory(config);
  // Icons
  library.add(faPlusCircle, faMinusCircle, faCog, faEye, faEyeSlash);
  Vue.component('fai', FontAwesomeIcon);

  // Make BootstrapVue available throughout your project
  Vue.use(BootstrapVue);
  // Optionally install the BootstrapVue icon components plugin
  Vue.use(IconsPlugin);

  Vue.use(I18n);
  const i18n = new I18n();
  Vue.config.productionTip = (process.env.NODE_ENV === 'development');
  Language.init(i18n);


  const api = apiFactory(config);
  const router = routerFactory(config);
  const store = storeFactory(config, api);


  Vue.mixin({
    data() {
      return {
        // Distribute runtime configs into every Vue component
        config,
      };
    },
  });

  new Vue({
    router,
    store,
    i18n,
    render: h => h(App),
  }).$mount('#app');
});
