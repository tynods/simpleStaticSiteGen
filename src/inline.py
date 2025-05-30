import re

from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type!=TextType.TEXT or node.text is None or node.text=="":
            new_nodes.append(node)
            continue

        type_toggle = False
        split = node.text.split(delimiter)
        if len(split)%2==0:
            raise Exception("invalid markup (closing missing)")
        for chunk in split:
            new_nodes.append(TextNode(chunk, 
                                      text_type if type_toggle else node.text_type,
                                      node.url))
            type_toggle = not type_toggle

    return new_nodes


def extract_markdown_images(text):
    # images
    #rx = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text):
    # regular links
    #rx = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.strip()=="":
            continue

        links = extract_markdown_links(node.text)
        if len(links)==0:
            new_nodes.append(node)
            continue
        nodeLink = TextNode(links[0][0], TextType.LINK, links[0][1])
        split = node.text.split(f"[{links[0][0]}]({links[0][1]})", maxsplit=1)
        new_nodes.append(TextNode(split[0], TextType.TEXT))
        new_nodes.append(nodeLink)
        new_nodes.extend(split_nodes_link([TextNode(split[1], TextType.TEXT)]))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.strip()=="":
            continue

        imgs = extract_markdown_images(node.text)
        if len(imgs)==0:
            new_nodes.append(node)
            continue
        nodeImage = TextNode(imgs[0][0], TextType.IMAGE, imgs[0][1])
        split = node.text.split(f"![{imgs[0][0]}]({imgs[0][1]})", maxsplit=1)
        new_nodes.append(TextNode(split[0], TextType.TEXT))
        new_nodes.append(nodeImage)
        new_nodes.extend(split_nodes_image([TextNode(split[1], TextType.TEXT)]))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes