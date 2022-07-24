<template>
  <div class="animation">
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <animation-selector :enableOffButton="false" @animationUpdate="onAnimationsUpdate" />
      </b-row>
      <b-row class="row d-flex pt-5 justify-content-center">
        <animation-form :animation="animation" />
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import AnimationForm from '@/components/AnimationForm.vue';
import AnimationSelector from '@/components/AnimationSelector.vue';
import { Animation } from '@/types/api';

@Component({
  data() {
    return {
      animation: null,
    };
  },

  components: {
    AnimationSelector,
    AnimationForm,
  },
  methods: {
    onAnimationsUpdate(animation: Animation) {
      this.animation = animation;
    },
  } as any,
})
export default class AnimationsVue extends Vue { }
</script>
