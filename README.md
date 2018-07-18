<p align="center">

<a href="https://pypi.python.org/pypi/metadocs">
  <img alt="PyPI" src="https://badge.fury.io/py/metadocs.svg">
</a>
<a href="https://github.com/ambv/black">
  <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://github.com/entrepreneur-interet-general/metadocs/blob/master/LICENCE">
  <img alt="License: AGPL v3" src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg">
</a>

</p>

<!-- TOC -->

- [About](#about)
- [Install](#install)
- [Getting Started](#getting-started)
- [Usage](#usage)
    - [Adding a Python project](#adding-a-python-project)
    - [Manual addition of a built documentation](#manual-addition-of-a-built-documentation)
    - [Customization](#customization)
        - [Useful Resources](#useful-resources)

<!-- /TOC -->
---


# About

`metadocs` allows you to integrate several `sphinx` documentation projects into one Home Documentation listing them and allowing you to have cross projects documentation with `mkdocs`. 

Any `sphinx` module can be used as long as `make html` works and the built code is in `your_documentation/your_project/build`.

`metadocs` comes with an example project and a standalone documention so you can already get started!

Default settings are that the Home Documentation will use a Material Design theme and Project Documentations will use Read The Docs's theme, to better distinguish the hierarchy. You can change that (in the global `mkdocs.yml` and in individual python projects' `conf.py`).

![metadocs illustration](https://i.imgur.com/OyYGmOL.png)

# Install

`metadocs` requires python3 and mainly uses `sphinx`, `mkdocs` and `watchdog` as 3rd party libraries. Check out the [full requirements](/requirements.txt)

```
pip install metadocs
```

# Getting Started

Start your Home Documentation with:

```
metadocs init your_home_documentation
```

Start the server with 

```
metadocs serve
```

Optionnaly you can specify a port with `metadocs serve -s your_port`

<img src="http://g.recordit.co/egF8bzx7qc.gif" alt="metadocs demo" style="max-width:300px"></img>

You can also manually build the documentation with `build`:

```
metadocs build [FLAGS]
```

Flags being:

```
  -v, --verbose                             verbose flag (Sphinx will stay verbose)
  -A, --all                                 Build doc for all projects
  -F, --force                               force the build, no verification asked
  -o, --only_index                          only build projects listed in the Documentation's Home
  -p, --projects [PROJECTS [PROJECTS ...]]  list of projects to build
```



# Usage

The package comes with a thorough documentation by default, which you'll see by running `metadocs serve` after a proper `init`. A Read The Docs-hosted version may arrive at some point. 

The built in documentation is there to help you but is in no way necessary, you can overwrite or delete everything. **There are however 2 mandatory things:**

**1** You have to keep this structure:

```
your_home_documentation/
    mkdocs.yml
    docs/ # your home documentation, listing sphinx docs
        index.md # mandatory file -> mkdocs's index
    site/
    your_project_1/
        build/ # sphinx's build directory
        source/ # sphinx's documentation source directory
        your_project_1/ # your documented code as a package
            __init__.py
            your_package_1_1/
            your_package_1_2/
            ...
    your_project_2/
        build/
        source/
        your_project_2/
            __init__.py
            your_package_2_1/
            your_package_2_2/
            ...
    ...
```

**2**  `mkdocs`'s `index.md` file must have a `# Projects` section listing them as in the example

Also, remember to run `build` or `serve` commands from your Home Documenation's **root folder** (in `your_home_documentation/` in the example above) otherwise you may get errors saying `metadocs` can't find a file.

## Adding a Python project

`metadocs` comes with a useful `autodoc` command helping you easily add a new python project to your documentation.

All you have to do is put the documented (Google-style docstrings) code along the documentation in `your_home_documentation/`. Say it's called `your_project_3`. Then you just need to make a new directory called `your_project_3` go there, copy `your_project_3`'s code in there (as a package, meaning it should include a `__init__.py` and use `autodoc`:

```
$ pwd
/path_to_your_documentation/
$ mkdir your_project_3
$ cd your_project_3
$ cp -r path/to/your_project_3 .
$ ls
your_project_3
$ metadocs autodoc
... some prints
$ ls
Makefile    source    build    your_project_3
```

Under the hood, `metadocs autodoc` runs `sphinx-quickstart`, updates default values in `conf.py`, runs `sphinx-apidoc`, rearranges the created `.rst` files, builds the documentation with `metadocs build` and updates the Home Documentation's `index.md` file to list `your_project_3`.

If `metadocs autodoc`'s default values for the `sphinx` documentation don't suit you, do update `/path_to_your_documentation/your_project_3/source/conf.py`.

<img src="http://g.recordit.co/Jo299BwQC5.gif" alt="metadocs autodoc demo" style="max-width:300px"></img>

## Manual addition of a built documentation

If you don't want to `metadocs autodoc`, you may use any sphinx configuration you want. Just keep in mind that `metadocs` will run `make html` from your project's directory (so check that this works) and `metadocs serve` expects to find a file called `index.html` in a directory called `build/` in your project.

## Customization

You may use any other theme for instance. To use `mkdocs-nature` just:

```
pip install mkdocs-nature
```

Then change this in `mkdocs.yaml` : `theme: nature` and finally:

```
mkdocs build
```

Edit the global configuration in `mkdocs.yaml` and each project's in `source/conf.py`.


### Useful Resources

* [Mkdocs's Getting Started](https://www.mkdocs.org/user-guide/writing-your-docs/)
* [Material for Mkdocs's customization instructions](https://squidfunk.github.io/mkdocs-material/customization/)
* [Material for Mkdocs's supported extensions list](https://squidfunk.github.io/mkdocs-material/extensions/admonition/)
