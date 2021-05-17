import os
import sys


def get_resource_path(rel_path):
    return os.path.join(getattr(sys, '_MEIPASS', ""), 'resources', rel_path)
