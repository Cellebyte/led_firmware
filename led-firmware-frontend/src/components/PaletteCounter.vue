<template>
  <div>
    <b-badge variant="dark" style="font-size: 1.5rem;">{{ getActivePalette }}</b-badge>
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
