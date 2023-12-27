<template>
  <div class="box" :style="{'background-color':hexColour}"></div>
</template>
<script lang="ts">
import {
  Component, Prop, Vue,
} from 'vue-property-decorator';
import { RGB } from '@/types/api';
import iro from '@jaames/iro';

@Component({
  name: 'colour-box',
})
export default class ColourBox extends Vue {
  @Prop({ default: { red: 255, green: 255, blue: 255 } }) readonly colour!: RGB;

  public hexColour(): string {
    if (this.colour) {
      return new iro.Color(`rgb(${this.colour.red},${this.colour.green},${this.colour.blue})`).hexString;
    }
    return '';
  }
}
</script>
<style scoped>
.box {
  padding: 8px;
  height: 8px;
  width: 8px;
  clear: both;
}
</style>
