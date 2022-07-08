<template>
  <div>
    <b-button
      v-b-tooltip.hover.bottom title="Delete a colour from the ColourWheel"
      size="lg"
      v-on:click="deleteAdditionalColour"
    >
      <b-icon-dash-lg/>
    </b-button>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex';


export default {
  name: 'delete-colour-button',
  computed: {
    ...mapGetters('ColourPalettes', {
      getActivePalette: 'activePalette',
      colours: 'colours',
      colourIndices: 'colourIndices',
    }),
  },
  methods: {
    ...mapActions({
      deletePaletteColour: 'ColourPalettes/DELETE_PALETTE_COLOUR',
    }),
    deleteAdditionalColour() {
      if (this.colourIndices[this.colours.length - 1]) {
        this.deletePaletteColour(
          {
            paletteID: this.getActivePalette,
            colourID: this.colourIndices[this.colours.length - 1],
          },
        );
      }
    },
  },
};
</script>
