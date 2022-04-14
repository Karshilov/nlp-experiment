<script lang="ts">
  let modelType: string = "all";
</script>

<nav>
  <h1>GPT网文续写</h1>
  <p>NLP实践作业</p>
  <div class="divid" />
  <select bind:value={modelType}>
    <option value="all">未筛选网文</option>
    <option value="yq">女频言情小说</option>
  </select>
</nav>

<style lang="scss">
  nav {
    width: 100%;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
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
      font-size: 1rem;
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
    @media (min-width: 480px) {
      h1 {
        max-width: none;
      }

      p {
        max-width: none;
      }
    }
  }

  .divid {
    flex-grow: 1;
  }
</style>
