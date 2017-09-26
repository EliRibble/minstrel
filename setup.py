#!/usr/bin/env python
import imp
import os
import re
import subprocess

from setuptools import setup

DATA_ROOTS = ['alembic']
PROJECT = 'minstrel'
VERSION_FILE = 'minstrel/version.py'

def _get_output_or_none(args):
    try:
        return subprocess.check_output(args).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def _get_git_description():
    return _get_output_or_none(['git', 'describe'])

def _get_git_branches_for_this_commit():
    branches = _get_output_or_none(['git', 'branch', '-r', '--contains', 'HEAD'])
    split = branches.split('\n') if branches else []
    return [branch.strip() for branch in split]

def _is_on_releasable_branch(branches):
    return any([branch == 'origin/master' or branch.startswith('origin/hotfix') for branch in branches])

def _git_to_version(git):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git)
    if not match:
        version = git
    else:
        version = "{tag}.post0.dev{offset}".format(**match.groupdict())
    print("Calculated {} version '{}' from git description '{}'".format(PROJECT, version, git))
    return version

def write_version():
    git_description = _get_git_description()
    git_branches = _get_git_branches_for_this_commit()
    version = _git_to_version(git_description) if git_description else None
    if git_branches and not _is_on_releasable_branch(git_branches):
        print("Forcing version to 0.0.1 because this commit is on branches {} and not a whitelisted branch".format(git_branches))
        version = '0.0.1'
    if not version:
        return
    with open(VERSION_FILE, 'w') as version_file:
        new_contents = '__version__ = "{}"\n'.format(version)
        version_file.write(new_contents)
        print("Wrote '{}' to {}".format(new_contents, VERSION_FILE))

def get_version():
    basedir = os.path.abspath(os.path.dirname(__file__))
    version = imp.load_source('version', os.path.join(basedir, PROJECT, '__init__.py'))
    return version.__version__

def get_data_files():
    data_files = []
    for data_root in DATA_ROOTS:
        for root, _, files in os.walk(data_root):
            data_files.append((os.path.join(PROJECT, root), [os.path.join(root, f) for f in files]))
    return data_files

def main():
    write_version()
    setup(
        name='minstrel',
        version=get_version(),
        description="A system for using machine learning to play music for my mood or task",
        long_description=open('README.md').read(),
        author='Eli Ribble',
        author_email='junk@theribbles.org',
        install_requires=[
            'chryso==1.25',
            'eyed3==0.8.2',
            'flask',
        ],
        extras_require={
            'develop': [
                'pytest==3.0.2',
                'pytest-cov==2.3.1',
            ],
        },
        packages=[
            'minstrel',
        ],
        package_data={
            'minstrel'                : ['minstrel/*'],
        },
        data_files          = get_data_files(),
        scripts             = ['bin/minstrel-debug'],
        include_package_data=True,
    )

if __name__ == '__main__':
    main()
