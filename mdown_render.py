import click
import os
import re
from shutil import rmtree


def close_section(root_path, chapter, section_cnt, section_title, section_content, force, t_o_c):
    file_name = "{:02d}".format(section_cnt) + "-" + format_name(section_title) + '.md'
    file_path = os.path.join(root_path, chapter, file_name)
    rel_path = os.path.join(".", chapter, file_name)
    link = create_link(remove_hashtags(section_title), rel_path)
    t_o_c.append("  * " + link)
    if not force and os.path.exists(file_path):
        if not click.confirm('The file {} already exists and will be overwritten, do you want to continue?'.format(file_path)):
            return
    if section_content:
        with open(file_path, 'w') as new_f:
            new_f.write(section_content.strip())


def create_link(text, target):
    return f"[{text}]({target})"


def generate_table_of_contents(path, T_O_C):
    text = "\n".join(T_O_C)
    file_path = os.path.join(path, 'Table_Of_Contents.md')
    with open(file_path, 'w') as new_f:
        new_f.write(text)


def remove_hashtags(name):
    # Remove all # and the first space at the beginning
    return re.sub(r'^#* ', '', name).strip()


def format_name(name):
    name = remove_hashtags(name)
    # Substitute the space char with _
    name = name.replace(' ', '_')
    # Remove all non-word characters
    return re.sub(r'\W+', '', name)


@click.command()
@click.argument("source", required=True, type=click.Path(exists=True))
@click.option("--targer_folder", "-t", required=False, default="./course/content", type=click.Path())
@click.option(
    "--clean", '-c', is_flag=True, required=False, help="Deletes the target folder and all its content before rendering"
)
@click.option(
    "--force", '-f', is_flag=True, required=False, help="Doesn't ask for confirmation before deleting or rewriting files"
)
def render(source, targer_folder, clean, force):
    root_path = targer_folder

    if clean:
        if os.path.exists(root_path):
            if not force:
                if not click.confirm('The folder {} and all its content will be deleted, do you want to continue?'.format(root_path), abort=True):
                    return
            rmtree(root_path)

    if not os.path.exists(root_path):
        os.makedirs(root_path)

    f = open(source, "r")
    t_o_c = ["# Table of contents"]
    chapter = ""
    section_title = ""
    section_content = ""
    section_not_empty = False
    chapter_cnt = 0
    section_cnt = 0
    for line in f:
        if line.startswith("# "):
            # Close previous section and create new chapter
            if section_not_empty:
                close_section(root_path, chapter, section_cnt, section_title, section_content, force, t_o_c)
                section_cnt += 1
                section_not_empty = False
            section_cnt = 0
            # Add to table of contents
            chapter_name = format_name(line)
            chapter = "{:02d}".format(chapter_cnt) + "-" + chapter_name
            chapter_path = os.path.join(root_path, chapter)
            rel_path = os.path.join(".", chapter)
            link = create_link(remove_hashtags(line), rel_path)
            t_o_c.append("* " + link)
            chapter_cnt += 1
            if not os.path.exists(chapter_path):
                os.mkdir(chapter_path)
            section_content = line
            section_title = line

        elif line.startswith("## "):
            # Close current section and start a new one
            if section_not_empty:
                close_section(root_path, chapter, section_cnt, section_title, section_content, force, t_o_c)
                section_cnt += 1
                section_not_empty = False
            section_title = line
            section_content = line[1:]

        else:
            if line.strip():
                section_not_empty = True
            text = line
            if re.match(r'^####* ', line):
                text = line[2:]
            section_content += text

    f.close()
    # Last section
    close_section(root_path, chapter, section_cnt, section_title, section_content, force, t_o_c)
    # Table of contents
    generate_table_of_contents(root_path, t_o_c)


if __name__ == "__main__":
    render()
