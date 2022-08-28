import { Animation, AnimationObject, PolyAnimation } from '@/types/api';
import {
  Action, Module, Mutation, VuexModule,
} from 'vuex-module-decorators';

@Module({ namespaced: true })
class Animations extends VuexModule {
    public currentAnimation: Animation | null = null;

    public animationOptions: {
      [animation in Animation]: PolyAnimation} = {} as {
        [animation in Animation]: PolyAnimation }

    get getActiveAnimation() : Animation | null {
      return this.currentAnimation;
    }

    get getAnimationOptions(): {[animation in Animation]: PolyAnimation} {
      return this.animationOptions;
    }

    get getActiveAnimationOptions(): PolyAnimation {
      if (this.currentAnimation) {
        return this.animationOptions[this.currentAnimation];
      } return {};
    }

    @Mutation
    SET_ACTIVE_ANIMATION(animation: Animation) {
      this.currentAnimation = animation;
    }

    @Mutation
    SET_ANIMATION_OPTIONS(value: {animation: Animation, animationOptions: PolyAnimation}) {
      this.animationOptions[value.animation] = value.animationOptions;
    }

    @Action({ rawError: true })
    async FETCH_ANIMATION() {
      const response = await this.context.rootState.api.animation.getAnimation();
      if (response.data && response.status === 200) {
        this.context.commit('SET_ACTIVE_ANIMATION', response.data.animation);
      }
    }

    @Action({ rawError: true })
    async FETCH_ANIMATION_OPTIONS() {
      if (this.context.getters.getActiveAnimation && [
        Animation.Breath, Animation.Normal, Animation.Rainbow, Animation.Snake,
      ].includes(this.context.getters.getActiveAnimation)) {
        const response = await this.context.rootState.api.animation.animationDetail(
          this.context.getters.getActiveAnimation,
        );
        if (response.data && response.status === 200) {
          this.context.commit('SET_ANIMATION_OPTIONS', { animation: this.context.getters.getActiveAnimation, animationOptions: response.data });
        }
      } else {
        this.context.commit('SET_ANIMATION_OPTIONS', { animation: this.context.getters.getActiveAnimation, animationOptions: {} as PolyAnimation });
      }
    }

    @Action({ rawError: true })
    async CHANGE_ANIMATION(
      animation: Animation,
    ) {
      const response = await this.context.rootState.api.animation.putAnimation(
        { animation } as AnimationObject,
      );
      if (response.data && response.status === 201) {
        this.context.commit('SET_ACTIVE_ANIMATION', response.data.animation);
        this.context.dispatch('FETCH_ANIMATION_OPTIONS');
      }
    }

    @Action({ rawError: true })
    async UPDATE_ANIMATION_OPTIONS(
      value: {
      animation: Animation, animationOptions: PolyAnimation},
    ) {
      const response = await this.context.rootState.api.animation.animationUpdate(
        value.animation, value.animationOptions,
      );
      if (response.data && response.status === 200) {
        this.context.commit('SET_ANIMATION_OPTIONS', { animation: value.animation, animationOptions: response.data });
      }
    }
}

export default Animations;
