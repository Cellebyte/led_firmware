<template>
  <div>
    <b-button
      v-b-tooltip.hover.top title="Delete a colour from the ColourWheel"
      size=md
      style="font-size: 2rem;"
      v-on:click="deleteAdditionalColour"
    >
      <b-icon-dash/>
    </b-button>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import { RGB } from '@/types/api';

const colourPalettes = namespace('ColourPalettes');

@Component
export default class NewColourButton extends Vue {
    @colourPalettes.Getter
    public getActivePalette!: number;

    @colourPalettes.Getter
    public getAvailableSlots!: number;

    @colourPalettes.Getter
    public colours!: Array<string>;

    @colourPalettes.Getter
    public colourIndices!: Array<string>;

    @colourPalettes.Action
    public DELETE_PALETTE_COLOUR!: (value: {
      paletteID: number, colourID: number},
    ) => Promise<void>;

    deleteAdditionalColour() {
      if (this.colourIndices[this.colours.length - 1]) {
        this.DELETE_PALETTE_COLOUR(
          {
            paletteID: this.getActivePalette,
            colourID: parseInt(this.colourIndices[this.colours.length - 1], 10),
          },
        );
      }
    }
}
</script>
