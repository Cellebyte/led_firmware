import {
  Animation, Api, ColourPalette, PolyAnimation,
} from '@/types/api';
import { LedFirmwareFrontendConfiguration } from '@/types/config';

export interface RootState {
    version: string
    config: LedFirmwareFrontendConfiguration
    api: Api
}

export interface ColourPaletteDict {
    [id: number] : ColourPalette
}

export interface ColourPaletteState {
    activePalette: number,
    availableSlots: number,
    availablePalettes: Array<number>,
    availablePalettesAmount: number
    colourPalettes: ColourPaletteDict
}

export interface AnimationsState {
    currentAnimation: Animation | undefined,
    animationOptions: {[animation in Animation]: PolyAnimation},
}
