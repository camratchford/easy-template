import os
import logging
from pathlib import Path

import click
from {{ project_stub }}.config import config
from {{ project_stub }}.__main__ import main

from {{ project_stub }}.commands.create_user import create_superuser


logger = logging.getLogger("__name__")
