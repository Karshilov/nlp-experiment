<script lang="ts">
  import Navbar from "./lib/Navbar.svelte";
  import Content from "./lib/Content.svelte";
</script>

<main>
  <Navbar />
  <Content />
</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }

  main {
    margin: 0 auto;
  }
</style>
