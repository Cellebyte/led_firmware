import Vue from 'vue';
import {
  AnimationsState, RootState,
} from '@/types/store';
import { Animation, AnimationObject, PolyAnimation } from '@/types/api';

export default {
  namespaced: true,

  state: {
    currentAnimation: null,
    animationOptions: {} as { [animation in Animation]: PolyAnimation },
  },

  getters: {
    activeAnimation: (state: AnimationsState) => state.currentAnimation,
    animationOptions: (state: AnimationsState) => state.animationOptions,
  },

  mutations: {
    SET_ACTIVE_ANIMATION(state: AnimationsState, animation: Animation) {
      Vue.set(state, 'currentAnimation', animation);
    },
    SET_ANIMATION_OPTIONS(
      state: AnimationsState, payload: { animation: Animation, animationOptions: PolyAnimation },
    ) {
      Vue.set(state.animationOptions, payload.animation, payload.animationOptions);
    },
  } as any,

  actions: {
    async FETCH_ANIMATION(context: { commit: any; rootState: RootState }) {
      const response = await context.rootState.api.animation.getAnimation();
      if (response.data && response.status === 200) {
        context.commit('SET_ACTIVE_ANIMATION', response.data.animation);
      }
    },
    async FETCH_ANIMATION_OPTIONS(context: {
      state: AnimationsState, commit: any; rootState: RootState
    }) {
      if (context.state.currentAnimation && [
        Animation.Breath, Animation.Normal, Animation.Rainbow, Animation.Snake,
      ].includes(context.state.currentAnimation)) {
        const response = await context.rootState.api.animation.animationDetail(
          context.state.currentAnimation,
        );
        if (response.data && response.status === 200) {
          context.commit('SET_ANIMATION_OPTIONS', { animation: context.state.currentAnimation, animationOptions: response.data });
        }
      } else {
        context.commit('SET_ANIMATION_OPTIONS', { animation: context.state.currentAnimation, animationOptions: {} as PolyAnimation });
      }
    },
    async CHANGE_ANIMATION(
      context: {
        commit: any; dispatch: any; rootState: RootState;
      },
      payload: {
        animation: Animation
      },
    ) {
      const response = await context.rootState.api.animation.putAnimation(
        { animation: payload.animation } as AnimationObject,
      );
      if (response.data && response.status === 200) {
        context.commit('currentAnimation', response.data.animation as Animation);
        context.dispatch('FETCH_ANIMATION_OPTIONS');
      }
    },
    async UPDATE_ANIMATION_OPTIONS(
      context: {
        commit: any; rootState: RootState
      },
      payload: {
        animation: Animation; animationOptions: PolyAnimation
      },
    ) {
      const response = await context.rootState.api.animation.animationUpdate(
        payload.animation, payload.animationOptions,
      );
      if (response.data && response.status === 200) {
        context.commit('SET_ANIMATION_OPTIONS', { animation: payload.animation, animationOptions: response.data });
      }
    },
  },
};
