<template>
  <div class="home">
    <!-- <img alt="Snake logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <!-- <device-color-picker/> -->
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <animation-selector :animation="getActiveAnimation" @animationUpdate="animationUpdate" />
      </b-row>
      <b-row class="row d-flex pt-1 justify-content-center">
        <b-button-group>
          <previous-palette-button />
          <new-colour-button />
          <palette-counter />
          <delete-colour-button />
          <next-palette-button />
        </b-button-group>
      </b-row>
      <b-row class="row d-flex justify-content-center">
        <color-picker />
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ColorPicker from '@/components/ColorPicker.vue';
import NewColourButton from '@/components/NewColourButton.vue';
import DeleteColourButton from '@/components/DeleteColourButton.vue';
import AnimationSelector from '@/components/AnimationSelector.vue';
import NextPaletteButton from '@/components/NextPaletteButton.vue';
import PreviousPaletteButton from '@/components/PreviousPaletteButton.vue';
import PaletteCounter from '@/components/PaletteCounter.vue';
import { namespace } from 'vuex-class';

const animations = namespace('Animations');
@Component({
  components: {
    ColorPicker,
    NewColourButton,
    DeleteColourButton,
    AnimationSelector,
    NextPaletteButton,
    PreviousPaletteButton,
    PaletteCounter,
  },
})
export default class ColourWheel extends Vue {
  created() {
    this.FETCH_ANIMATION().then(() => {
      console.log('Got animation Update');
    });
  }

  @animations.Getter
  public getActiveAnimation!: Animation | undefined;

  @animations.Action
  public CHANGE_ANIMATION!: (animation: Animation) => void;

  @animations.Action
  public FETCH_ANIMATION!: () => any;

  public animationUpdate(animation: Animation) {
    this.CHANGE_ANIMATION(animation);
  }
}
</script>
