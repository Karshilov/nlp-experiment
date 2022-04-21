export default function RangeSelection(
  target: Node,
  offset: number,
  container: Node,
  flag: boolean
) {
  if (flag) {
    let fg = 0, removeList = [];
    if (target.isSameNode(container)) {
      target.textContent = target.textContent.slice(0, offset);
      return;
    }
    for (const child of container.childNodes) {
      if (fg) removeList.push(child);
      if (child.contains(target)) {
        fg = 1;
        if (child.isSameNode(target)) {
          child.textContent = child.textContent.slice(0, offset);
        } else RangeSelection(target, offset, child, flag);
      }
      if (!fg) continue;
    }
    removeList.forEach(child => container.removeChild(child))
  } else {
    let fg = 0, removeList = [];
    if (target.isSameNode(container)) {
      target.textContent = target.textContent.slice(offset);
      return;
    }
    for (const child of container.childNodes) {
      if (fg) continue;
      if (child.contains(target)) {
        fg = 1;
        if (child.isSameNode(target)) {
          child.textContent = child.textContent.slice(offset);
        } else RangeSelection(target, offset, child, flag);
      }
      if (!fg) removeList.push(child);
    }
    removeList.forEach(child => container.removeChild(child))
  }
}
