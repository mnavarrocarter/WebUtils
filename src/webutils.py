import click
import os
import sys
from subprocess import call

# This config object will be created and instanciated so we can share 
# global parameters and options to share with the other groups of 
# applications.
class Config(object):
    def __init__(self):
        # We define the properties here
        self.verbose = False
        self.current_path = os.getcwd()

# We define a pass_config variable, so we pass the config.
pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--verbose', is_flag="True")
@pass_config
def cli(config, verbose):
    """
    WebUtils by Matias Navarro Carter
    
    Version: 1.0

    This program contains some useful tools for web development.

    If you happen to have a copy of this, consider yourself lucky.
    """
    config.verbose = verbose

###########################################################################
# WEBUTILS->APACHE
###########################################################################
@cli.group()
@pass_config
def apache(config):
    """Apache useful commands."""

@apache.command('newvhost', short_help='Creates a new Apache2 Virtual Host.')
@click.option('--string', default='World',
    help='This is the thing that is greeted.')
@click.option('--repeat', default=1,
    help='How many times you should be greeted.')
@click.argument('name',
    type=click.File('w'), default='default.dev', required=True)
@pass_config
def newvhost(config, string, repeat, out):
    """
    This command creates a new Apache2 Virtual Host

    Providing a name, it will create *.vhost-conf file in your Apache2
    virtualhost directory. We recommend the name to be something.dev like.
    Dev is a good top-level fake domain name to use for your development
    projects.

    It will create a record in your /etc/hosts file so your fake domain
    name can be resolvable in your browser.

    This script will automatically create the Document Root within your 
    /var/www/ directory. The --here flag will set the Document Root to your
    current working directory, will create the *.vhost-conf file in that
    directory and symlink it to Apache's virtual host directory.
    But keep in mind that Apache will need permissions to access that folder.
    Check 'webutils apache set_perm --help' for more info.
    """
    if config.verbose:
        click.echo('We are in verbose mode.')
    for x in xrange(repeat):
        click.echo('Hello %s' % string, file=out)


@apache.command('set-perm', short_help='Sets special permissions for a directory.')
@pass_config
def set_perm(config, string, repeat, out):
    """
    This command sets special Apache permissions for a directory.

    What this command does is that sets a directory's ownership to www-data
    user and group, so Apache can write there no matter what.
    
    If no directory is specified, then the current working directory
    is used.

    Keep in mind that you will no longer have access to that directory, because
    you are not the www-data user and you do not belong to the www-data group.
    The --www-data-add flag will solve that for you, and will add your user
    to the www-data group so you can see those files.

    This command is intended to be used to give permissions to a Projects 
    folder of some sort in your home directory or alike, where you will
    have your web projects to be served.
    
    All this will require sudo privileges.
    """
    # sudo adduser $USER www-data
    # sudo chown -R www-data:www-data /home/$USER/public_html
    # sudo chmod -R 775 /home/$USER/public_html 

###########################################################################
# GIT COMMANDS
###########################################################################