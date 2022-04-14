<script lang="ts">
  import Navbar from "./lib/Navbar.svelte";
  import Content from "./lib/Content.svelte";
  import { setContext } from "svelte";
  import { writable } from "svelte/store";
  let modelType = writable("all");
  setContext("type", modelType);
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
