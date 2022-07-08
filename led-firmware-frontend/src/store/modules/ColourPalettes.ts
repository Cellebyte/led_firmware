import Vue from 'vue';
import { ColourPalette, ColourPalettes, RGB } from '@/types/api';
import { ColourPaletteDict, ColourPaletteState, RootState } from '@/types/store';
import iro from '@jaames/iro';

export default {
  namespaced: true,

  state: {
    activePalette: 1,
    availableSlots: 0,
    availablePalettes: [],
    availablePalettesAmount: 0,
    colourPalettes: {} as ColourPaletteDict,
  },

  getters: {
    colourPalettes: (state: ColourPaletteState) => state.colourPalettes,
    colours: (state: ColourPaletteState) => Object.values(
      state.colourPalettes[state.activePalette],
    ).map(
      colour => new iro.Color(`rgb(${colour.red},${colour.green},${colour.blue})`).hexString,
    ),
    colourIndices: (state: ColourPaletteState) => Object.keys(
      state.colourPalettes[state.activePalette],
    ),
    availableSlots: (state: ColourPaletteState) => state.availableSlots,
    activePalette: (state: ColourPaletteState) => state.activePalette,
    availablePalettes: (state: ColourPaletteState) => state.availablePalettes,
    availablePalettesAmount: (state: ColourPaletteState) => state.availablePalettesAmount,
  },

  mutations: {
    SET_PALETTES(state: ColourPaletteState, colourPalettes: ColourPalettes) {
      Vue.set(state, 'availableSlots', colourPalettes.slots);
      Vue.set(state, 'availablePalettes', colourPalettes.colour_palettes);
      Vue.set(state, 'availablePalettesAmount', colourPalettes.amount);
      colourPalettes.colour_palettes.forEach((colourPalette) => {
        Vue.set(state.colourPalettes, colourPalette, {} as ColourPalette);
      });
    },
    SET_ACTIVE_PALETTE(state: ColourPaletteState, id: number) {
      Vue.set(state, 'activePalette', id);
    },
    SET_PALETTE(state: ColourPaletteState, payload: { id: number, colourPalette: ColourPalette }) {
      Vue.set(state.colourPalettes, payload.id, payload.colourPalette);
    },
    SET_PALETTE_COLOUR(state: ColourPaletteState, payload: {
      id: number, colourID: number, colour: RGB}) {
      Vue.set(state.colourPalettes[payload.id], payload.colourID, payload.colour);
    },
    DELETE_PALETTE_COLOUR(state: ColourPaletteState, payload: {id: number, colourID: number}) {
      Vue.delete(state.colourPalettes[payload.id], payload.colourID);
    },
    DELETE_PALETTE(state: ColourPaletteState, id: number) {
      Vue.set(state.colourPalettes, id, {} as ColourPalette);
    },
  } as any,

  actions: {
    async FETCH_PALETTES(context: { commit: any; rootState: RootState }) {
      const response = await context.rootState.api.palettes.getPalettes();
      if (response.data && response.status === 200) {
        context.commit('SET_PALETTES', response.data);
      }
    },

    async FETCH_PALETTE(
      context: {state: ColourPaletteState, commit: any; rootState: RootState},
      payload: { paletteID: number },
    ) {
      const response = await context.rootState.api.palettes.getPalette(payload.paletteID);
      if (response.data && response.status === 200) {
        console.log(response.data);
        context.commit('SET_PALETTE', { id: payload.paletteID, colourPalette: response.data });
        context.commit('SET_ACTIVE_PALETTE', payload.paletteID);
        context.state.availablePalettes.forEach((colourPalette) => {
          if (colourPalette !== payload.paletteID
            && context.state.colourPalettes[colourPalette]) {
            context.commit('DELETE_PALETTE', colourPalette);
          }
        });
      }
    },
    async SET_PALETTE_COLOUR(
      context: { commit: any; rootState: RootState },
      payload: { paletteID: number, colourID: number, formData: RGB },
    ) {
      const response = await context.rootState.api.palettes.postColour(
        payload.paletteID, payload.colourID, payload.formData,
      );
      if (response.status === 201 && response.data) {
        context.commit('SET_PALETTE_COLOUR', { id: payload.paletteID, colourID: payload.colourID, colour: response.data });
      }
    },
    async ADD_PALETTE_COLOUR(
      context: { commit: any, rootState: RootState },
      payload: {paletteID: number, formData: RGB },
    ) {
      const response = await context.rootState.api.palettes.postColours(
        payload.paletteID, payload.formData,
      );
      if (response.status === 201 && response.data) {
        context.commit('SET_PALETTE_COLOUR', {
          id: payload.paletteID,
          colourID: Object.keys(response.data)[0],
          colour: Object.values(response.data)[0],
        });
      }
    },
    async DELETE_PALETTE_COLOUR(
      context: { commit: any; rootState: RootState },
      payload: { paletteID: number, colourID: number },
    ) {
      const response = await context.rootState.api.palettes.deleteColour(
        payload.paletteID, payload.colourID,
      );
      if (response.status === 200) {
        context.commit('DELETE_PALETTE_COLOUR', { id: payload.paletteID, colourID: payload.colourID });
      }
    },
    async DELETE_PALETTE(
      context: { commit: any; rootState: RootState },
      payload: { paletteID: number, colourID: number },
    ) {
      const response = await context.rootState.api.palettes.deleteColours(
        payload.paletteID,
      );
      if (response.status === 200) {
        context.commit('DELETE_PALETTE', payload.paletteID);
      }
    },
  },
};
