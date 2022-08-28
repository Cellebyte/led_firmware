import Vue from 'vue';
import { ColourPalette, ColourPalettes as APIColourPalettes, RGB } from '@/types/api';
import { ColourPaletteDict } from '@/types/store';
import iro from '@jaames/iro';
import {
  VuexModule, Module, Mutation, Action,
} from 'vuex-module-decorators';

@Module({ namespaced: true })
class ColourPalettes extends VuexModule {
    private activePalette: number = 1;

    private availableSlots: number = 0;

    private availablePalettes: Array<number> = [];

    private availablePalettesAmount: number = 0

    private colourPalettes: ColourPaletteDict = {}

    public get getActivePalette(): number {
      return this.activePalette;
    }

    public get getAvailableSlots(): number {
      return this.availableSlots;
    }

    public get getAvailablePalettes(): Array<number> {
      return this.availablePalettes;
    }

    public get getAvailablePalettesAmount(): number {
      return this.availablePalettesAmount;
    }

    public get getColourPalettes() : ColourPaletteDict {
      return this.colourPalettes;
    }

    public get colours() : Array<string> {
      return Object.values(
        this.getColourPalettes[this.activePalette],
      ).map(colour => new iro.Color(`rgb(${colour.red},${colour.green},${colour.blue})`).hexString);
    }

    public get colourIndices(): Array<string> {
      return Object.keys(
        this.getColourPalettes[this.activePalette],
      );
    }

    @Mutation
    SET_PALETTES(colourPalettes: APIColourPalettes): void {
      this.availableSlots = colourPalettes.slots;
      this.availablePalettes = colourPalettes.colour_palettes;
      this.availablePalettesAmount = colourPalettes.amount;
      colourPalettes.colour_palettes.forEach((colourPalette) => {
        Vue.set(this.colourPalettes, colourPalette, {} as ColourPalette);
      });
    }

    @Mutation
    SET_ACTIVE_PALETTE(id: number) {
      this.activePalette = id;
    }

    @Mutation
    SET_PALETTE(value: {id: number, colourPalette: ColourPalette}) {
      this.colourPalettes[value.id] = value.colourPalette;
    }

    @Mutation
    SET_PALETTE_COLOUR(value: { id: number, colourID: number, colour: RGB}) {
      this.colourPalettes[value.id][value.colourID] = value.colour;
    }

    @Mutation
    DEL_PALETTE_COLOUR(value: {id: number, colourID: number}) {
      this.colourPalettes[value.id][value.colourID] = {} as RGB;
    }

    @Mutation
    DEL_PALETTE(id: number) {
      this.colourPalettes[id] = {} as ColourPalette;
    }

    @Action({ rawError: true })
    public async FETCH_PALETTES() {
      const response = await this.context.rootState.api.palettes.getPalettes();
      if (response.data && response.status === 200) {
        this.context.commit('SET_PALETTES', response.data);
      }
    }

    @Action({ rawError: true })
    public async FETCH_PALETTE(paletteID: number) {
      console.log(paletteID);
      const response = await this.context.rootState.api.palettes.getPalette(paletteID);
      if (response.data && response.status === 200) {
        console.log(response.data);
        this.context.commit('SET_PALETTE', { id: paletteID, colourPalette: response.data });
        this.context.commit('SET_ACTIVE_PALETTE', paletteID);
        this.availablePalettes.forEach((colourPalette) => {
          if (colourPalette !== paletteID
            && this.availablePalettes[colourPalette]) {
            this.context.commit('DEL_PALETTE', colourPalette);
          }
        });
      }
    }

    @Action({ rawError: true })
    public async POST_PALETTE_COLOUR(
      value: {
      paletteID: number, colourID: number, formData: RGB},
    ) {
      console.log(value.colourID);
      const response = await this.context.rootState.api.palettes.postColour(
        value.paletteID, value.colourID, value.formData,
      );
      if (response.status === 201 && response.data) {
        this.context.commit('SET_PALETTE_COLOUR', { id: value.paletteID, colourID: value.colourID, colour: response.data });
      }
    }

    @Action({ rawError: true })
    public async ADD_PALETTE_COLOUR(
      value: {
      paletteID: number, formData: RGB},
    ) {
      const response = await this.context.rootState.api.palettes.postColours(
        value.paletteID, value.formData,
      );
      if (response.status === 201 && response.data) {
        this.context.commit('SET_PALETTE_COLOUR', {
          id: value.paletteID,
          colourID: Object.keys(response.data)[0],
          colour: Object.values(response.data)[0],
        });
      }
    }

    @Action({ rawError: true })
    public async DELETE_PALETTE_COLOUR(
      value: {
      paletteID: number, colourID: number},
    ) {
      const response = await this.context.rootState.api.palettes.deleteColour(
        value.paletteID, value.colourID,
      );
      if (response.status === 200) {
        this.context.commit('DEL_PALETTE_COLOUR', { id: value.paletteID, colourID: value.colourID });
      }
    }

    @Action({ rawError: true })
    public async DELETE_PALETTE(
      paletteID: number,
    ) {
      const response = await this.context.rootState.api.palettes.deleteColours(
        paletteID,
      );
      if (response.status === 200) {
        this.context.commit('DELETE_PALETTE', paletteID);
      }
    }
}
export default ColourPalettes;
