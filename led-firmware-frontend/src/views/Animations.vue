<template>
  <div class="animation">
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <animation-selector :enableOffButton="false" @animationUpdate="onAnimationsUpdate" />
      </b-row>
      <b-row class="row d-flex justify-content-center">
        <snake-animation-form />
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import SnakeAnimationForm from '@/components/SnakeAnimationForm.vue';
import AnimationSelector from '@/components/AnimationSelector.vue';
import { Animation } from '@/types/api';

@Component({
  data() {
    return {
      animation: Animation.Normal,
    };
  },
  components: {
    AnimationSelector,
    SnakeAnimationForm,
  },
  methods: {
    onAnimationsUpdate(animation: Animation) {
      console.log(animation);
    },
  },
})
export default class AnimationsVue extends Vue { }
</script>
