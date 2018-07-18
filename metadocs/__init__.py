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

from .commands import init
from .commands import build
from .commands import serve
from .commands import version
from .commands import autodoc
from .commands import clean
from .commands import __VERSION__
from .utils import colors
__version__ = __VERSION__
