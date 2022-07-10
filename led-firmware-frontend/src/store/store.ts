import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import VuexPersist from 'vuex-persist';
import { RootState } from '@/types/store';
import { Api } from '@/types/api';
import { LedFirmwareFrontendConfiguration } from '@/types/config';
import ColourPalettes from '@/store/modules/ColourPalettes';
import Animations from '@/store/modules/Animations';

export default function storeFactory(config: LedFirmwareFrontendConfiguration, API: Api) {
  Vue.use(Vuex);

  const debug = process.env.NODE_ENV !== 'production';

  const vuexLocalStorage = new VuexPersist({
    key: 'vuex', // The key to store the state on in the storage provider.
    storage: window.localStorage, // or window.sessionStorage or localStorage
  });

  const storeOptions: StoreOptions<RootState> = {
    state: {
      version: '1.0.0', // a simple property
      config,
      api: API,
    },
    modules: {
      ColourPalettes,
      Animations,
    },
    plugins: [vuexLocalStorage.plugin],
    strict: debug,
  };
  return new Vuex.Store<RootState>(storeOptions);
}
