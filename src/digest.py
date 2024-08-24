from htmlnode import *
from textnode import *
import re
import itertools
text_types = {"text": (None, None), "bold": ("b", "**"), "italic": ("i", "*"),
              "code": ("code", "`"), "link": ("a", None), "image": ("img", None)}
block_types = {"paragraph": "p", "code": "code", "quote": "blockquote", "unordered_list": "ul", "ordered_list": "ol", "header": "h"}


def text_node_to_html_node(text_node):
    type = text_node.text_type
    if type not in text_types:
        raise Exception(f"{type} is not a valid text type")
    if text_types[type][0] in [None, "b"]:
        return LeafNode(text_types[type][0], text_node.text)
    if text_types[type][0] == "a":
        return HTMLNode(text_types[type][0], text_node.text, None, {"href": text_node.url})
    if text_types[type][0] == "img":
        return HTMLNode(text_types[type][0], None, None, {"src": text_node.url, "alt": text_node.text})
    return HTMLNode(text_types[type][0], text_node.text)


def split_on_delim(old_nodes, delim, text_type):
    new_nodes = []
    if not delim:
        return old_nodes
    new_delim = "\\".join(list(map(lambda a: a, delim)))
    pat = fr"(?<!\{new_delim})\{new_delim}(?!\{new_delim})+"
    for node in old_nodes:
        delim_text = re.split(pat, node.text)
        if delim_text == node.text:
            new_nodes.append(node)
            continue
        for i in range(0, len(delim_text)):
            if not delim_text[i]:
                continue
            if i % 2 != 0:
                new_nodes.append(TextNode(delim_text[i], text_type, node.url))
            else:
                new_nodes.append(
                    TextNode(delim_text[i], node.text_type, node.url))

    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_text = extract_markdown_links(node.text)
        if not link_text:
            new_nodes.append(node)
            continue
        split_text = re.split(r"(?<!!)\[.*?\]\(.*?\)", node.text)
        for z in itertools.zip_longest(split_text, link_text):
            if z[0]:
                new_nodes.append(TextNode(z[0], node.text_type, node.url))
            if z[1]:
                new_nodes.append(TextNode(z[1][0], "link", z[1][1]))
    return new_nodes


def split_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_text = extract_markdown_images(node.text)
        if not image_text:
            new_nodes.append(node)
            continue
        split_text = re.split(r"!\[.*?\]\(.*?\)", node.text)
        for z in itertools.zip_longest(split_text, image_text):
            if z[0]:
                new_nodes.append(TextNode(z[0], node.text_type, node.url))
            if z[1]:
                new_nodes.append(TextNode(z[1][0], "image", z[1][1]))
    return new_nodes


def text_to_textnodes(text):
    start_node = TextNode(text, "text")
    nodes = split_image(split_links(split_on_delim(split_on_delim(split_on_delim([start_node], text_types["bold"][1], "bold"), text_types["italic"][1], "italic"), text_types["code"][1], "code")))
    return nodes


def markdown_block_split(text):
    lst = text.splitlines(True)
    blocks = [""]
    for s in lst:
        if s.isspace() and blocks[-1]:
            blocks[-1] = blocks[-1][:len(blocks[-1]) - 1].rstrip()
            blocks.append("")
        elif not s.isspace():
            blocks[-1] += s.rstrip() + "\n"
    if not blocks[-1]:
        blocks.pop()
    blocks[-1] = blocks[-1][:len(blocks[-1]) - 1]
    return blocks


def block_to_blocktype(block):
    if re.findall(r"(?<!#)#{1,6}(?= )", block):
        return "header"
    if re.match(r"(?s)(?m)(^```(.*?)```$)", block):
        return "code"
    if all(line.startswith(">") for line in block.splitlines()):
        return "quote"
    if all(line.startswith("* ") or line.startswith("- ") for line in block.splitlines()):
        return "unordered_list"
    lst = block.splitlines()
    if all(lst[i].startswith(f"{i+1}. ")for i in range(0, len(lst))):
        return "ordered_list"
    else:
        return "paragraph"
    pass


def MD_to_htmlnode(text):
    blocks = markdown_block_split(text)
    html_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == "unordered_list":
            split_text = block.splitlines()
            parent_html = ParentNode(block_types[block_type], list(map(lambda sub: ParentNode("li", sub), list(map(lambda a: list(map(lambda b: text_node_to_html_node(b), text_to_textnodes(a[2:]))), split_text)))))
        if block_type == "ordered_list":
            split_text = block.splitlines()
            parent_html = ParentNode(block_types[block_type], list(map(lambda sub: ParentNode("li", sub), list(map(lambda a: list(map(lambda b: text_node_to_html_node(b), text_to_textnodes(a.lstrip("1234567890")[2:]))), split_text)))))
        if block_type == "code":
            parent_html = ParentNode("pre", [ParentNode(block_types[block_type], [text_node_to_html_node(split_on_delim([TextNode(block, "text")], "```", "text")[0])])])
        if block_type == "quote":
            split_text = block.splitlines(True)
            parent_html = ParentNode(block_types[block_type], [text_node_to_html_node(TextNode("".join(list(map(lambda a: a[1:].lstrip(" "), split_text))), "text"))])
        if block_type == "header":
            head_num = len(re.findall("((?<!.)#{1,6})(?= )", block)[0])
            parent_html = ParentNode(f"{block_types[block_type]}{head_num}", [text_node_to_html_node(TextNode(block[head_num + 1:], "text"))])
        if block_type == "paragraph":
            parent_html = ParentNode(block_types[block_type], list(map(lambda a: text_node_to_html_node(a), text_to_textnodes(block))))
        html_nodes.append(parent_html)
    return ParentNode("div", html_nodes)
