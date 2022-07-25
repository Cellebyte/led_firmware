<template>
  <div>
    <b-badge variant="dark" style="font-size: 1.5rem;">{{ getActivePalette }}</b-badge>
  </div>
</template>
<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';

export default Vue.extend({
  name: 'palette-counter',
  computed: {
    ...mapGetters('ColourPalettes', {
      getActivePalette: 'activePalette',
    }),
  },
});
</script>
