<template>
  <div class="editor">
    <div class="image-frame">
      <template v-if="!loading">
        <Bar
          v-for="bar in this.meta.layers.mark.entities"
          :key="JSON.stringify(bar.box)"
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
          :key="JSON.stringify(text.box)"
          :text="text"
          @aaa="
            text.text = $event;
            render();
          "
        ></TextE>
      </template>
      <img :src="this.currentImage" draggable="false" />
    </div>
  </div>
</template>
<script>
import Bar from "@/components/Bar";
import TextE from "@/components/TextE";

export default {
  name: "Editor",
  components: { Bar, TextE },
  data() {
    return {
      originalImageURL: "",
      originalImage: "",
      currentImage: "",
      meta: "",
      loading: true,
    };
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

img {
  user-select: none;
}
</style>