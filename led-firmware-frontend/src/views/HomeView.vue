<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/images/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
    <ColorPicker ref="picker" v-model="color" />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import ColorPicker from '@/components/ColorPicker.vue';

@Options({
  components: {
    HelloWorld,
    ColorPicker,
  },
})
export default class HomeView extends Vue {}
</script>
