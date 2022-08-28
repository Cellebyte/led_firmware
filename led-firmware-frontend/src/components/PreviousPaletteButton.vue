<template>
  <div>
    <b-button
      v-b-tooltip.hover.top title="Go to the previous ColourPalette."
      size=md
      style="font-size: 2rem;"
      v-on:click="previousColourPalette"
    >
      <b-icon-arrow-left-short />
    </b-button>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const colourPalettes = namespace('ColourPalettes');

@Component
export default class PreviousPaletteButton extends Vue {
    @colourPalettes.Getter
    public getActivePalette!: number;

    @colourPalettes.Getter
    public getAvailablePalettes!: Array<number>;

    @colourPalettes.Action
    public FETCH_PALETTE!: (paletteID: number) => void ;

    public previousColourPalette(): any {
      console.log(this.getActivePalette);
      const currentPalette = this.getActivePalette;
      const currentIndex = this.getAvailablePalettes.indexOf(currentPalette);
      console.log(currentIndex);
      const newIndex = currentIndex - 1;
      if (newIndex >= 0) {
        this.FETCH_PALETTE(this.getAvailablePalettes[newIndex]);
      }
    }
}
</script>
