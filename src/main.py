import sys
import os
import shutil
import re

from textnode import *
from htmlnode import *

from blocks import *

def copy_to(dfrom, dto):
    for elem in os.listdir(dfrom):
        p_elem = os.path.join(dfrom, elem)
        if os.path.isfile(p_elem):
            print("copy: "+p_elem)
            shutil.copy(p_elem, dto)
        else :
            p_dto_elem = os.path.join(dto, elem)
            os.mkdir(p_dto_elem)
            copy_to(p_elem, p_dto_elem)


def extract_title(markdown):
    m = re.search(r"^# +(.*)", markdown, flags=re.MULTILINE)
    if m is None:
        raise Exception("no title found")
    return m.group(1).strip()


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    from_content = f.read()
    f.close()
    template = open(template_path).read()
    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    f_out = open(dest_path, "w")
    f_out.write(template)
    f_out.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for elem in os.listdir(dir_path_content):
        p_elem = os.path.join(dir_path_content, elem)
        if os.path.isfile(p_elem):
            generate_page(p_elem, template_path, os.path.join(dest_dir_path, elem.split(".")[0]+".html"), basepath)
        else :
            p_dto_elem = os.path.join(dest_dir_path, elem)
            generate_pages_recursive(p_elem, template_path, p_dto_elem, basepath)


def clean_docs():
    for elem in os.listdir("docs"):
        p_elem = os.path.join("docs", elem)
        if os.path.isfile(p_elem):
            os.remove(p_elem)
        else:
            shutil.rmtree(p_elem)



def main(basepath="/"):
    clean_docs()
    copy_to("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__=="__main__" :
    basepath = "/"
    if len(sys.argv)>1:
        basepath = sys.argv[1]
    main(basepath)
