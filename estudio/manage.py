#!/usr/bin/env python
"""
Django’s command-line utility for administrative tasks.
"""

import os
import sys
from pathlib import Path

LOCAL_SETTINGS = "local_settings.py"


def set_settings_module():
    """
    This function will choose a Django settings file to work with.
    If you have a local file with settings, it will use that file.
    But if not, stay calm: it will directly go with "settings.py".
    """

    local_settings = Path(f"estudio/{LOCAL_SETTINGS}")
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"estudio.{local_settings.stem}"
        if local_settings.exists()
        else "estudio.settings",
    )


def main():
    set_settings_module()

    try:
        # pylint: disable=import-outside-toplevel
        from django.core.management import execute_from_command_line
    except ImportError as exception:
        raise ImportError("Could not import Django.") from exception
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
