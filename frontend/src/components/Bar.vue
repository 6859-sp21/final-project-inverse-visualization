<template>
  <div class="bar" :style="pos">
    <div class="container">
      <div class="handle" @mousedown="mousedown"></div>
      <div class="colorbutton" @click="pickeropen = true">
        <font-awesome-icon icon="palette"></font-awesome-icon>
      </div>
      <div>
        <Chrome
          class="picker"
          v-model="color"
          v-if="pickeropen"
          v-on-clickaway="() => (pickeropen = false)"
        ></Chrome>
      </div>
    </div>
  </div>
</template>
<script>
import { Chrome } from "vue-color";
import { mixin as clickaway } from "vue-clickaway2";

export default {
  name: "Bar",
  mixins: [clickaway],
  components: { Chrome },
  props: {
    bar: {
      required: true,
      type: Object,
    },
  },
  watch: {
    bar() {
      const [r, g, b] = this.bar.color;
      this.color = { r, g, b };
    },
    color() {
      const c = this.color.rgba;
      //   console.log(c);
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
      md: false,
      mdy: 0,
      delta: 0,
      pickeropen: false,
      color: { r: 255, g: 255, b: 255 },
      tt: undefined,
    };
  },
  methods: {
    mousedown(e) {
      this.md = true;
      this.mdy = e.clientY;
      this.delta = 0;
    },
    mouseup() {
      if (!this.md) return;
      this.md = false;
      const [x1, y1, x2, y2] = this.bar.box;
      this.$emit("boxchange", [x1, y1 - this.delta, x2, y2]);
    },
    mousemove(e) {
      if (!this.md) return;
      this.delta = this.mdy - e.clientY;
    },
  },
  mounted() {
    document.addEventListener("mouseup", this.mouseup);
    document.addEventListener("mousemove", this.mousemove);

    const [r, g, b] = this.bar.color;
    this.color = { r, g, b };
  },
  destroyed() {
    document.removeEventListener("mousemove", this.mousemove);
  },
  computed: {
    pos() {
      const [x1, y1, x2, y2] = this.bar.box;

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
.bar {
  position: absolute;
  border-radius: 5px;
  transform: translate(-1.5px, -1.5px);
  cursor: pointer;
}

.bar:hover {
  border: 3px solid rgb(165, 165, 165);
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
}

.container {
  width: 100%;
  height: 100%;
  position: relative;
}

.handle {
  left: 50%;
  top: 0;
  width: 10px;
  height: 10px;
  border-radius: 100%;
  background: rgb(255, 255, 255);
  border: 1px grey solid;
  position: absolute;
  transform: translate(-50%, -50%);
  visibility: hidden;
  cursor: ns-resize;
}

.bar:hover .handle {
  visibility: inherit;
}

.bar:hover .colorbutton {
  visibility: inherit;
}

.colorbutton {
  visibility: hidden;
  color: grey;
  left: 50%;
  top: 50%;
  position: absolute;
  transform: translate(-50%, -50%);
}

.colorbutton:hover {
  color: rgb(85, 85, 85);
}

.picker {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 99;
}
</style>