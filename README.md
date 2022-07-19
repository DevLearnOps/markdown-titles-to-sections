# markdown-titles-to-sections
A command line tool to generate multiple files from a single markdown document

## What does this do?
It renders a single markdown file into multiple files for every section.
Useful for maintaining a single markdown that can be separated into multiple sections automatically.

## How does it work?
Install it with the command 

```
pip install .
```

Then generate the files using the command

```
course-render <path/to/source>
```

Few options are available:

- `-t`/`--targer_folder`: Specify where to generate the files, if not specified the files will be generated at `./course/content`
- `-c`/`--clean`: Deletes the target folder before rendering
- `f`/`--force`: Doesn't ask for confirmation before deleting the target folder or overwriting the files
