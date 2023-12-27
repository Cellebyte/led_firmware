import { AnimationDirection } from './api';

export interface AnimationFormData {
  length: number,
  steps: number,
  dimPercentage: number,
  paletteSelector: number,
  selectedColours: Array<number>,
  direction: AnimationDirection,
  changeColour: Array<boolean>,
}

export interface PaletteFormOption {
  'v-html': any,
  html: string,
  value: number
}
