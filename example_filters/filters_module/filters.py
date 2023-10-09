from six import binary_type, text_type


def stringify(node, encoding: str):
    if isinstance(node, binary_type):
        return node.decode(encoding)
    elif hasattr(node, "__repl__"):
        return str(node)
    elif hasattr(node, "__str__"):
        return str(node)


def concat(nodes: list, encoding='utf-8'):

    txt_nodes = [t for t in nodes if isinstance(t, text_type)]
    nontxt_nodes = [n for n in nodes if n not in txt_nodes]
    for n in nontxt_nodes:
        new_node = stringify(n, encoding)
        if new_node:
            txt_nodes.append(new_node)
    output = " ".join(txt_nodes)
    return output




