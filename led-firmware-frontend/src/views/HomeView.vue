<template>
  <b-container fluid>
      <b-row>
        <b-col class="d-flex justify-content-center">
          <ColorPicker ref="picker" v-model="color" />
        </b-col>
      </b-row>
      <b-row>
        <hline/>
      </b-row>
      <b-row>
        <b-col class="d-flex justify-content-center justify-content-end">
          <ColourPalette/>
        </b-col>
      </b-row>
  </b-container>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import ColorPicker from '@/components/ColorPicker.vue';
import ColourPalette from '@/components/ColourPalette.vue';

@Options({
  components: {
    ColorPicker,
    ColourPalette,
  },
})
export default class HomeView extends Vue {}
</script>
