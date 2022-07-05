<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/> -->
    <!-- <device-color-picker/> -->
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <color-picker/>
      </b-row>
      <b-row class="row d-flex justify-content-center">
        <new-colour-button/>
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ColorPicker from '@/components/ColorPicker.vue';
import NewColourButton from '@/components/NewColourButton.vue';

@Component({
  components: {
    ColorPicker,
    NewColourButton,
  },
})
export default class HomeView extends Vue {}
</script>
