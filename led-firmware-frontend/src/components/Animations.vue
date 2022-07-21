<template>
  <div class="animation">
    <b-container>
      <b-row class="row d-flex justify-content-center">
        <snake-animation-form/>
      </b-row>
    </b-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import SnakeAnimationForm from '@/components/SnakeAnimationForm.vue';

@Component({
  components: {
    SnakeAnimationForm,
  },
})
export default class AnimationsVue extends Vue {}
</script>
