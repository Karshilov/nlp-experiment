<script lang="ts">
  let content = "";
  let isEmpty = true;
  const getContent = (node: HTMLElement) => {
    const listener = (e: InputEvent) => {
      if (e.inputType.startsWith("in") && e.inputType !== 'insertParagraph') {
        const text = e.data ? e.data : e.dataTransfer.getData("text/html");
        e.preventDefault();
        const newText = text.split(/<[^<>]*>/).join("");
        content += newText;
        const targetElement = node.children.length === 0 ? node : node.children[node.children.length - 1];
        targetElement.textContent += newText;
        const selection = getSelection();
        const range = selection.getRangeAt(0);
        range.collapse(true);
        range.setStartAfter(node.childNodes[node.childNodes.length - 1]);
        selection.removeAllRanges();
        selection.addRange(range);
      }
      if (content) isEmpty = false;
      else isEmpty = true;
    };
    const inputListener = (_e: InputEvent) => {
      content = node.innerHTML.split(/<[^<>]*>/).join("");
    }
    node.addEventListener("beforeinput", listener);
    node.addEventListener("input", inputListener);
    return {
      destroy: () => {
        node.removeEventListener("beforeinput", listener);
        node.removeEventListener("input", inputListener);
      },
    };
  };
</script>

<div class="container">
  <div class="placeholder" hidden={!isEmpty}>请输入一段文本作为开头</div>
  <div class="editor" contenteditable use:getContent></div>
</div>

<style lang="scss">
  .container {
    width: calc(100% - 28rem);
    margin-left: 14rem;
    margin-right: 14rem;
    padding-top: 2rem;
    margin-top: 8rem;
    position: relative;
    font-size: 1.2rem;
    .editor {
      min-height: 400px;
      left: 0.25rem;
      top: 0.25rem;
      right: 0.25rem;
      border: 0px;
      outline: none;
      position: absolute;
    }
    .placeholder {
      left: 0.25rem;
      top: 0.25rem;
      position: absolute;
      color: #b3afa9;
    }
    @media (max-width: 480px) {
      margin-top: 4rem;
      font-size: 1.1rem;
      width: calc(100% - 3rem);
      margin-left: 1.5rem;
      margin-right: 1.5rem;
    }
  }
</style>
