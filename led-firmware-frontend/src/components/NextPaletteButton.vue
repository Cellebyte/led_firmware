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
<script>
import { mapActions, mapGetters } from 'vuex';


export default {
  name: 'next-palette-button',
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
    nextColourPalette() {
      const currentPallete = this.getActivePalette;
      const currentIndex = this.getAvailablePalettes.indexOf(currentPallete);
      const newIndex = currentIndex + 1;
      if (newIndex < this.getAvailablePalettes.length) {
        this.setActivePalette({ paletteID: this.getAvailablePalettes[newIndex] });
      }
    },
  },
};
</script>
