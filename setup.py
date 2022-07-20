from setuptools import setup

setup(
    name="md-titles-to-sections",
    version="0.1.0",
    py_modules=["md_titles_sections"],
    install_requires=['click==8.1.3'],
    entry_points={
        "console_scripts": [
            "md-render = mdown_render:render",
        ],
    },
)