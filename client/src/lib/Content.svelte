<script context="module" lang="ts">
  //span，另外行内元素还包括img、a、big、small、sub、sup、strong、u、button
  const inlineNames = [
    "img",
    "a",
    "big",
    "small",
    "sub",
    "sup",
    "strong",
    "u",
    "button",
  ];
</script>

<script lang="ts">
  import axios from "axios";
  import { getContext } from "svelte";
  import type { Writable } from "svelte/store";
  import pen from "../assets/pen.svg";
  import RangeSelection from "./RangeSelection";
  let modelType: Writable<string> = getContext("type");
  let content = "";
  let isEmpty = true;
  let isLoading = false;
  const getContent = (node: HTMLElement) => {
    const listener = (e: InputEvent) => {
      if (e.inputType.startsWith("in") && e.inputType !== "insertParagraph") {
        isEmpty = false;
        if (e.isComposing) return;
        if (!Object.is(document.activeElement, node)) return;
        const selection = getSelection();
        const range = selection.getRangeAt(0);
        e.preventDefault();
        const text = e.data ? e.data : e.dataTransfer.getData("text/plain");
        let newText = text.split(/<[^<>]*>/).join("");
        const targetNode = selection.focusNode;
        const previousText = targetNode.textContent;
        let { startContainer, endContainer, startOffset, endOffset } = range;
        let rangeType = 0;
        let newNode = document.createTextNode(newText);
        if (range.collapsed) {
          targetNode.textContent =
            previousText.slice(0, startOffset) +
            newText +
            previousText.slice(startOffset);
        } else if (range.startContainer.isSameNode(range.endContainer)) {
          targetNode.textContent =
            previousText.slice(0, startOffset) +
            newText +
            previousText.slice(endOffset);
        } else {
          const lca = range.commonAncestorContainer;
          let fg = 0;
          const removeList = [];
          for (const child of lca.childNodes) {
            if (fg === 2) continue;
            if (child.contains(startContainer)) {
              fg = 1;
              RangeSelection(startContainer, startOffset, child, true);
              startContainer = child;
              continue;
            } else if (child.contains(endContainer)) {
              fg = 2;
              RangeSelection(endContainer, endOffset, child, true);
              lca.insertBefore(newNode, child);
              endContainer = child;
            }
            if (fg === 1) {
              removeList.push(child);
            }
            if (!fg) {
              continue;
            }
          }
          removeList.forEach((child) => lca.removeChild(child));
          if (
            inlineNames.includes(startContainer.nodeName.toLowerCase()) &&
            !inlineNames.includes(endContainer.nodeName.toLowerCase())
          ) {
            lca.replaceChild(
              document.createTextNode(endContainer.textContent),
              endContainer
            );
          } else if (
            !inlineNames.includes(startContainer.nodeName.toLowerCase()) &&
            inlineNames.includes(endContainer.nodeName.toLowerCase())
          ) {
            lca.replaceChild(
              document.createTextNode(startContainer.textContent),
              startContainer
            );
          }
          rangeType = 1;
        }
        const newRange = document.createRange();
        newRange.collapse(true);
        if (!rangeType) {
          if (startContainer.nodeName !== "#text") {
            newRange.setStart(
              startContainer.lastChild,
              startContainer.lastChild.textContent.length
            );
          } else {
            newRange.setStart(startContainer, startOffset + newText.length);
          }
        } else {
          newRange.setStartAfter(newNode);
        }
        selection.removeAllRanges();
        selection.addRange(newRange);
        content = node.innerHTML.split(/<[^<>]*>/).join("");
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
    isLoading = true;
    const prefixes = content.split(/。！？/).filter((i) => i.trim() !== "");
    let prefix = "，";
    prefixes.reverse().forEach((value) => {
      if (prefix.length < 200) prefix = value + prefix;
      else return;
    });
    document.querySelector(".editor").innerHTML = document
      .querySelector(".editor")
      .innerHTML.replace(/<strong[^<>]*>/, "");
    const res = await axios.post("http://127.0.0.1:8000/generate", {
      prefix,
      model_type: $modelType === "yq",
    });
    const strong = document.createElement("strong");
    strong.textContent = res.data.result
      .slice(prefix.length)
      .split(/ /)
      .join("");
    document.querySelector(".editor").appendChild(strong);
    content = document.querySelector(".editor").innerHTML.split(/<[^<>]*>/).join("");
    isLoading = false;
  };
</script>

<div class="container">
  <div class="placeholder" hidden={!isEmpty}>请输入一段文本作为开头</div>
  <div class="editor" contenteditable use:getContent />
</div>
{#if !isLoading}
  <img src={pen} alt="" on:click={getGeneratedText} />
{:else}
  <div class="lds-roller">
    <div />
    <div />
    <div />
    <div />
    <div />
    <div />
    <div />
    <div />
  </div>
{/if}

<style lang="scss">
  img {
    position: fixed;
    right: 4rem;
    bottom: 8rem;
    width: 3rem;
    cursor: pointer;
    @media (max-width: 480px) {
      bottom: 2rem;
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
  .lds-roller {
    display: inline-block;
    position: fixed;
    width: 3rem;
    height: 3rem;
    right: 4rem;
    bottom: 8rem;
    cursor: pointer;
    @media (max-width: 480px) {
      bottom: 2rem;
      right: 2rem;
    }
  }
  .lds-roller div {
    animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    transform-origin: 50% 50%;
  }
  .lds-roller div:after {
    content: " ";
    display: block;
    position: absolute;
    width: 0.2625rem;
    height: 0.2625rem;
    border-radius: 50%;
    background: rgb(233, 74, 21);
    margin: -0.15rem 0 0 -0.15rem;
  }
  .lds-roller div:nth-child(1) {
    animation-delay: -0.036s;
  }
  .lds-roller div:nth-child(1):after {
    top: 2.3625rem;
    left: 2.3625rem;
  }
  .lds-roller div:nth-child(2) {
    animation-delay: -0.072s;
  }
  .lds-roller div:nth-child(2):after {
    top: 2.55rem;
    left: 2.1rem;
  }
  .lds-roller div:nth-child(3) {
    animation-delay: -0.108s;
  }
  .lds-roller div:nth-child(3):after {
    top: 2.6625rem;
    left: 1.8rem;
  }
  .lds-roller div:nth-child(4) {
    animation-delay: -0.144s;
  }
  .lds-roller div:nth-child(4):after {
    top: 2.7rem;
    left: 1.5rem;
  }
  .lds-roller div:nth-child(5) {
    animation-delay: -0.18s;
  }
  .lds-roller div:nth-child(5):after {
    top: 2.6625rem;
    left: 1.2rem;
  }
  .lds-roller div:nth-child(6) {
    animation-delay: -0.216s;
  }
  .lds-roller div:nth-child(6):after {
    top: 2.55rem;
    left: 0.9rem;
  }
  .lds-roller div:nth-child(7) {
    animation-delay: -0.252s;
  }
  .lds-roller div:nth-child(7):after {
    top: 2.3625rem;
    left: 0.6375rem;
  }
  .lds-roller div:nth-child(8) {
    animation-delay: -0.288s;
  }
  .lds-roller div:nth-child(8):after {
    top: 2.1rem;
    left: 0.45rem;
  }
  @keyframes lds-roller {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
