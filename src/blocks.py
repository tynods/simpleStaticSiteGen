import re
from enum import Enum

from textnode import *
from htmlnode import *
from inline import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    

def markdown_to_blocks(markdown):
    return [l.strip() for l in markdown.split("\n\n")]


def block_to_block_type(block):
    if re.match(r"^#{1,6} \w+", block) :
        return BlockType.HEADING
    elif re.match(r"^```.*```", block, re.MULTILINE | re.DOTALL):
        return BlockType.CODE
    elif all(map(lambda x: x.startswith(">"), block.split("\n"))):
        return BlockType.QUOTE
    elif all(map(lambda x: x.startswith("- "), block.split("\n"))):
        return BlockType.UNORDERED_LIST
    
    if all(map(lambda x: re.match(r"^\d+\. ", x), block.split("\n"))) :
        nums = list(map(int, re.findall(r"\n(\d+)\. .*", "\n"+block, flags=re.MULTILINE)))
        ok = True
        for i in range(len(nums)):
            if nums[i]!=i+1:
                ok = False
                break
        if ok:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                nodes.append(ParentNode("pre",[LeafNode("code", re.match(r"```\n(.*)```",block,flags=re.MULTILINE|re.DOTALL).group(1))]))
            case BlockType.PARAGRAPH:
                sub_nodes = text_to_textnodes(block.replace("\n", " ").strip(" \n"))
                if len(sub_nodes)>0:
                    nodes.append(ParentNode("p", list(map(text_node_to_html_node,sub_nodes))))
            case BlockType.HEADING:
                m = re.match(r"(#{1,6}) +(.*)", block)
                nodes.append(LeafNode("h"+str(len(m.group(1))), m.group(2)))
            case BlockType.QUOTE:
                sub_nodes = []
                for line in block.split("\n"):
                    sub_nodes.extend(text_to_textnodes(line[2:]))    
                if len(sub_nodes)>0:
                    nodes.append(ParentNode("blockquote", list(map(text_node_to_html_node,sub_nodes))))
            case BlockType.UNORDERED_LIST:
                html_lines = []
                for line in block.split("\n"):
                    html_lines.append(ParentNode("li", list(map(text_node_to_html_node,text_to_textnodes(line[2:])))))
                nodes.append(ParentNode("ul", html_lines))
            case BlockType.ORDERED_LIST:
                html_lines = []
                for line in block.split("\n"):
                    html_lines.append(ParentNode("li", list(map(text_node_to_html_node,text_to_textnodes(re.match(r"\d+\. (.*)",line).group(1))))))
                nodes.append(ParentNode("ol", html_lines))

    return ParentNode("div", nodes)