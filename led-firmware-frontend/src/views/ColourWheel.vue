<template>
  <div class="home">
    <!-- <img alt="Snake logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <!-- <device-color-picker/> -->
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <animation-selector :animation="getActiveAnimation" @animationUpdate="onAnimationsUpdate" />
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
import { mapActions, mapGetters } from 'vuex';

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
  computed: {
    ...mapGetters('Animations', {
      getActiveAnimation: 'activeAnimation',
    }),
  },
  created() {
    this.fetchAnimation().then(() => {
      console.log('Got animation Update');
    });
  },
  methods: {
    ...mapActions({
      updateAnimation: 'Animations/CHANGE_ANIMATION',
      fetchAnimation: 'Animations/FETCH_ANIMATION',
    }),
    onAnimationsUpdate(animation: Animation) {
      this.updateAnimation({
        animation,
      });
    },
  },
})
export default class ColourWheel extends Vue { }
</script>
