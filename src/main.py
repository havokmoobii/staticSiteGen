import os, shutil, sys
from markdown_to_html import markdown_to_html_node, extract_title
from htmlnode import ParentNode

STATIC_PATH = "./static"
PUBLIC_PATH = "./docs"
CONTENT_PATH = "./content"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    log = ""
    log = rm_public(log)
    if not os.path.exists(STATIC_PATH):
        raise Exception(f"FATAL: {STATIC_PATH} not found.")
    else:
        os.mkdir(PUBLIC_PATH)
        log = log + f"Created {PUBLIC_PATH}\n"
        log = copy_static_to_public(STATIC_PATH, PUBLIC_PATH, log)

    log = generate_pages_recursive(CONTENT_PATH, "./template.html", PUBLIC_PATH, log, basepath)

    with open("main_log.txt", "w") as f:
        f.write(log)

def rm_public(log):
    if os.path.exists(PUBLIC_PATH):
        shutil.rmtree(PUBLIC_PATH)
        log = log + f"Removed {PUBLIC_PATH}\n"
    return log

def copy_static_to_public(path, dest, log):
    log = log + f"Files found in {path}: {os.listdir(path)}\n"
    current_level_files = os.listdir(path)
    for file in current_level_files:    
        if not os.path.isfile(f"{path}/{file}"):
            os.mkdir(f"{dest}/{file}")
            log = log + f"Copied {path}/{file} to {dest}/{file}\n"
            log = copy_static_to_public(f"{path}/{file}", f"{dest}/{file}", log)
        else:
            shutil.copy(f"{path}/{file}", f"{dest}/{file}")
            log = log + f"Copied {path}/{file} to {dest}/{file}\n"
    return log

def generate_page(dir_path_content, template_path, dest_dir_path, log, basepath):
    log = log + f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}\n"

    md = ""
    if not os.path.exists(dir_path_content):
        raise Exception("Specified source file does not exist")
    with open(dir_path_content, "r") as f:
        md = f.read()
        log = log + f"Read contents of {dir_path_content}\n"
    template = ""
    if not os.path.exists(template_path):
        raise Exception("Specified template file does not exist")
    with open(template_path, "r") as f:
        template = f.read()
        log = log + f"Read contents of {template_path}\n"
    content = markdown_to_html_node(md).to_html()
    log = log + "Markdown converted to HTML\n"
    title = extract_title(md)
    log = log + "Title extracted\n"
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    with open(dest_dir_path, "w") as f:
        f.write(template)
        log = log + f"{dest_dir_path} file created\n"

    return log

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, log, basepath):
    current_level_files = os.listdir(dir_path_content)
    for file in current_level_files:
        if not os.path.isfile(f"{dir_path_content}/{file}"):
            os.mkdir(f"{dest_dir_path}/{file}")
            log = log + f"Created new directory at {dest_dir_path}/{file}\n"
            log = generate_pages_recursive(f"{dir_path_content}/{file}", template_path, f"{dest_dir_path}/{file}", log, basepath)
        else:
            log = generate_page(f"{dir_path_content}/{file}", template_path, f"{dest_dir_path}/index.html", log, basepath)
            
    return log

main()