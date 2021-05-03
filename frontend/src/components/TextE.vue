<template>
  <div class="text" :style="pos" @click="editing = true" v-on-clickaway="aaway">
    <input type="text" v-model="t" v-if="editing" @keypress.enter="aaway" />
  </div>
</template>
<script>
import { mixin as clickaway } from "vue-clickaway2";

export default {
  name: "TextE",
  mixins: [clickaway],
  props: {
    text: {
      required: true,
      type: Object,
    },
  },
  watch: {},
  data() {
    return {
      editing: false,
      t: "",
    };
  },
  methods: {
    aaway() {
      if (!this.editing) return;
      this.editing = false;
      this.$emit("aaa", this.t);
    },
  },
  mounted() {
    this.t = this.text.text;
  },
  destroyed() {},
  computed: {
    pos() {
      const [x1, y1, x2, y2] = this.text.box;

      if (!this.md) {
        return {
          left: `${x1}px`,
          top: `${y1}px`,
          width: `${x2 - x1}px`,
          height: `${y2 - y1}px`,
        };
      }
      return {
        left: `${x1}px`,
        top: `${y1 - this.delta}px`,
        width: `${x2 - x1}px`,
        height: `${y2 - y1 + this.delta}px`,
      };
    },
  },
};
</script>
<style lang="scss" scoped>
.text {
  position: absolute;
  border-radius: 5px;
  transform: translate(-0.1rem, -0.1rem);
  cursor: pointer;
  padding: 0.2rem;
}

.text:hover {
  border: 3px solid rgb(165, 165, 165);
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}

.container {
  width: 100%;
  height: 100%;
  position: relative;
}

input {
  width: 100%;
  height: 100%;
  padding: 0.2rem;
  transform: translate(-0.3rem, -0.3rem);
}
</style>