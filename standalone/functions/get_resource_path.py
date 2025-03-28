import os
import sys

def get_resource_path(relative_path):
    """Get the absolute path to a resource, works for development and PyInstaller."""
    if getattr(sys, '_MEIPASS', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)