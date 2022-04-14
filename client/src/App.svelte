<script lang="ts">
  import Navbar from "./lib/Navbar.svelte";
</script>

<main>
  <Navbar />
</main>

<style>
  :root {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }

  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }

  @media (max-width: 480px) {
    :root {
      font-size: 16px;
    }
  }

  @media (min-width: 480px) {
    :root {
      font-size: 28px;
    }
  }
</style>
