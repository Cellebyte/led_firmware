<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
    <device-color-picker/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import DeviceColorPicker from '@/components/DeviceColorPicker.vue';

@Component({
  components: {
    HelloWorld,
    DeviceColorPicker,
  },
})
export default class HomeView extends Vue {}
</script>
