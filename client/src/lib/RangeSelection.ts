export default function RangeSelection(target: Node, offset: number, container: Node, flag: boolean) {
    if (flag) {
        let fg = 0;
        if (target.isEqualNode(container)) {
            target.textContent = target.textContent.slice(0, offset);
            return;
        }
        for (const child of container.childNodes) {
            if (fg) container.removeChild(child);
            if (child.contains(target)) {
                fg = 1;
                if (child.isEqualNode(target)) {
                    child.textContent = child.textContent.slice(0, offset);
                    console.log(child)
                }
                else RangeSelection(target, offset, child, flag);
            }
            if (!fg) continue;
        }
    } else {
        let fg = 0;
        if (target.isEqualNode(container)) {
            target.textContent = target.textContent.slice(offset);
            return;
        }
        for (const child of container.childNodes) {
            if (fg) continue;
            if (child.contains(target)) {
                fg = 1;
                if (child.isEqualNode(target)) {
                    child.textContent = child.textContent.slice(offset);
                }
                else RangeSelection(target, offset, child, flag);
            }
            if (!fg) container.removeChild(child);
        }
    }
}