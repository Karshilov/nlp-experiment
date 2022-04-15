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
  const getContent = (node: HTMLElement) => {
    const listener = (e: InputEvent) => {
      if (e.inputType.startsWith("in") && e.inputType !== "insertParagraph") {
        isEmpty = false;
        if (e.isComposing) return;
        if (!Object.is(document.activeElement, node)) return;
        const selection = getSelection();
        const range = selection.getRangeAt(0);
        e.preventDefault();
        const text = e.data ? e.data : e.dataTransfer.getData("text/html");
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
