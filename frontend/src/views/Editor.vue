<template>
  <div class="editor">
    <h2 class="h">Inverse Viz Editor</h2>
    <router-link to="/"
      ><button class="h">Try Another Image</button></router-link
    >
    <p class="h" v-if="loading">Loading ...</p>
    <div class="editor-bar">
      <div class="image-frame" v-if="!loading">
        <template v-if="!loading">
          <Bar
            v-for="bar in this.bars"
            :key="bar.id"
            :bar="bar"
            @boxchange="
              bar.box = $event;
              render();
            "
            @colorchange="
              bar.color = $event;
              render();
            "
          ></Bar>
          <TextE
            v-for="text in this.meta.layers.text.entities"
            :key="text.id"
            :text="text"
            @aaa="
              text.text = $event;
              render();
            "
          ></TextE>
        </template>
        <img :src="this.currentImage" draggable="false" />
      </div>
      <div class="sidebar">
        <Series
          :s="s"
          v-for="s in series"
          :key="s.id"
          @colorchange="seriesColor(s, $event)"
        ></Series>
      </div>
    </div>
    <div class="code-bar" v-if="!loading">
      <b>Decompiled Code:</b> <br />
      <div class="code">
        <pre>{{ code }}</pre>
      </div>
    </div>
  </div>
</template>
<script>
import Bar from "@/components/Bar";
import TextE from "@/components/TextE";
import Series from "@/components/Series";

export default {
  name: "Editor",
  components: { Bar, TextE, Series },
  data() {
    return {
      originalImageURL: "",
      originalImage: "",
      currentImage: "",
      meta: "",
      loading: true,
    };
  },
  computed: {
    bars() {
      return this.meta.layers.mark.entities.filter((x) => x["type"] === "bar");
    },
    points() {
      return this.meta.layers.mark.entities.filter(
        (x) => x["type"] === "point"
      );
    },
    code() {
      return JSON.stringify(this.meta, null, 2);
    },
    series() {
      if (this.meta.layers === undefined) return [];
      const e = this.meta.layers.mark.entities;
      const colors = e
        .map((x) => JSON.stringify(x.color))
        .filter((x) => x !== "[255, 255, 255]")
        .filter((v, i, s) => s.indexOf(v) === i);
      const series = colors
        .map((color) => e.filter((x) => JSON.stringify(x.color) === color))
        .map((x, i) => ({
          id: i,
          name: `Series ${i + 1}`,
          color: x[0].color,
          entities: x,
        }));
      return series;
    },
  },
  methods: {
    derender() {
      this.$http
        .post("/api/decompile", { image: this.currentImage })
        .then((r) => {
          this.meta = r.data;
          this.render();
        });
    },
    render() {
      this.$http.post("/api/compile", { meta: this.meta }).then((r) => {
        this.currentImage = r.data;
        this.loading = false;
      });
    },
    seriesColor(s, color) {
      const entities = this.meta.layers.mark.entities.filter(
        (x) => JSON.stringify(x.color) === JSON.stringify(s.color)
      );
      for (let e of entities) {
        e.color = color;
      }
      this.render();
    },
  },
  mounted() {
    this.loading = true;
    this.originalImageURL = this.$route.query.url;
    this.$http.post("/api/image", { url: this.originalImageURL }).then((r) => {
      this.originalImage = r.data;
      this.currentImage = this.originalImage;
      this.derender();
    });
  },
};
</script>
<style lang="scss" scoped>
.image-frame {
  position: relative;
}

.h {
  margin-left: 2rem;
}

img {
  user-select: none;
}

.editor-bar {
  display: flex;
}

.code-bar {
  margin-left: 2rem;
}

.editor-bar {
  min-height: 30rem;
}

.code {
  max-height: 20rem;
  width: 30rem;
  overflow-y: scroll;
  background: rgb(238, 238, 238);
  user-select: text;
}
</style>