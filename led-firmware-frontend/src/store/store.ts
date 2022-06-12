import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';
import VuexPersist from 'vuex-persist';
import Pool from '@/store/modules/Pool';
import { RootState } from '@/types/store';
import { Api } from '@/types/api';
import { LedFirmwareFrontendConfiguration } from '@/types/config';

export default function storeFactory(config: LedFirmwareFrontendConfiguration, API: Api) {
  Vue.use(Vuex);

  const debug = process.env.NODE_ENV !== 'production';

  const vuexLocalStorage = new VuexPersist({
    key: 'vuex', // The key to store the state on in the storage provider.
    storage: window.localStorage, // or window.sessionStorage or localStorage
    // Function that passes the state and returns the state with only the objects you want to store.
    reducer: (state: any) => ({
      Auth: state.Auth,
    }),
  });

  const storeOptions: StoreOptions<RootState> = {
    state: {
      version: '1.0.0', // a simple property
      config,
      api: API,
    },
    modules: {
      // CIDR,
      Pool,
      // Search,
      // Auth,
      // Token,
      // AuthOIDC,
    },
    plugins: [vuexLocalStorage.plugin],
    strict: debug,
  };
  return new Vuex.Store<RootState>(storeOptions);
}
