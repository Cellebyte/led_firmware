<template>
  <div>
    <b-button
      v-b-tooltip.hover.top title="Add a colour to the ColourWheel"
      size=md
      style="font-size: 2rem;"
      v-on:click="addAdditionalColor"
    >
      <b-icon-plus/>
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
    public colourIndices!: Array<string>;

    @colourPalettes.Action
    public ADD_PALETTE_COLOUR!: (value: {paletteID: number, formData: RGB}) => Promise<void>;

    public addAdditionalColor() {
      console.log(this.colourIndices);
      if (!this.colourIndices.includes(this.getAvailableSlots.toString())) {
        this.ADD_PALETTE_COLOUR(
          { paletteID: this.getActivePalette, formData: { red: 255, green: 255, blue: 255 } },
        );
      }
    }
}
</script>
