<template>
  <b-button-group>
    <b-button
      v-b-tooltip.hover.top
      title="Switch to the Normal. Animation"
      style="normal"
      size="md"
      v-on:click="changeToNormal"
    >
      <b-img
        v-show="normal"
        width="42px"
        :src="require('@/assets/Normal_on_small.png')"
      />
      <b-img
        v-show="!normal"
        width="42px"
        :src="require('@/assets/Normal_off_small.png')"
      />
    </b-button>
    <b-button
      v-b-tooltip.hover.top
      title="Switch to the Snake." Animation
      size="lg"
      style="snake"
      v-on:click="changeToSnake"
    >
      <b-img
        v-show="snake"
        width="42px"
        :src="require('@/assets/Snake_on_small.png')"
      />
      <b-img
        v-show="!snake"
        width="42px"
        :src="require('@/assets/Snake_off_small.png')"
      />
    </b-button>
    <b-button
      v-b-tooltip.hover.top
      title="Switch to the Breath. Animation"
      size="lg"
      style="breath"
      v-on:click="changeToBreath"
    >
      <b-img
        v-show="breath"
        width="42px"
        :src="require('@/assets/Breath_on_small.png')"
      />
      <b-img
        v-show="!breath"
        width="42px"
        :src="require('@/assets/Breath_off_small.png')"
      />
    </b-button>
    <b-button
      v-b-tooltip.hover.top
      title="Switch to the Rainbow Animation."
      size="lg"
      style="rainbow"
      v-on:click="changeToRainbow"
    >
      <b-img
        v-show="rainbow"
        width="42px"
        :src="require('@/assets/Rainbow_on_small.png')"
      />
      <b-img
        v-show="!rainbow"
        width="42px"
        :src="require('@/assets/Rainbow_off_small.png')"
      />
    </b-button>
    <b-button
      v-if="enableOffButton"
      v-b-tooltip.hover.top
      title="Switch to Off Animation"
      size="lg"
      style="rainbow"
      v-on:click="changeToOff"
    >
      Off
    </b-button>
  </b-button-group>
</template>
<script lang="ts">
import Vue from 'vue';
import { Animation } from '@/types/api';

export default Vue.extend({
  name: 'animation-selector',
  props: {
    enableOffButton: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      animation: Animation.Normal,
    };
  },
  computed: {
    normal() {
      return this.animation === Animation.Normal;
    },
    snake() {
      return this.animation === Animation.Snake;
    },
    breath() {
      return this.animation === Animation.Breath;
    },
    rainbow() {
      return this.animation === Animation.Rainbow;
    },
    off() {
      return this.animation === Animation.Off;
    },
  } as any,
  methods: {
    changeToNormal() {
      this.animation = Animation.Normal;
      this.$emit('animationUpdate', this.animation);
    },
    changeToBreath() {
      this.animation = Animation.Breath;
      this.$emit('animationUpdate', this.animation);
    },
    changeToRainbow() {
      this.animation = Animation.Rainbow;
      this.$emit('animationUpdate', this.animation);
    },
    changeToSnake() {
      this.animation = Animation.Snake;
      this.$emit('animationUpdate', this.animation);
    },
    changeToOff() {
      this.animation = Animation.Off;
      this.$emit('animationUpdate', this.animation);
    },
  },
});
</script>

<style scoped>
</style>
