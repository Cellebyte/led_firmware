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
