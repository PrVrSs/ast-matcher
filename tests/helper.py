import tomlkit
from collections import namedtuple
from distutils.version import LooseVersion
from pathlib import Path


CONFIG = (Path(__file__).parent.parent / 'pyproject.toml').resolve()

NodeFixture = namedtuple('NodeFixture', 'code, pattern')


def get_project_meta():
    with open(str(CONFIG)) as pyproject:
        file_contents = pyproject.read()

    return tomlkit.parse(file_contents)['tool']['poetry']


version = LooseVersion(str(get_project_meta()['version']))
