# coding=utf-8
from __future__ import absolute_import, unicode_literals, print_function, division
from fabric.context_managers import cd
from fabric.decorators import task, hosts
from fabric.operations import run


def _fresh_clone_repo(virtual_env_dir, repo_folder_name='devbackend', tag='develop'):
    """
    Clone the git repo and checkout the correct tag.
    :param virtual_env_dir: directory path to the virtual env on the server
    :param repo_folder_name: name for the top level folder of the new repo
    :param tag: name of the tag/branch to checkout
    :return: None
    """
    with cd(virtual_env_dir):
        run('rm -rf {}/'.format(repo_folder_name))
        run('git clone git@104.236.119.129:root/swizly.git {}'.format(repo_folder_name))
        with cd('{}'.format(repo_folder_name)):
            run('git checkout {0}'.format(tag))


def _git_status(virtual_env_dir, repo_folder_name='devbackend'):
    """
    Run 'git status' on the git folder on the server
    :param virtual_env_dir: directory path to the virtual env on the server
    :param repo_folder_name: name for the top level folder of the new repo
    :return: None
    """
    with cd('{}/{}'.format(virtual_env_dir, repo_folder_name)):
        run('git status')


def _git_pull(virtual_env_dir, repo_folder_name='devbackend', branch='develop'):
    """
    Run 'git pull origin <branch>' on the git folder on the server
    :param virtual_env_dir: directory path to the virtual env on the server
    :param repo_folder_name: name for the top level folder of the new repo
    :param branch: The name of the branch to pull
    :return: None
    """
    with cd('{}/{}'.format(virtual_env_dir, repo_folder_name)):
        run('git pull origin {}'.format(branch))


def _git_reset_hard(virtual_env_dir, repo_folder_name='devbackend', branch=None):
    """
    Run 'git reset --hard' on the git folder on the server
    :param virtual_env_dir: directory path to the virtual env on the server
    :param repo_folder_name: name for the top level folder of the new repo
    :param branch: The name of the branch to reset to
    :return: None
    """
    with cd('{}/{}'.format(virtual_env_dir, repo_folder_name)):
        if branch:
            run('git reset --hard {}'.format(branch))
        else:
            run('git reset --hard')


def _git_checkout(virtual_env_dir, options=None, repo_folder_name='devbackend', branch='develop'):
    """
    Run 'git checkout <branch>' on the git folder on the server
    :param virtual_env_dir: directory path to the virtual env on the server
    :param options: options for the checkout command eg. '-f'
    :param repo_folder_name: name for the top level folder of the new repo
    :param branch: The name of the branch to checkout
    :return: None
    """
    with cd('{}/{}'.format(virtual_env_dir, repo_folder_name)):
        if options:
            run('git checkout {} {}'.format(options, branch))
        else:
            run('git checkout {}'.format(branch))


def _git_fetch(virtual_env_dir, options=None, repo_folder_name='devbackend'):
    """
    Run 'git checkout <branch>' on the git folder on the server
    :param virtual_env_dir: directory path to the virtual env on the server
    :param options: options for the fetch command eg. '--all'
    :param repo_folder_name: name for the top level folder of the new repo
    :return: None
    """
    with cd('{}/{}'.format(virtual_env_dir, repo_folder_name)):
        if options:
            run('git fetch {}'.format(options))
        else:
            run('git fetch')


S01 = 'root@104.236.35.196'
S02 = 'root@104.236.47.137'
S03 = 'root@104.236.17.228'
S04 = 'root@104.131.108.12'
S05 = 'root@104.131.166.166'
S06 = 'root@104.236.107.132'
RABBIT_MQ = 'root@104.236.86.150'
VIRTUAL_ENV_DIR = '/opt/apps/Swizly-3.0-env'


@task(default=True)
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def setup(branch=None):
    """
    Setup the git repo on all servers in the cluster.  fab setup | fab setup:branch='release/3.0'
    :param branch: optional argument for the git branch to checkout
    :return: None
    """
    if branch:
        _fresh_clone_repo(VIRTUAL_ENV_DIR, tag=branch)
    else:
        _fresh_clone_repo(VIRTUAL_ENV_DIR)


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def git_status():
    """
    Does 'git status' for each of the servers in the cluster.
    :return: None
    """
    _git_status(VIRTUAL_ENV_DIR)


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def git_pull(branch=None):
    """
    Does a 'git pull origin <branch>' for each of the servers in the cluster. fab git_pull:branch='release/3.0'
    :return: None
    """
    if branch:
        _git_pull(VIRTUAL_ENV_DIR, branch=branch)
    else:
        _git_pull(VIRTUAL_ENV_DIR)


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def git_checkout(options=None, branch=None):
    """
    Does a 'git checkout <branch>' for each of the servers in the cluster. fab git_checkout:options='-f',branch='release/3.0'
    :return: None
    """
    if branch:
        _git_checkout(VIRTUAL_ENV_DIR, options, branch=branch)
    else:
        _git_checkout(VIRTUAL_ENV_DIR, options)


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def git_reset(branch=None, hard=True):
    """
    Does a 'git reset' for each of the servers in the cluster. fab git_reset:branch='origin/develop',hard='False'
    :return: None
    """
    # TODO there is a bug here right now with the translation to boolean. Fix later
    if hard:
        _git_reset_hard(VIRTUAL_ENV_DIR, branch=branch)
    else:
        print('Not supported')


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def git_fetch(options=None):
    """
    Does a 'git fetch <options>' for each of the servers in the cluster. fab git_fetch:options='--all'
    :return: None
    """
    _git_fetch(VIRTUAL_ENV_DIR, options)
