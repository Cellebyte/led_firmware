<template>
  <div>
    <b-badge variant="dark" class="huge">{{ getActivePalette }}</b-badge>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { namespace } from 'vuex-class';

const colourPalettes = namespace('ColourPalettes');

@Component
export default class PaletteCounter extends Vue {
    @colourPalettes.Getter
    public getActivePalette!: number;
}
</script>
<style scoped>
.huge {
  font-size: 2.5rem;
  size: 4rem;
}
</style>
