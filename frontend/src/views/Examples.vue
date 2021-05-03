<template>
  <div class="examples">
    <h2>Inverse Visualization</h2>
    <p>
      We allow users to take an image of a visualization and turn it into the
      code that created it, thus allowing the user to edit an image
      visualization on the fly.
    </p>
    <p>
      <strong
        >MVP Warning: Only works with bar plots created using
        matplotlib.</strong
      >
    </p>
    <br />
    <p>
      Enter Image URL: &nbsp; <input v-model="url" type="text" />
      <button @click="$router.push({ name: 'Editor', query: { url: url } })">
        Derender
      </button>
    </p>
    <p>Here we provide a few example images that can be worked with,</p>
    <router-link
      :to="{
        name: 'Editor',
        query: { url: 'https://i.imgur.com/W1eZaSk.png' },
      }"
      ><img src="https://i.imgur.com/W1eZaSk.png" alt=""
    /></router-link>
    <router-link
      :to="{
        name: 'Editor',
        query: {
          url:
            'https://stackabuse.com/ezoimgfmt/stackabuse.s3.amazonaws.com/media/matplotlib-bar-plot-tutorial-and-examples-1.png?ezimgfmt=rs:640x480/rscb1/ng:webp/ngcb1',
        },
      }"
      ><img
        src="https://stackabuse.com/ezoimgfmt/stackabuse.s3.amazonaws.com/media/matplotlib-bar-plot-tutorial-and-examples-1.png?ezimgfmt=rs:640x480/rscb1/ng:webp/ngcb1"
        alt=""
    /></router-link>
  </div>
</template>
<script>
export default {
  name: "Examples",
  data() {
    return {
      url: "",
    };
  },
};
</script>
<style scoped>
.examples {
  padding-left: 2rem;
}

img:hover {
  border: 2px black solid;
  border-radius: 5px;
}

p {
  max-width: 40rem;
}
</style>