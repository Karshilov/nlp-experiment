<script lang="ts">
  import { Select, SelectItem } from "carbon-components-svelte";
  let modelType: string = "all";
</script>

<nav>
  <h1>GPT网文续写</h1>
  <p>NLP实践作业</p>
  <div class="divid" />
  <div class="pc-only">
    <Select bind:value={modelType} style="flex-grow: 0;">
      <SelectItem value="all" text="未筛选网文" />
      <SelectItem value="yq" text="女频言情小说" />
    </Select>
  </div>
</nav>

<style lang="scss">
  nav {
    padding-left: 12rem;
    padding-right: 12rem;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    h1 {
      color: #ff3e00;
      text-transform: uppercase;
      font-size: 1.5rem;
      font-weight: 100;
      line-height: 1.1;
      margin: auto 2rem;
      max-width: 14rem;
    }

    p {
      max-width: 14rem;
      margin: auto 1rem;
      line-height: 1.35;
    }

    @media (max-width: 480px) {
      padding-left: 1rem;
      padding-right: 1rem;
      h1 {
        margin: auto 0.5rem;
        max-width: none;
      }

      p {
        margin: auto 0.5rem;
        max-width: none;
      }
    }
  }

  .divid {
    flex-grow: 1;
  }

  @media (max-width: 480px) {
    nav > .pc-only {
      display: none;
    }
  }
</style>
