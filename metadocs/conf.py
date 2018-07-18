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

# Version string
__VERSION__ = "0.4"

# Key to state that a project's hard links must be updated
PROJECT_KEY = "# Projects"
# Hard link to the index.html file to update with link to the
# Documentation's home
HTML_LOCATION = "build/html/"
# mkdocs's home file
MKDOCS_INDEX = "docs/index.md"

# Substring marking the line to replace
TO_REPLACE_WITH_HOME = '<a href="_sources'
# New line replacing the above one
NEW_HOME_LINK = '<h3><a href="/">Home</a></h3>'
PORT = 8443
