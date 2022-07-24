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
<script>
import { mapActions, mapGetters } from 'vuex';


export default {
  name: 'new-colour-button',
  computed: {
    ...mapGetters('ColourPalettes', {
      getActivePalette: 'activePalette',
      getAvailableSlots: 'availableSlots',
      colourIndices: 'colourIndices',
    }),
  },
  methods: {
    ...mapActions({
      addPaletteColour: 'ColourPalettes/ADD_PALETTE_COLOUR',
    }),
    addAdditionalColor() {
      console.log(this.colourIndices);
      if (!this.colourIndices.includes(this.getAvailableSlots)) {
        this.addPaletteColour(
          { paletteID: this.getActivePalette, formData: { red: 255, green: 255, blue: 255 } },
        );
      }
    },
  },
};
</script>
