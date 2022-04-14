<script lang="ts">
  import axios from "axios";
  import { getContext } from "svelte";
  import type { Writable } from "svelte/store";
  import pen from "../assets/pen.svg";
  let modelType: Writable<string> = getContext("type");
  let content = "";
  let isEmpty = true;
  const getContent = (node: HTMLElement) => {
    const listener = (e: InputEvent) => {
      if (e.inputType.startsWith("in") && e.inputType !== "insertParagraph") {
        isEmpty = false;
        if (e.isComposing) return;
        const selection = getSelection();
        e.preventDefault();
        const text = e.data ? e.data : e.dataTransfer.getData("text/html");
        const newText = text.split(/<[^<>]*>/).join("");
        content += newText;
        const targetElement =
          node.children.length === 0
            ? node
            : node.children[node.children.length - 1];
        targetElement.textContent += newText;
        const range = selection.getRangeAt(0);
        range.collapse(true);
        range.setStartAfter(node.childNodes[node.childNodes.length - 1]);
        selection.removeAllRanges();
        selection.addRange(range);
      }
    };
    const inputListener = (_e: InputEvent) => {
      content = node.innerHTML.split(/<[^<>]*>/).join("");
      if (content) isEmpty = false;
      else isEmpty = true;
    };
    node.addEventListener("beforeinput", listener);
    node.addEventListener("input", inputListener);
    return {
      destroy: () => {
        node.removeEventListener("beforeinput", listener);
        node.removeEventListener("input", inputListener);
      },
    };
  };

  const getGeneratedText = async () => {
    const prefixes = content.split(/。！？/).filter((i) => i.trim() !== "");
    let prefix = '，';
    prefixes.reverse().forEach(value => {
      if (prefix.length < 200) prefix = value + prefix;
      else return;
    })
    document.querySelector(".editor").innerHTML = document.querySelector(".editor").innerHTML.replace(/<strong[^<>]*>/, '')
    const res = await axios.post("http://127.0.0.1:8000/generate", {
      prefix,
      model_type: $modelType === "yq",
    });
    const strong = document.createElement("strong");
    strong.textContent = res.data.result.slice(prefix.length).split(/ /).join('');
    document.querySelector(".editor").appendChild(strong);
  };
</script>

<div class="container">
  <div class="placeholder" hidden={!isEmpty}>请输入一段文本作为开头</div>
  <div class="editor" contenteditable use:getContent />
</div>
<img src={pen} alt="" on:click={getGeneratedText} />

<style lang="scss">
  img {
    position: fixed;
    right: 4rem;
    bottom: 8rem;
    width: 3rem;
    cursor: pointer;
    @media (max-width: 480px) {
      bottom: 2rem;
      width: 2rem;
      right: 2rem;
    }
  }
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
      font-size: 1.2rem;
      line-height: 1.75;
      text-align: justify;
      @media (max-width: 480px) {
        font-size: 1.1rem;
      }
    }
    .placeholder {
      left: 0.25rem;
      top: 0.25rem;
      position: absolute;
      color: #b3afa9;
      line-height: 1.75;
      text-align: justify;
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
