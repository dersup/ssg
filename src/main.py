from digest import MD_to_htmlnode
import os
import shutil
import re


def copy_path(start, target):
    if not os.path.exists(start):
        raise ValueError("source dos'nt exist")
    if not os.path.exists(target):
        os.mkdir(target, 0o700)
    target_lst = os.listdir(target)
    if len(target_lst) > 0:
        shutil.rmtree(target)
        os.mkdir(target, 0o700)
    path_lst = os.listdir(start)
    if len(path_lst) == 0:
        return None
    current_path = start
    for add_path in path_lst:
        if not current_path.endswith("/"):
            current_path += "/"
        if os.path.isfile(current_path + add_path):
            shutil.copy(current_path + add_path, target)
        elif os.path.isdir(current_path + add_path):
            os.mkdir(target + add_path + "/", 0o700)
            copy_path(current_path + add_path, target + add_path)


def extract_title(MD):
    MD_lst = MD.splitlines()
    if all(not re.match(r"(?<!#)#{1}(?= )", MD_lst[i]) for i in range(0, len(MD_lst))):
        raise Exception("no header")
    for i in range(0, len(MD_lst)):
        if re.match(r"(?<!#)#{1}(?= )", MD_lst[i]):
            return MD_lst[i].lstrip("# ").rstrip(" ")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise ValueError("source not found")
    if not os.path.exists(template_path):
        raise ValueError("template not found")
    if not from_path.endswith(".md"):
        raise Exception("not a Markdown document")
    MD_file = open(from_path, "r")
    html_file = open(template_path, "r")
    final_file = html_file.read()
    MD = MD_file.read()
    final_file = final_file.replace("{{ Title }}", extract_title(MD))
    MD_html = MD_to_htmlnode(MD).to_html()
    final_file = final_file.replace("{{ Content }}", MD_html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), 0o700)
    f = open(dest_path, "w")
    f.write(final_file)
    html_file.close()
    MD_file.close()
    f.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise ValueError("content path dos'nt exist")
    if not os.path.exists(template_path):
        raise ValueError("template dos'nt exist")
    cont_lst = os.listdir(dir_path_content)
    if len(cont_lst) == 0:
        return None
    for cont in cont_lst:
        if not dest_dir_path.endswith("/"):
            dest_dir_path += "/"
        if not dir_path_content.endswith("/"):
            dir_path_content += "/"
        dest = dest_dir_path + cont
        current = dir_path_content + cont
        if os.path.isdir(current):
            os.mkdir(dest)
            generate_pages_recursive(current, template_path, dest)
        elif cont.endswith(".md"):
            print(cont)
            generate_page(current, template_path, dest.replace(".md",".html"))
        else:
            shutil.copy(current, dest_dir_path)


copy_path("static/", "public/")
generate_pages_recursive("content/", "template.html", "public/")
