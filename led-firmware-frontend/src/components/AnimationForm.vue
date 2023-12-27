<template>
  <div>
    <b-form
      @submit="onSubmit"
      @reset="onReset"
      v-if="show"
    >
      <b-form-group
        id="input-group-6"
        label-for="input-6"
        v-show="!rainbow"
        :description="animation + ' colour pallete.'"
      >
        <colour-box v-for="colour in getColours" :key="colour" :colour="colour"/>
        <b-form-select
          id="input-6"
          v-model="form.paletteSelector"
          :options="getAvailablePalettes"
          required
        ></b-form-select>
      </b-form-group>
      <b-form-group
        id="input-group-7"
        v-show="rainbow"
        label-for="input-7"
        :description="'The ' + animation + ' period'"
        >
        <b-form-input
          id="input-7"
          v-model="form.period"
          type="number"
          :placeholder="'Enter ' + animation + ' period.'"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-1"
        v-show="snake"
        label-for="input-1"
        :description="'The ' + animation + ' length'"
      >
        <b-form-input
          id="input-1"
          v-model="form.length"
          type="number"
          :placeholder="'Enter ' + animation + ' length.'"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-5"
        v-show="breath"
        label-for="input-5"
        :description="'The ' + animation + ' dim_percentage'"
      >
        <b-form-input
          id="input-5"
          v-model="form.dimPercentage"
          type="number"
          min="0.005"
          max="1"
          step="0.005"
          :placeholder="'Enter ' + animation + ' dim_percentage.'"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        v-show="snake"
        label-for="input-2"
        :description="'The ' + animation + ' step count'"
      >
        <b-form-input
          id="input-2"
          v-model="form.steps"
          type="number"
          :placeholder="'Enter the ' + animation + ' step count.'"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-3"
        label-for="input-3"
        :description="animation + ' direction of travel'"
        v-show="snake"
      >
        <b-form-select
          id="input-3"
          v-model="form.direction"
          :options="directions"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group
        id="input-group-4"
        :description="'change ' + animation +' colour?'"
        v-show="!rainbow"
        v-slot="{ ariaDescribedby }"
      >
        <b-form-checkbox-group
          v-model="form.changeColour"
          id="checkboxes-4"
          :aria-describedby="ariaDescribedby"
        >
          <b-form-checkbox size="lg" value="true"></b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>

      <b-button
        type="submit"
        variant="primary"
      >Submit</b-button>
      <b-button
        type="reset"
        variant="danger"
      >Reset</b-button>
    </b-form>
    <b-card
      class="mt-3"
      header="Form Data Result"
    >
      <pre class="m-0">{{ form }}</pre>
    </b-card>
  </div>
</template>

<script lang="ts">
import {
  Component, Prop, Vue, Emit,
} from 'vue-property-decorator';
import { namespace } from 'vuex-class';
import { Animation, AnimationDirection, RGB } from '@/types/api';
import { AnimationFormData, PaletteFormOption } from '@/types/components';
import ColourBox from '@/components/ColourBox.vue';
import { ColourPaletteDict } from '@/types/store';

const colourPalettes = namespace('ColourPalettes');

@Component({
  name: 'animation-form',
  components: {
    ColourBox,
  },
})
export default class AnimationForm extends Vue {
  @Prop({ default: Animation.Normal }) readonly animation!: string;

  private show: boolean = true;

  private form: AnimationFormData = {
    length: 30,
    steps: 1,
    dimPercentage: 0.0,
    paletteSelector: 0,
    selectedColours: [],
    direction: AnimationDirection.Up,
    changeColour: [],
  } as AnimationFormData

  @colourPalettes.Getter
  public getAvailablePalettes!: Array<number>;

  @colourPalettes.Getter
  public getColourPalettes!: ColourPaletteDict;

  public getColours(): RGB[] {
    if (this.form.paletteSelector !== 0) {
      const data = Object.values(this.getColourPalettes[this.form.paletteSelector]);
      alert(JSON.stringify(data));
      return data;
    }
    return [];
  }

  // created() {
  // this.fetchPalettes().then(() => {
  //   this.fetchPalette({ paletteID: this.getActivePalette }).then(() => {
  //     console.log('Init done');
  //   });
  // });
  // },
  // eslint-disable-next-line class-methods-use-this
  public get directions() {
    return [AnimationDirection.Up, AnimationDirection.Down];
  }

  public get snake() {
    return this.animation === Animation.Snake;
  }

  public get breath() {
    return this.animation === Animation.Breath;
  }

  public get rainbow() {
    return this.animation === Animation.Rainbow;
  }

  public onSubmit(event: any) {
    event.preventDefault();
    alert(JSON.stringify(this.form));
  }

  public onReset(event: any) {
    event.preventDefault();
    // Reset our form values
    // Trick to reset/clear native browser form validation state
    this.show = false;
    this.$nextTick(() => {
      this.show = true;
    });
  }
}
</script>
