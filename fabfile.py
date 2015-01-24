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
    """
    _fresh_clone_repo(VIRTUAL_ENV_DIR)


@task()
@hosts(S01, S02, S03, S04, S05, S06, RABBIT_MQ)
def get_git_status():
    """
    Returns the output of 'git status' for each of the servers in the cluster.
    :return:
    """
    _git_status(VIRTUAL_ENV_DIR)
