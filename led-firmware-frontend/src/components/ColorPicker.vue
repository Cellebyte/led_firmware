<template>
  <div ref="picker">
  </div>
</template>

<script lang="ts">
import iro from '@jaames/iro';

import {
  Component, Prop, Vue, Emit, Watch,
} from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import { RGB } from '@/types/api';

const colourPalettes = namespace('ColourPalettes');

@Component({
  name: 'color-picker',
})
export default class ColorPicker extends Vue {
  @Prop({ default: 360 }) readonly width!: number;

  @Prop({ default: 360 }) readonly height!: number;

  @Prop({ default: undefined }) readonly handleSvg!: string | undefined;

  @Prop({ default: () => ({ x: 0, y: 0 }) }) readonly handleOrigin!: object;

  @Prop({ default: 6 }) readonly padding!: number;

  @Prop({ default: 24 }) readonly handleRadius!: number;

  @Prop({ default: 32 }) readonly sliderMargin!: number;

  @Prop({ default: 0 }) readonly borderWidth!: number;

  @Prop({ default: '#ffffff' }) readonly borderColor!: string;

  @Prop({ default: 'block' }) readonly display!: string;

  @Prop({ default: 'block' }) readonly layout!: string;

  @Prop({ default: 0 }) readonly wheelAngle!: number;

  @Prop({ default: 'anticlockwise' }) readonly wheelDirection!: '' | 'clockwise' | 'anticlockwise' | undefined;

  @Prop({ default: true }) readonly wheelLightness!: boolean;

  private colorPicker: iro.ColorPicker| null = null;

  public currentColour: iro.Color | null = null;

  @colourPalettes.Getter
  public getActivePalette!: number;

  @colourPalettes.Getter
  public colours!: Array<string>;

  @colourPalettes.Action
  public FETCH_PALETTES!: () => Promise<void>;

  @colourPalettes.Action
  public FETCH_PALETTE!: (paletteID: number) => Promise<void>;

  @colourPalettes.Action
  public POST_PALETTE_COLOUR!: (
    value: {
      paletteID: number,
      colourID: number,
      formData: RGB
    }
  ) => Promise<void>;

  created() {
    this.FETCH_PALETTES().then(() => {
      this.FETCH_PALETTE(this.getActivePalette).then(() => {
        console.log('Init done');
      });
    });
  }

  @Emit('input')
  public onInput(color: iro.Color) {
    this.currentColour = color;
    return color.hexString;
  }

  @Emit('color:change')
  public onColorChange(color: iro.Color, changes: any) {
    this.currentColour = color;
    return {
      color,
      changes,
    };
  }

  @Emit('color:init')
  public onColorInit(color: iro.Color, changes: any) {
    this.currentColour = color;
    return {
      color,
      changes,
    };
  }

  @Emit('input:change')
  public onInputChange(color: iro.Color, changes: any) {
    this.currentColour = color;
    return {
      color,
      changes,
    };
  }

  @Emit('input:start')
  public onInputStart(color: iro.Color) {
    this.currentColour = color;
    return color;
  }

  @Emit('input:move')
  public onInputMove(color: iro.Color) {
    this.currentColour = color;
    return color;
  }

  @Emit('input:end')
  public onInputEnd(color: iro.Color) {
    const colourID = color.index + 1;
    this.POST_PALETTE_COLOUR({
      paletteID: this.getActivePalette,
      colourID,
      formData: { red: color.red, green: color.green, blue: color.blue } as RGB,
    });
    console.log(color.index, color.hexString);
    return color;
  }

  @Emit('mount')
  onMount(colorPicker: iro.ColorPicker) {
    this.colorPicker = colorPicker;
    return colorPicker;
  }

  beforeUnmount() {
    if (this.colorPicker) {
      this.colorPicker.off('input:end', this.onInput);
      this.colorPicker.off('color:change', this.onColorChange);
      this.colorPicker.off('color:init', this.onColorInit);
      this.colorPicker.off('input:change', this.onInputChange);
      this.colorPicker.off('input:start', this.onInputStart);
      this.colorPicker.off('input:move', this.onInputMove);
      this.colorPicker.off('input:end', this.onInputEnd);
      this.colorPicker.off('mount', this.onMount);
    }
  }

  @Watch('colours', { immediate: true, deep: true })
  getColours(newColours: Array<iro.Color>) {
    if ((newColours.length === 0) || !this.colorPicker) {
      return;
    }
    if (this.colorPicker.colors && newColours) {
      if (
        this.colorPicker.colors.length === newColours.length
      || this.colorPicker.colors.length < newColours.length
      ) {
        let alreadySaved = 0;
        this.colorPicker.colors.forEach((_, index) => {
          if (this.colorPicker) {
            this.colorPicker.colors[index].set(newColours[index]);
          }
          alreadySaved = index;
        });
        newColours.forEach((_, index) => {
          if (index > alreadySaved) {
            if (this.colorPicker) {
              this.colorPicker.addColor(newColours[index], index);
              this.colorPicker.setActiveColor(index);
            }
          }
        });
      } else if (this.colorPicker.colors.length > newColours.length) {
        let alreadySaved = 0;
        newColours.forEach((colour, index) => {
          if (this.colorPicker) {
            this.colorPicker.colors[index].set(colour);
          }
          alreadySaved = index;
        });
        this.colorPicker.setActiveColor(alreadySaved);
        this.colorPicker.colors.forEach((_, index) => {
          if (index > alreadySaved) {
            const deleteIndex = index;
            if (this.colorPicker) {
              this.colorPicker.removeColor(deleteIndex);
            }
          }
        });
      }
      this.colorPicker.forceUpdate();
    }
  }

  mounted() {
    this.colorPicker = iro.ColorPicker(this.$refs.picker as unknown as HTMLElement, {
      width: this.width,
      height: this.height,
      handleSvg: this.handleSvg,
      padding: this.padding,
      layout: this.layout as any,
      display: this.display,
      wheelDirection: this.wheelDirection,
      wheelAngle: this.wheelAngle,
      wheelLightness: this.wheelLightness,
      handleRadius: this.handleRadius,
      sliderMargin: this.sliderMargin,
      borderWidth: this.borderWidth,
      borderColor: this.borderColor,
    });
    this.colorPicker.on('input:end', this.onInput);
    this.colorPicker.on('color:change', this.onColorChange);
    this.colorPicker.on('color:init', this.onColorInit);
    this.colorPicker.on('input:change', this.onInputChange);
    this.colorPicker.on('input:start', this.onInputStart);
    this.colorPicker.on('input:move', this.onInputMove);
    this.colorPicker.on('input:end', this.onInputEnd);
    this.colorPicker.on('mount', this.onMount);
  }
}
</script>
