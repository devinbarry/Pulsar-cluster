# coding=utf-8
from __future__ import absolute_import, unicode_literals, print_function, division
from fabric.context_managers import cd
from fabric.decorators import task, hosts
from fabric.operations import run


def fresh_clone_repo(virtual_env_dir, repo_folder_name='devbackend', tag='develop'):
    """
    Clone the git repo and checkout the correct tag.
    :param virtual_env_dir: name for the top level folder of the new repo
    :param tag: name of the tag/branch to checkout
    :return: None
    """
    with cd(virtual_env_dir):
        run('rm -rf {}/'.format(repo_folder_name))
        run('git clone git@104.236.119.129:root/swizly.git {}'.format(repo_folder_name))
        with cd('{}'.format(repo_folder_name)):
            run('git checkout {0}'.format(tag))


S01 = 'root@104.236.35.196'
S02 = 'root@104.236.47.137'
S03 = 'root@104.236.17.228'
S04 = 'root@104.131.108.12'
S05 = 'root@104.131.166.166'
S06 = 'root@104.236.107.132'
RabbitMQ = 'root@104.236.86.150'


@task(default=True)
@hosts(S01, S02, S03, S04, S05, S06, RabbitMQ)
def setup(branch=None):
    """ Setup the git repo on all servers in the cluster.  fab setup | fab setup:branch='release/3.0'
    """
    virtual_env_dir = '/opt/apps/Swizly-3.0-env'
    fresh_clone_repo(virtual_env_dir)
