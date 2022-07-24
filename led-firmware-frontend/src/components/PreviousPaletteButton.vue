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
<script>
import { mapActions, mapGetters } from 'vuex';


export default {
  name: 'previous-palette-button',
  computed: {
    ...mapGetters('ColourPalettes', {
      getActivePalette: 'activePalette',
      getAvailablePalettes: 'availablePalettes',
    }),
  },
  methods: {
    ...mapActions({
      setActivePalette: 'ColourPalettes/FETCH_PALETTE',
    }),
    previousColourPalette() {
      const currentPallete = this.getActivePalette;
      const currentIndex = this.getAvailablePalettes.indexOf(currentPallete);
      const newIndex = currentIndex - 1;
      if (newIndex >= 0) {
        this.setActivePalette({ paletteID: this.getAvailablePalettes[newIndex] });
      }
    },
  },
};
</script>
