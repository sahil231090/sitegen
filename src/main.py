import os
import sys
import shutil
from textnode import extract_title
from htmlnode import markdown_to_html_node

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = os.path.join(root_dir, 'static')
    dst = os.path.join(root_dir, 'docs')
    
    if not os.path.isdir(src):
        raise Exception(f"The dir doesn't exist {src}")
    if not os.path.isdir(dst):
        raise Exception(f"The dir doesn't exist {dst}")
    copy_directory(src, dst)
    

    generate_pages_recursive(dir_path_content=os.path.join(root_dir, 'content'), 
                  template_path=os.path.join(root_dir, 'template.html'), 
                  dest_dir_path=os.path.join(root_dir, 'docs'),
                  basepath=basepath)


def copy_directory(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Copying directory: {src_path} -> {dst_path}")
            copy_directory(src_path, dst_path)



# generate_page
def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)
    
# generate_pages_recursive
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path):
            if item.endswith(".md"):
                dst_path = dst_path.replace(".md", ".html")
                generate_page(src_path, template_path, dst_path, basepath)
        else:
            generate_pages_recursive(src_path, template_path, dst_path, basepath)


if __name__ == "__main__":
    main()


