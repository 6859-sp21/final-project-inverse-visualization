<template>
  <div class="series">
    <div
      class="color"
      :style="{ backgroundColor: colorCSS }"
      @click="pickeropen = true"
    ></div>
    <div class="name">{{ s.name }}</div>
    <Chrome
      class="picker"
      v-model="color"
      v-if="pickeropen"
      v-on-clickaway="() => (pickeropen = false)"
    ></Chrome>
  </div>
</template>
<script>
import { Chrome } from "vue-color";
import { mixin as clickaway } from "vue-clickaway2";

export default {
  name: "Series",
  props: ["s"],
  mixins: [clickaway],
  components: { Chrome },
  watch: {
    s() {
      const [r, g, b] = this.s.color;
      this.color = { r, g, b };
    },
    color() {
      const c = this.color.rgba;
      if (this.tt) {
        clearTimeout(this.tt);
      }

      this.tt = setTimeout(() => {
        this.$emit("colorchange", [c.r, c.g, c.b]);
      }, 1000);
    },
  },
  data() {
    return {
      pickeropen: false,
      color: { r: 255, g: 255, b: 255 },
      tt: undefined,
    };
  },
  computed: {
    colorCSS() {
      return `rgb(${this.s.color[0]}, ${this.s.color[1]}, ${this.s.color[2]})`;
    },
  },
  mounted() {
    const [r, g, b] = this.s.color;
    this.color = { r, g, b };
  },
};
</script>
<style scoped>
.color {
  width: 2rem;
  height: 2rem;
  border-radius: 5px;
  border: 1px rgb(0, 0, 0) solid;
  margin-right: 1rem;
  cursor: pointer;
}

.series {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  position: relative;
}

.picker {
  position: absolute;
  left: 20%;
  top: 50%;
  z-index: 99;
}
</style>