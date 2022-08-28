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
import {
  Component, Prop, Vue, Emit,
} from 'vue-property-decorator';
import { Animation } from '@/types/api';


@Component({
  name: 'animation-selector',
})
export default class AnimationSelector extends Vue {
  @Prop({ default: true }) readonly enableOffButton!: boolean;

  @Prop({ default: Animation.Normal }) readonly animation!: Animation;

  private privateAnimation: Animation = Animation.Off;

  created(): void {
    this.privateAnimation = this.animation;
  }


  public get normal(): boolean {
    return this.privateAnimation === Animation.Normal;
  }

  public get snake(): boolean {
    return this.privateAnimation === Animation.Snake;
  }

  public get breath(): boolean {
    return this.privateAnimation === Animation.Breath;
  }

  public get rainbow(): boolean {
    return this.privateAnimation === Animation.Rainbow;
  }

  public get off(): boolean {
    return this.privateAnimation === Animation.Off;
  }

  @Emit('animationUpdate')
  public changeTo(animation: Animation): Animation {
    this.privateAnimation = animation;
    return animation;
  }

  public changeToNormal() {
    this.changeTo(Animation.Normal);
  }

  public changeToBreath() {
    this.changeTo(Animation.Breath);
  }

  public changeToRainbow() {
    this.changeTo(Animation.Rainbow);
  }

  public changeToSnake() {
    this.changeTo(Animation.Snake);
  }

  public changeToOff() {
    this.changeTo(Animation.Off);
  }
}
</script>

<style scoped>
.off {
  border: 1px solid #000000;
  border-radius: 10px;
  background-color: #000000;
  color: #ffffff;
}
</style>
