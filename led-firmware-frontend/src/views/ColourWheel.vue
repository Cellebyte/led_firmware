<template>
  <div class="home">
    <!-- <img alt="Snake logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <!-- <device-color-picker/> -->
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <animation-selector />
      </b-row>
      <b-row class="row d-flex pt-1 justify-content-center">
        <b-button-group>
          <previous-palette-button />
          <new-colour-button />
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

@Component({
  components: {
    ColorPicker,
    NewColourButton,
    DeleteColourButton,
    AnimationSelector,
    NextPaletteButton,
    PreviousPaletteButton,
  },
})
export default class ColourWheel extends Vue { }
</script>
