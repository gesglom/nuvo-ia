import os

WORKSPACE = "workspace"


def scan_project():

    files = []

    for root, dirs, filenames in os.walk(WORKSPACE):

        for f in filenames:

            path = os.path.join(root, f)

            files.append(path)

    return files
