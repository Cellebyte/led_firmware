<template>
  <div>
    <b-button v-on:click="addAdditionalColor">
      <b-icon-plus-circle-dotted/>
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
    }),
  },
  methods: {
    ...mapActions({
      addPaletteColour: 'ColourPalettes/ADD_PALETTE_COLOUR',
    }),
    addAdditionalColor() {
      this.addPaletteColour(
        { paletteID: this.getActivePalette, formData: { red: 255, green: 255, blue: 255 } },
      );
    },
  },
};
</script>
