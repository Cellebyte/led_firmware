<template>
  <div>
    <b-button
      v-b-tooltip.hover.top title="Go to the next ColourPalette."
      size=md
      style="font-size: 2rem;"
      v-on:click="nextColourPalette"
    >
      <b-icon-arrow-right-short />
    </b-button>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const colourPalettes = namespace('ColourPalettes');

@Component
export default class NextPaletteButton extends Vue {
    @colourPalettes.Getter
    public getActivePalette!: number;

    @colourPalettes.Getter
    public getAvailablePalettes!: Array<number>;

    @colourPalettes.Action
    public FETCH_PALETTE!: (paletteID: number) => void ;

    public nextColourPalette(): any {
      console.log(this.getActivePalette);
      const currentPalette = this.getActivePalette;
      const currentIndex = this.getAvailablePalettes.indexOf(currentPalette);
      console.log(currentIndex);
      const newIndex = currentIndex + 1;
      if (newIndex < this.getAvailablePalettes.length) {
        this.FETCH_PALETTE(this.getAvailablePalettes[newIndex]);
      }
    }
}
</script>
