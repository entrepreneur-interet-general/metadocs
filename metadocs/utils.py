# metadocs: Manage sphinx documentations with mkdocs
# Copyright (C) 2018  Victor Schmidt vsch[at]pm.me

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import fnmatch
import json
import os
import re
import subprocess
from pathlib import Path
from shutil import copyfile

from watchdog.events import PatternMatchingEventHandler

from .conf import HTML_LOCATION, NEW_HOME_LINK, PROJECT_KEY, TO_REPLACE_WITH_HOME


class colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def suggest_path(func):
    def wrapper(*args, **kwds):
        try:
            func(*args, **kwds)
        except FileNotFoundError as e:
            print(e)
            print()
            print(
                '{}Are you sure you ran "{}" in the right directory?{}'.format(
                    colors.FAIL, func.__name__, colors.ENDC
                )
            )
            try:
                dir_path = Path().absolute()
                potential_projects = [
                    str(p)
                    for p in dir_path.iterdir()
                    if p.is_dir()
                    and any(["mkdocs.yml" in str(sp) for sp in p.iterdir()])
                ]
                locations = [
                    "." + p[p.find(str(dir_path)) + len(str(dir_path)) :]
                    for p in potential_projects
                ]
                print("Try in", "\n".join(locations))
            except:
                pass

    return wrapper


def overwrite_view_source(project, dir_path):
    """In the project's index.html built file, replace the top "source"
    link with a link to the documentation's home, which is mkdoc's home

    Args:
        project (str): project to update
        dir_path (pathlib.Path): this file's path
    """

    project_html_location = dir_path / project / HTML_LOCATION
    if not project_html_location.exists():
        return

    files_to_overwrite = [
        f for f in project_html_location.iterdir() if "html" in f.suffix
    ]

    for html_file in files_to_overwrite:
        with open(html_file, "r") as f:
            html = f.readlines()
        for i, l in enumerate(html):
            if TO_REPLACE_WITH_HOME in l:
                html[i] = NEW_HOME_LINK
                break
        with open(html_file, "w") as f:
            f.writelines(html)


def get_listed_projects():
    """Find the projects listed in the Home Documentation's
    index.md file

    Returns:
        set(str): projects' names, with the '/' in their beginings
    """
    index_path = Path().resolve() / "docs" / "index.md"
    with open(index_path, "r") as index_file:
        lines = index_file.readlines()

    listed_projects = set()
    project_section = False
    for _, l in enumerate(lines):
        idx = l.find(PROJECT_KEY)
        if idx >= 0:
            project_section = True
        if project_section:
            # Find first parenthesis after the key
            start = l.find("](")
            if start > 0:
                closing_parenthesis = sorted(
                    [m.start() for m in re.finditer(r"\)", l) if m.start() > start]
                )[0]
                project = l[start + 2 : closing_parenthesis]
                listed_projects.add(project)
        # If the Projects section is over, stop iteration.
        # It will stop before seeing ## but wainting for it
        # Allows the user to use single # in the projects' descriptions
        if len(listed_projects) > 0 and l.startswith("#"):
            return listed_projects
    return listed_projects


def set_routes():
    """Set the METADOCS_ROUTES environment variable with a serialized list
    of list of routes, one route being:
        [pattern to look for, absolute location]
    """
    os.system("pwd")
    dir_path = Path(os.getcwd()).absolute()
    projects = get_listed_projects()
    routes = [
        [p if p[0] == "/" else "/" + p, str(dir_path) + "{}/build/html".format(p)]
        for p in projects
    ]
    os.environ["METADOCS_ROUTES"] = json.dumps(routes)


def get_routes():
    """Parse routes from environment.

    Returns:
        list(list): list of routes, one route being:
            [pattern to look for, absolute location]
    """
    return json.loads(os.getenv("METADOCS_ROUTES", "[[]]"))


class MetadocsFileHandler(PatternMatchingEventHandler):
    """Class handling file changes:
        .md: The Home Documentation has been modified
            -> mkdocs build
        .rst: A project's sphinx documentation has been modified
            -> metadocs build -F -p {project}
    """

    def on_any_event(self, event):
        set_routes()

        offline = ""
        if event.src_path.split(".")[-1] in {"md", "yml", "yaml"}:
            try:
                _ = subprocess.check_output("mkdocs build > /dev/null", shell=True)
            except subprocess.CalledProcessError as e:
                print(e, "\n")
            if json.loads(os.getenv("METADOCS_OFFLINE", "false")):
                make_offline()

        if event.src_path.split(".")[-1] == "rst":
            # src_path:
            # /Users/you/Documents/YourDocs/example_project/source/index.md
            # os.getcwd():
            # /Users/you/Documents/YourDocs
            # relative_path:
            # /example_project/docs/index.md
            # project: example_project

            relative_path = event.src_path.split(os.getcwd())[-1]
            project = relative_path.split("/")[1]
            if json.loads(os.getenv("METADOCS_OFFLINE", "false")):
                offline = "--offline"
            os.system("metadocs build -F {} -p {} > /dev/null".format(offline, project))


def make_offline():
    """Deletes references to the external google fonts in the Home
    Documentation's index.html file
    """
    dir_path = Path(os.getcwd()).absolute()

    css_path = dir_path / "site" / "assets" / "stylesheets"
    material_css = css_path / "material-style.css"
    if not material_css.exists():
        file_path = Path(__file__).resolve().parent
        copyfile(file_path / "material-style.css", material_css)
        copyfile(file_path / "material-icons.woff2", css_path / "material-icons.woff2")

    indexes = []
    for root, _, filenames in os.walk(dir_path / "site"):
        for filename in fnmatch.filter(filenames, "index.html"):
            indexes.append(os.path.join(root, filename))
    for index_file in indexes:
        update_index_to_offline(index_file)


def update_index_to_offline(path):
    with open(path, "r") as f:
        lines = f.readlines()
    new_lines = []
    for l in lines:
        if "https://fonts" in l:
            if "icon" in l:
                new_lines.append(
                    '<link rel="stylesheet"'
                    + " href=/assets/stylesheets/material-style.css>"
                )
            elif "css" in l:
                pass
        else:
            new_lines.append(l)
    with open(path, "w") as f:
        f.writelines(new_lines)


def set_sphinx_config(path_to_config, project_name, mocks):
    path = Path(path_to_config).resolve()
    with path.open("r") as f:
        lines = f.readlines()

    new_lines = []

    for l in lines:
        if "# import os" in l:
            l = "import os\n"
        if "# import sys" in l:
            l = "import sys\n"
        if "# sys.path.insert(0, os.path.abspath('.'))" in l:
            l = "sys.path.insert(0, os.path.abspath('.'))\n"
            l += "sys.path.insert(0, os.path.abspath('..'))\n"
            l += "sys.path.insert(0, os.path.abspath('../{}'))\n".format(project_name)
        if "'sphinx.ext.viewcode'," in l:
            l = "'sphinx.ext.viewcode', 'sphinx.ext.napoleon'\n"
        if "html_theme = 'alabaster'" in l:
            l = "html_theme = 'sphinx_rtd_theme'\n"
        new_lines.append(l)

    extended_conf = "\nhtml_theme_options = {\n"
    extended_conf += "    'titles_only': True,\n"
    extended_conf += "    'navigation_depth': -1,\n"
    extended_conf += "    'collapse_navigation': False\n"
    extended_conf += "}\n"
    extended_conf += "\nautoclass_content = 'both'\n"
    if mocks:
        extended_conf += "\nautodoc_mock_imports = [{}]\n".format(
            ", ".join('"{}"'.format(m) for m in mocks)
        )

    new_lines.append(extended_conf)

    with path.open("w") as f:
        f.write("".join(new_lines))


def create_rst_for_package(package_path, source_path):
    title = "``{}``".format(package_path.name)
    header = "{}\n{}\n{}\n\n\n".format("*" * len(title), title, "*" * len(title))

    body = (
        "This is the package's auto-documentation generated by ``metadocs``"
        + " using ``sphinx``'s ``autodoc``.\nYou may edit this .rst file.\n\n"
    )

    module_names = [
        m.name
        for m in package_path.iterdir()
        if m.suffix == ".py" and "__" not in m.name
    ]

    for m in module_names:
        sub_body = m.capitalize()
        sub_body += "\n{}\n\n".format("=" * len(sub_body))
        sub_body += ".. automodule:: {}.{}\n".format(
            package_path.name, m.split(".py")[0]
        )
        sub_body += "   :members:\n\n"
        body += sub_body

    filename = package_path.name + ".rst"
    with open(source_path / filename, "w") as f:
        f.write(header + body)


def add_project_to_rst_index(index_path, project_name):
    with open(index_path, "r") as index_file:
        lines = index_file.readlines()

    for i, l in enumerate(lines):
        if "Indices and tables" in l:
            l = "   {}\n\n".format(project_name)
            lines[i] = l
        elif ":maxdepth:" in l:
            l = "   :maxdepth: 6\n"
            lines[i] = l

    with open(index_path, "w") as f:
        f.write("".join(lines))


def add_project_to_doc_index(index_path, project_name):

    with open(index_path, "r") as index_file:
        lines = index_file.readlines()

    new_lines = []
    project_strings = []
    project_section = False
    for _, l in enumerate(lines):
        idx = l.find(PROJECT_KEY)

        if idx >= 0:
            project_section = True
            new_lines.append(l)
            continue

        if project_section:
            if "#" in l:
                project_section = False
                project_exists = False
                for p in project_strings:
                    if "(/{})".format(project_name) in p:
                        project_exists = True
                if not project_exists:
                    project_strings.append(
                        "* [{}](/{}/) - [Project Desctiption to write]".format(
                            " ".join([w.capitalize() for w in project_name.split("_")]),
                            project_name,
                        )
                    )
                    l = "\n".join(project_strings) + "\n" + l
            else:
                if "*" in l and "](" in l:
                    project_strings.append(l.replace("\n", ""))
                    l = ""

        new_lines.append(l)
    with open(index_path, "w") as f:
        f.write("".join([l for l in new_lines if l]))


def remove_project_name_from_titles(source_path):
    path = Path(source_path)
    for fname in path.iterdir():
        if fname.is_file() and fname.suffix == ".rst":
            with open(fname, "r") as f:
                lines = f.readlines()

            if "==" in lines[1]:
                no_package_or_modules = lines[0].split(" ")[0]
                no_path = no_package_or_modules.split(".")[-1]
                formatted = "``{}``".format(no_path).replace("\_", "_")
                lines[0] = formatted + "\n"
                lines[1] = "=" * len(formatted) + "\n"

            with open(fname, "w") as f:
                f.write("".join(lines))
