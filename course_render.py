import click
import os
import re
from shutil import rmtree


def close_section(root_path, chapter, section_title, section_content, force):
    file_name = os.path.join(root_path, chapter, section_title + '.md')
    if not force and os.path.exists(file_name):
        if not click.confirm('The file {} already exists and will be overwritten, do you want to continue?'.format(file_name)):
            return
    if section_content:
        with open(file_name, 'w') as new_f:
            new_f.write(section_content)


def format_name(name):
    # Remove all # and the first space at the beginning
    name = re.sub(r'^#* ', '', name)
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
        if not force and os.path.exists(root_path):
            if not click.confirm('The folder {} and all its content will be deleted, do you want to continue?'.format(root_path), abort=True):
                return
        rmtree(root_path)

    if not os.path.exists(root_path):
        os.makedirs(root_path)

    f = open(source, "r")
    chapter = ""
    section_title = ""
    section_content = ""
    for line in f:
        if line.startswith("# "):
            # Close previous section and create new chapter
            if section_content:
                close_section(root_path, chapter, section_title, section_content, force)
                section_content = ""
                section_title = ""

            chapter = format_name(line)
            chapter_path = os.path.join(root_path, chapter)
            if not os.path.exists(chapter_path):
                os.mkdir(chapter_path)

        elif line.startswith("## "):
            # Close current section and start a new one
            if section_content:
                close_section(root_path, chapter, section_title, section_content, force)
                section_content = ""
            section_title = format_name(line)

        else:
            # Exclude the text between chapter name and section title
            if section_title:
                section_content += line

    f.close()
    # Last section
    close_section(root_path, chapter, section_title, section_content, force)


if __name__ == "__main__":
    render()
