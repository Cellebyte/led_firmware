<template>
  <div class="animation">
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <color-picker/>
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';


@Component({
  components: {
    // ColorPicker,
    // NewColourButton,
    // DeleteColourButton,
  },
})
export default class AnimationsVue extends Vue {}
</script>
