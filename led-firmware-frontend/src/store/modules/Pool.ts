import Vue from 'vue';
import { Animation } from '@/types/api';

export default {
  namespaced: true,

  state: {
    palettes: {},
  },

  getters: {
    // poolList: (state: PoolState) => Object.values(state.pools),
  },

  mutations: {
    // SET_POOLS(state: PoolState, pools: Pool[]) {
    //   pools.forEach((pool) => {
    //     Vue.set(state.pools, pool.id, pool);
    //   });
    // },
    // SET_POOL(state: PoolState, pool: Pool) {
    //   Vue.set(state.pools, pool.id, pool);
    // },
    // DELETE_POOL(state: PoolState, id: string) {
    //   Vue.delete(state.pools, id);
    // },
  },

  actions: {
    // async FETCH_POOLS(context: { commit: any; rootState: RootState }) {
    //   const response = await context.rootState.api.pool.poolList();
    //   if (response.data && response.status === 200) {
    //     context.commit('SET_POOLS', response.data);
    //     response.data.forEach((pool: Pool) => {
    //       context.commit('CIDR/SET_CIDRS', pool.prefixes, { root: true });
    //     });
    //   }
    // },
    // async UPDATE_POOL(
    //   context: { commit: any; rootState: RootState },
    //   payload: { poolID: string; formData: Pool },
    // ) {
    //   const response = await context.rootState.api.pool.poolUpdate(
    //     payload.poolID,
    //     payload.formData,
    //   );
    //   if (response.status === 200) {
    //     context.commit('SET_POOL', response.data);
    //   } else {
    //     console.log(response);
    //   }
    // },
    // async CREATE_POOL(context: { commit: any; rootState: RootState }, formData: Pool) {
    //   const response = await context.rootState.api.pool.poolCreate(formData);
    //   if (response.status === 201) {
    //     context.commit('SET_POOL', response.data);
    //   } else {
    //     console.log(response);
    //   }
    // },
    // async DELETE_POOL(context: { commit: any; rootState: RootState }, poolID: string) {
    //   const response = await context.rootState.api.pool.poolDelete(poolID);
    //   if (response.status === 204) {
    //     context.commit('DELETE_POOL', poolID);
    //   } else {
    //     console.log(response);
    //   }
    // },
    // async ASSIGN(
    //   context: { commit: any; rootState: RootState },
    //   payload: { poolID: string; assignmentData: Assignment },
    // ) {
    //   const response = await context.rootState.api.pool.poolAssignCreate(
    //     payload.poolID,
    //     payload.assignmentData,
    //   );
    //   return new Promise((resolve, reject) => {
    //     if (response.status === 201 && response.data) {
    //       context.commit('CIDR/SET_CIDRS', response.data.assignments, { root: true });
    //       resolve(response.data);
    //     } else {
    //       console.log(response);
    //       reject();
    //     }
    //   });
    // },
  },
};
