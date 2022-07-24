<template>
  <div ref="picker">
    <!-- <label style="font-size: large;">
      <div class="box" :style="{'background-color':hexColour}"></div> {{ currentColour.hexString }}
    </label> -->
  </div>
</template>

<script lang="js">
import iro from '@jaames/iro';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'color-picker',
  props: {
    width: {
      type: Number,
      default: 360,
    },
    height: {
      type: Number,
      default: 360,
    },
    handleSvg: {
      type: String,
      default: null,
    },
    handleOrigin: {
      type: Object,
      default() {
        return {
          x: 0,
          y: 0,
        };
      },
    },
    padding: {
      type: Number,
      default: 6,
    },
    handleRadius: {
      type: Number,
      default: 24,
    },
    sliderMargin: {
      type: Number,
      default: 32,
    },
    sliderHeight: {
      type: Number,
      default: undefined,
    },
    borderWidth: {
      type: Number,
      default: 0,
    },
    borderColor: {
      type: String,
      default: '#ffffff',
    },
    display: {
      type: String,
      default: 'block',
    },
    layout: {
      type: String,
      default: 'block',
    },
    wheelAngle: {
      type: Number,
      default: 0,
    },
    wheelDirection: {
      type: String,
      default: 'anticlockwise',
    },
    wheelLightness: {
      type: Boolean,
      default: true,
    },
  },
  data() {
    return {
      colorPicker: null,
      currentColour: '',
    };
  },
  created() {
    this.fetchPalettes().then(() => {
      this.fetchPalette({ paletteID: this.getActivePalette }).then(() => {
        console.log('Init done');
      });
    });
  },
  computed: {
    ...mapGetters('ColourPalettes', {
      getColours: 'colours',
      getActivePalette: 'activePalette',
    }),
    hexColour() {
      if (this.currentColour) {
        return this.currentColour.hexString;
      }

      return '';
    },
  },
  methods: {
    ...mapActions({
      updatePaletteColour: 'ColourPalettes/SET_PALETTE_COLOUR',
      fetchPalettes: 'ColourPalettes/FETCH_PALETTES',
      fetchPalette: 'ColourPalettes/FETCH_PALETTE',
    }),
    onInput(color) {
      this.$emit('input', color.hexString);
    },
    onColorChange(color, changes) {
      this.currentColour = color;
      this.$emit('color:change', {
        color,
        changes,
      });
    },
    onColorInit(color, changes) {
      this.currentColour = color;
      this.$emit('color:init', {
        color,
        changes,
      });
    },
    onInputChange(color, changes) {
      this.$emit('input:change', {
        color,
        changes,
      });
    },
    onInputStart(color) {
      this.$emit('input:start', {
        color,
      });
    },
    onInputMove(color) {
      this.$emit('input:move', {
        color,
      });
    },
    onInputEnd(color) {
      this.updatePaletteColour(
        {
          paletteID: this.getActivePalette,
          colourID: color.index + 1,
          formData: { red: color.red, green: color.green, blue: color.blue },
        },
      );
      console.log(color.index, color.hexString);
      this.$emit('input:end', {
        color,
      });
    },
    onMount(colorPicker) {
      this.$emit('mount', {
        colorPicker,
      });
    },
  },
  mounted() {
    this.colorPicker = iro.ColorPicker(this.$refs.picker, {
      width: this.width,
      height: this.height,
      handleSvg: this.handleSvg,
      colors: this.getColours,
      padding: this.padding,
      layout: this.layout,
      display: this.display,
      css: this.css,
      wheelDirection: this.wheelDirection,
      wheelAngle: this.wheelAngle,
      wheelLightness: this.wheelLightness,
      handleOrigin: this.handleOrigin,
      handleRadius: this.handleRadius,
      sliderMargin: this.sliderMargin,
      sliderHeight: this.sliderHeight,
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
  },
  beforeUnmount() {
    this.colorPicker.off('input:end', this.onInput);
    this.colorPicker.off('color:change', this.onColorChange);
    this.colorPicker.off('color:init', this.onColorInit);
    this.colorPicker.off('input:change', this.onInputChange);
    this.colorPicker.off('input:start', this.onInputStart);
    this.colorPicker.off('input:move', this.onInputMove);
    this.colorPicker.off('input:end', this.onInputEnd);
    this.colorPicker.off('mount', this.onMount);
  },
  watch: {
    getColours(newColours) {
      if (!newColours.length === 0 || !this.colorPicker) {
        return;
      }
      if (this.colorPicker.colors && newColours) {
        if (
          this.colorPicker.colors.length === newColours.length
        || this.colorPicker.colors.length < newColours.length
        ) {
          let alreadySaved = 0;
          this.colorPicker.colors.forEach((colour, index) => {
            this.colorPicker.colors[index].hexString = newColours[index];
            alreadySaved = index;
          });
          newColours.forEach((colour, index) => {
            if (index > alreadySaved) {
              this.colorPicker.addColor(newColours[index], index);
              this.colorPicker.setActiveColor(index);
            }
          });
        } else if (this.colorPicker.colors.length > newColours.length) {
          let alreadySaved = 0;
          newColours.forEach((colour, index) => {
            this.colorPicker.colors[index].hexString = colour;
            alreadySaved = index;
          });
          this.colorPicker.colors.forEach((colour, index) => {
            if (index > alreadySaved) {
              this.colorPicker.removeColor(index);
            }
          });
        }
        // this.colorPicker.forceUpdate();
      }
    },
  },
};
</script>
<style scoped>
.box {
  padding: 32px;
  height: 32px;
  width: 32px;
  clear: both;
}
</style>
