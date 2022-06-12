<template>
  <div>
    <div class="mt-2" :style="style">Value: {{ color }}</div>
    <b-form-input type="color" v-model="color"></b-form-input>
  </div>
</template>

<script>
export default {
  data() {
    return {
      color: '#ff0000',
    };
  },
  computed: {
    style() {
      return `background-color: ${this.color};`;
    },
  },
};
</script>
