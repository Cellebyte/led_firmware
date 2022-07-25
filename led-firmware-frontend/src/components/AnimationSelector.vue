<template>
  <b-button-group>
    <b-button
      v-b-tooltip.hover.top
      title="Switch to Normal."
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
      title="Switch to the Snake."
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
      title="Switch to the Breath."
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
      title="Switch to the Rainbow."
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
      title="Switch Lights Off."
      size="lg"
      style="off"
      v-on:click="changeToOff"
    >
      <span
        v-show="off"
        class="off"
        style="padding: 0.75rem 0.5rem 0.75rem 0.5rem;"
      >Off</span>
      <span
        v-show="!off"
        style="padding: 0.75rem 0.5rem 0.75rem 0.5rem;"
      >Off</span>
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
    animation: {
      type: String,
      default: Animation.Normal,
    },
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
      this.$emit('animationUpdate', Animation.Normal);
    },
    changeToBreath() {
      this.$emit('animationUpdate', Animation.Breath);
    },
    changeToRainbow() {
      this.$emit('animationUpdate', Animation.Rainbow);
    },
    changeToSnake() {
      this.$emit('animationUpdate', Animation.Snake);
    },
    changeToOff() {
      this.$emit('animationUpdate', Animation.Off);
    },
  },
});
</script>

<style scoped>
.off {
  border: 1px solid #000000;
  border-radius: 10px;
  background-color: #000000;
  color: #ffffff;
}
</style>
